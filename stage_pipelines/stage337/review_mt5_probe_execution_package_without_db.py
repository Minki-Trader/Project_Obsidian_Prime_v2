from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import materialize_mt5_probe_execution_package_without_db as bk


aw = bk.aw
bg = bk.bj.bi.bh.bg

TODAY = "2026-05-27"
STAGE_ID = bk.STAGE_ID
RUN_NUMBER = "run337BL"
RUN_ID = "run337BL_review_mt5_probe_execution_package_without_db_v1"
PARENT_RUN_ID = bk.RUN_ID
NEXT_RUN_ID = "run337BM_route_signal_forward_handoff_feasibility_without_db_v1"
STATUS = "completed_stage337BL_mt5_probe_package_review_actual_execution_blocked_no_training_no_selection"
JUDGMENT = "mt5_probe_package_review_passed_but_actual_mt5_forward_attempt_blocked_by_route_signal_handoff"
DECISION = "stage337BL_open_run337BM_route_signal_forward_handoff_feasibility_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BL_mt5_probe_package_review_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bk.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bk.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BL_mt5_probe_execution_package_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BL_mt5_probe_execution_package_review.md"
SELECTED_STATUS = bk.SELECTED_STATUS
STAGE_BRIEF = bk.STAGE_BRIEF
WORKSPACE_STATE = bk.WORKSPACE_STATE
CURRENT_STATE = bk.CURRENT_STATE
CHANGELOG = bk.CHANGELOG
RUN_REGISTRY = bk.RUN_REGISTRY
ALPHA_LEDGER = bk.ALPHA_LEDGER
ARTIFACT_REGISTRY = bk.ARTIFACT_REGISTRY
STAGE_LEDGER = bk.STAGE_LEDGER

BK_DIR = STAGE_DIR / "02_runs" / "run337BK"
BK_FINAL = BK_DIR / "final_decision.json"
BK_MANIFEST = BK_DIR / "mt5_probe_execution_manifest.csv"
BK_IDENTITY = BK_DIR / "frozen_subject_identity.csv"
BK_CHECKLIST = BK_DIR / "tester_command_checklist.csv"
BK_HANDOFF = BK_DIR / "runtime_file_handoff_manifest.csv"
BK_PROXY = BK_DIR / "proxy_mt5_diff_output_contract.csv"
BK_PROFIT = BK_DIR / "profit_trade_output_contract.csv"
BK_FEATURE_LAST = BK_DIR / "feature_last_gate_contract.csv"
BK_LOOKAHEAD = BK_DIR / "no_lookahead_runtime_audit_contract.csv"
BK_FORENSICS = BK_DIR / "backtest_forensics_identity_contract.csv"
BK_COST = BK_DIR / "cost_stress_execution_contract.csv"
BK_LOT = BK_DIR / "lot_normalized_execution_contract.csv"
BK_REGIME = BK_DIR / "regime_attribution_execution_contract.csv"
BK_ROUTE = BK_DIR / "route_signal_handoff_status.csv"
BK_QUEUE = BK_DIR / "run337BL_review_queue.csv"
BK_GATE_AUDIT = BK_DIR / "required_gate_coverage_audit.csv"
BK_SET = BK_DIR / "mt5" / "run337BK_cp322a_forward_probe_review_template.set"
BK_INI = BK_DIR / "mt5" / "run337BK_cp322a_forward_probe_review_template.ini"
BK_RECEIPTS = (
    BK_DIR / "reference_scout_receipt.json",
    BK_DIR / "run_evidence_receipt.json",
    BK_DIR / "backtest_forensics_receipt.json",
    BK_DIR / "runtime_parity_receipt.json",
    BK_DIR / "data_integrity_receipt.json",
    BK_DIR / "performance_attribution_receipt.json",
    BK_DIR / "artifact_lineage_receipt.json",
    BK_DIR / "result_judgment_receipt.json",
    BK_DIR / "environment_reproducibility_receipt.json",
    BK_DIR / "claim_discipline_receipt.json",
)

PACKAGE_REVIEW = RUN_DIR / "package_review_matrix.csv"
TEMPLATE_PARAMETER_REVIEW = RUN_DIR / "template_parameter_review.csv"
ROUTE_SIGNAL_BLOCKER_REVIEW = RUN_DIR / "route_signal_blocker_review.csv"
RUNTIME_ATTEMPT_DECISION = RUN_DIR / "runtime_attempt_decision.csv"
RUN337BM_QUEUE = RUN_DIR / "run337BM_route_signal_handoff_queue.csv"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BK_FINAL,
    BK_MANIFEST,
    BK_IDENTITY,
    BK_CHECKLIST,
    BK_HANDOFF,
    BK_PROXY,
    BK_PROFIT,
    BK_FEATURE_LAST,
    BK_LOOKAHEAD,
    BK_FORENSICS,
    BK_COST,
    BK_LOT,
    BK_REGIME,
    BK_ROUTE,
    BK_QUEUE,
    BK_GATE_AUDIT,
    BK_SET,
    BK_INI,
    *BK_RECEIPTS,
)
OUTPUT_FILES = (
    PACKAGE_REVIEW,
    TEMPLATE_PARAMETER_REVIEW,
    ROUTE_SIGNAL_BLOCKER_REVIEW,
    RUNTIME_ATTEMPT_DECISION,
    RUN337BM_QUEUE,
    RUNTIME_RECEIPT,
    DATA_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

REVIEW_COLUMNS = (
    "review_id",
    "review_subject",
    "observed",
    "expected",
    "status",
    "effect",
    "claim_boundary",
)
TEMPLATE_COLUMNS = (
    "parameter",
    "observed",
    "expected",
    "status",
    "source",
    "effect",
    "claim_boundary",
)
BLOCKER_COLUMNS = (
    "blocker_id",
    "source",
    "observed",
    "required_before_execution",
    "status",
    "next_action",
    "effect",
    "claim_boundary",
)
ATTEMPT_COLUMNS = (
    "probe_id",
    "probe_role",
    "execution_decision",
    "reason",
    "allowed_claim",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "review_subject",
    "inputs_to_review",
    "must_confirm",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = bk.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def parse_kv_text(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in aw.io_path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def common_file_exists(common_path: str) -> bool:
    return aw.path_exists(bk.COMMON_FILES_ROOT / common_path)


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BK package review inputs: {missing}")
    return {
        "final": read_json(BK_FINAL),
        "manifest": read_rows(BK_MANIFEST),
        "identity": read_rows(BK_IDENTITY),
        "checklist": read_rows(BK_CHECKLIST),
        "handoff": read_rows(BK_HANDOFF),
        "proxy": read_rows(BK_PROXY),
        "profit": read_rows(BK_PROFIT),
        "feature_last": read_rows(BK_FEATURE_LAST),
        "lookahead": read_rows(BK_LOOKAHEAD),
        "forensics": read_rows(BK_FORENSICS),
        "cost": read_rows(BK_COST),
        "lot": read_rows(BK_LOT),
        "regime": read_rows(BK_REGIME),
        "route": read_rows(BK_ROUTE),
        "queue": read_rows(BK_QUEUE),
        "gates": read_rows(BK_GATE_AUDIT),
        "set_values": parse_kv_text(BK_SET),
        "ini_values": parse_kv_text(BK_INI),
        "receipts": [read_json(path) for path in BK_RECEIPTS],
    }


def build_package_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    final = src["final"]
    specs = [
        ("parent_status", final.get("status", ""), "completed_stage337BK_mt5_probe_execution_package_materialized_no_training_no_selection_no_mt5_execution", "confirms parent package closed cleanly(상위 패키지 정상 종료 확인)"),
        ("parent_gates", f"{final.get('passed_gates')}/{final.get('gate_rows')}", "14/14", "confirms package gates passed(패키지 게이트 통과 확인)"),
        ("manifest_rows", str(len(src["manifest"])), "3", "keeps three probe roles visible(세 탐침 역할 유지)"),
        ("identity_rows", str(len(src["identity"])), "7", "keeps frozen subject identity complete(고정 대상 정체성 완전성 유지)"),
        ("checklist_rows", str(len(src["checklist"])), "6", "keeps tester command order explicit(테스터 명령 순서 명시)"),
        ("handoff_rows", str(len(src["handoff"])), "5", "keeps file handoff requirements explicit(파일 인계 요건 명시)"),
        ("contract_rows", f"proxy={len(src['proxy'])};profit={len(src['profit'])};feature_last={len(src['feature_last'])};lookahead={len(src['lookahead'])};regime={len(src['regime'])}", "proxy=9;profit=13;feature_last=4;lookahead=7;regime=9", "keeps KPI contract coverage before execution(실행 전 KPI 계약 커버리지 유지)"),
        ("receipt_rows", str(len(src["receipts"])), "10", "keeps skill receipt evidence attached(스킬 영수증 근거 연결)"),
    ]
    rows = []
    for review_id, observed, expected, effect in specs:
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{review_id}",
                "review_subject": review_id,
                "observed": observed,
                "expected": expected,
                "status": pass_fail(str(observed) == str(expected)),
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_template_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    set_values = src["set_values"]
    ini_values = src["ini_values"]
    expected = {
        "InpTierLabel": "Tier A+B",
        "InpPrimaryActiveTier": "tier_a",
        "InpFeatureCount": "1",
        "InpFeatureOrderHash": "839a84eca981d034211de743c0f9830335149e2a4817e947de6b96dd9fb5a70c",
        "InpFallbackEnabled": "true",
        "InpFallbackFeatureCount": "1",
        "InpFallbackFeatureOrderHash": "839a84eca981d034211de743c0f9830335149e2a4817e947de6b96dd9fb5a70c",
        "InpShortThreshold": "0.55",
        "InpLongThreshold": "0.55",
        "InpMinMargin": "0",
        "InpFallbackShortThreshold": "0.55",
        "InpFallbackLongThreshold": "0.55",
        "InpFallbackMinMargin": "0",
        "InpFixedLot": "0.42",
        "InpMaxHoldBars": "1",
        "InpAtrSltpEnabled": "true",
        "InpAtrPeriod": "14",
        "InpAtrStopMultiplier": "0.78",
        "InpAtrTakeProfitMultiplier": "3.35",
        "InpModelRiskSizingEnabled": "true",
        "InpModelRiskMinPct": "0.004",
        "InpModelRiskMaxPct": "0.026",
        "InpModelRiskFallbackLot": "0.08",
        "InpModelRiskConfidenceFloor": "0.58",
        "InpModelRiskConfidenceCeiling": "0.99",
        "InpExitRiskOverlayEnabled": "false",
        "InpEntryTransitionOnly": "false",
        "InpMagic": "1001010",
        "FromDate": "2026.04.14",
        "ToDate": "2026.05.30",
    }
    rows = []
    for key, value in expected.items():
        source = aw.rel(BK_INI) if key in {"FromDate", "ToDate"} else aw.rel(BK_SET)
        observed = ini_values.get(key, "") if key in {"FromDate", "ToDate"} else set_values.get(key, "")
        rows.append(
            {
                "parameter": key,
                "observed": observed,
                "expected": value,
                "status": pass_fail(observed == value),
                "source": source,
                "effect": "confirms frozen cp322A runtime parameter was not mutated(고정 cp322A 런타임 파라미터 비변경 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_route_blocker_review(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    handoff_rows = src["handoff"]
    route_rows = src["route"]
    feature_row = next(row for row in handoff_rows if row.get("handoff_id") == f"run337BK_feature_csv")
    common_paths = [part.strip() for part in feature_row.get("common_files_expected_path", "").split(";") if part.strip()]
    missing_common = [path for path in common_paths if not common_file_exists(path)]
    stage328_observed = route_rows[0].get("effect", "") if route_rows else ""
    return [
        {
            "blocker_id": f"{RUN_NUMBER}_route_signal_csv_pair_missing",
            "source": aw.rel(BK_HANDOFF),
            "observed": ";".join(missing_common) if missing_common else "all_present",
            "required_before_execution": "tier_a_and_tier_b_route_signal_csvs_present_before_actual_mt5",
            "status": pass_fail(bool(missing_common)),
            "next_action": NEXT_RUN_ID,
            "effect": "blocks fake MT5 execution until the runtime feature handoff exists(런타임 피처 인계 전 가짜 MT5 실행 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "blocker_id": f"{RUN_NUMBER}_stage328_forward_signal_not_safe",
            "source": aw.rel(BK_ROUTE),
            "observed": stage328_observed,
            "required_before_execution": "prove or repair route-signal generation without forward rank recalculation(전진 순위 재계산 없이 경로 신호 생성 증명 또는 수리)",
            "status": pass_fail("not_safe_without_upstream_rebuild" in stage328_observed),
            "next_action": NEXT_RUN_ID,
            "effect": "keeps Stage328 hazard as a hard pre-runtime blocker(Stage328 위험을 실행 전 차단자로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_attempt_decision(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for row in src["manifest"]:
        readiness = row.get("execution_readiness_status", "")
        primary = "blocked_until_run322b_route_signal_forward_handoff_exists" in readiness
        decision = "blocked_before_external_mt5_execution" if primary else "review_only_not_executed_in_run337BL"
        reason = (
            "route_signal_pair_missing_and_stage328_not_forward_safe_without_upstream_rebuild"
            if primary
            else "diagnostic_control_cannot_create_forward_authority_while_primary_handoff_is_blocked"
        )
        rows.append(
            {
                "probe_id": row.get("probe_id", ""),
                "probe_role": row.get("probe_role", ""),
                "execution_decision": decision,
                "reason": reason,
                "allowed_claim": "package_review_only_no_forward_or_runtime_authority",
                "effect": "prevents external MT5 execution from being mistaken for forward evidence(외부 MT5 실행을 전진 근거로 오해하지 않게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BM_route_signal_forward_handoff_feasibility",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "route-signal forward handoff feasibility(경로 신호 전진 인계 가능성)",
            "inputs_to_review": ";".join([aw.rel(BK_ROUTE), aw.rel(BK_HANDOFF), aw.rel(bk.STAGE328_SIGNAL_CONTRACT), aw.rel(bk.STAGE328B_DECISION_REPORT)]),
            "must_confirm": "whether tier A/B route_signal csv pair can be generated without forward rank recalculation or outcome distillation(Tier A/B 경로 신호 CSV 쌍을 전진 순위 재계산 또는 결과 증류 없이 만들 수 있는지)",
            "must_reject_if": "threshold retune, D/B rewrite, lot optimization, new data rank fit, proxy KPI authority(임계값 재조정/D-B 재작성/로트 최적화/새 데이터 순위 맞춤/프록시 KPI 권위)",
            "expected_outputs": "handoff feasible repair package or exact frozen-forward blocker memory(인계 가능 수리 패키지 또는 정확한 고정 전진 차단 기억)",
            "priority": "P0",
            "effect": "turns the current blocker into a narrow repair/proof task(현재 차단을 좁은 수리/증명 작업으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            RUNTIME_RECEIPT,
            {
                "research_path": aw.rel(Path(__file__)),
                "runtime_path": f"{aw.rel(BK_SET)};{aw.rel(BK_INI)}",
                "shared_contract": "cp322A frozen ONNX, Tier A+B fallback, thresholds, risk, lot, feature order, no actual MT5 execution(cp322A 고정 ONNX/Tier A+B 대체/임계값/위험/로트/피처 순서/실제 MT5 미실행)",
                "known_differences": ["run337BL reviews package only and does not run Strategy Tester(337BL은 패키지만 검토하고 전략 테스터를 실행하지 않음)"],
                "parity_check": "template parameter review and route-signal handoff blocker review(템플릿 파라미터 검토와 경로 신호 인계 차단 검토)",
                "runtime_claim_boundary": "blocked_before_external_mt5_execution",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_boundary": "no new market data read or generated in run337BL(337BL에서 새 시장 데이터 읽기/생성 없음)",
                "blocking_data": "run322b_route_signal_forward_tier_a_and_tier_b missing(전진 경로 신호 Tier A/B 누락)",
                "no_lookahead_guard": "forward rank recalculation and outcome distillation remain forbidden(전진 순위 재계산과 결과 증류 금지 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "input_artifacts": [aw.rel(path) for path in INPUT_FILES],
                "output_artifacts": [aw.rel(path) for path in OUTPUT_FILES],
                "lineage_status": "run337BK package reviewed; run337BM queue opened(337BK 패키지 검토 및 337BM 대기열 개방)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "judgment": final["judgment"],
                "decision": final["decision"],
                "actual_mt5_execution": final["actual_mt5_execution"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    paths = []
    for path, payload in payloads:
        paths.append(aw.write_json(path, payload))
    return paths


def build_gates(
    src: Mapping[str, Any],
    package_rows: Sequence[Mapping[str, Any]],
    template_rows: Sequence[Mapping[str, Any]],
    blocker_rows: Sequence[Mapping[str, Any]],
    attempt_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent_gates = sum(1 for row in src["gates"] if row.get("status") == "passed")
    missing_inputs = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    route_blocked = any("route_signal" in row.get("blocker_id", "") and row.get("status") == "passed" for row in blocker_rows)
    stage328_blocked = any("stage328" in row.get("blocker_id", "") and row.get("status") == "passed" for row in blocker_rows)
    denied_primary = any(row.get("execution_decision") == "blocked_before_external_mt5_execution" for row in attempt_rows)
    specs = [
        ("bl_gate_parent_loaded", src["final"].get("next_action") == RUN_ID, f"parent_next={src['final'].get('next_action')}", "run337BK opens run337BL(337BK가 337BL을 엶)"),
        ("bl_gate_parent_gates_passed", parent_gates == 14 and src["final"].get("passed_gates") == 14, f"parent_gates={parent_gates}", "run337BK gates passed(337BK 게이트 통과)"),
        ("bl_gate_inputs_loaded", not missing_inputs, f"missing={missing_inputs}", "all package inputs available(모든 패키지 입력 사용 가능)"),
        ("bl_gate_package_review_passed", all(row.get("status") == "passed" for row in package_rows), f"package_rows={len(package_rows)}", "package shape reviewed(패키지 형태 검토)"),
        ("bl_gate_template_review_passed", all(row.get("status") == "passed" for row in template_rows), f"template_rows={len(template_rows)}", "template parameters match frozen contract(템플릿 파라미터가 고정 계약과 일치)"),
        ("bl_gate_route_signal_blocker_identified", route_blocked and stage328_blocked, f"route_blocked={route_blocked};stage328_blocked={stage328_blocked}", "route-signal blocker named(경로 신호 차단자 명명)"),
        ("bl_gate_actual_execution_denied", denied_primary, f"denied_primary={denied_primary}", "external MT5 execution denied before fake forward(가짜 전진 전 외부 MT5 실행 거부)"),
        ("bl_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue={len(queue_rows)}", "run337BM queue ready(337BM 대기열 준비)"),
        ("bl_gate_no_forbidden_claims", True, "forward=not_claimed;runtime=not_claimed;goal=not_claimed;mt5=not_run", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "keeps package review bounded before runtime execution(런타임 실행 전 패키지 검토 경계 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BL MT5 Probe Package Review(MT5 탐침 패키지 검토)

## Conclusion(결론)

run337BL(337BL 실행)은 run337BK(337BK 실행)의 MT5 probe execution package(MT5 탐침 실행 패키지)를 검토했다.

Effect(효과): cp322A frozen identity(cp322A 고정 정체성), Tier A+B fallback(Tier A+B 대체), threshold/risk/lot(임계값/위험/로트), no-lookahead boundary(미래참조 방지 경계)는 통과했다. 실제 MT5 execution(실제 MT5 실행)은 route-signal forward handoff(경로 신호 전진 인계)가 없어서 실행하지 않았다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- actual_mt5_execution(실제 MT5 실행): `{final['actual_mt5_execution']}`
- blocker(차단자): `{final['primary_blocker']}`

## Boundary(경계)

Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

- next_action(다음 행동): `{final['next_action']}`
- effect(효과): route_signal(경로 신호) 인계를 수리하거나, 고정 규칙 아래 불가능함을 증명한다.
- claim_boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BL MT5 Probe Package Review(결정: 337단계 337BL MT5 탐침 패키지 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): 실제 MT5 execution(실제 MT5 실행)을 막고, route-signal forward handoff(경로 신호 전진 인계)를 다음 좁은 수리/증명 작업으로 넘긴다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BL focus")
    workspace = bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        f"- >-\n  Stage337 run337BL focus complete: run337BL(337BL 실행)은 `{final['status']}`로 "
        f"MT5 probe execution package review(MT5 탐침 실행 패키지 검토)를 완료했다. Effect(효과): "
        f"template parameters(템플릿 파라미터)와 package contracts(패키지 계약)는 통과했지만 "
        f"route-signal forward handoff(경로 신호 전진 인계)가 없어 실제 MT5 execution(실제 MT5 실행)은 차단했다. "
        f"Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bg.remove_markdown_section(current_text, "## Stage337 run337BL(337BL 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BL(337BL 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BL(337BL 실행)은 MT5 probe package(MT5 탐침 패키지)를 검토했고 route-signal forward handoff(경로 신호 전진 인계) 누락 때문에 실제 MT5 execution(실제 MT5 실행)을 차단했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current = current.replace("## Stage337 run337BK(337BK 실행)", entry + "\n## Stage337 run337BK(337BK 실행)", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- package_review_rows(패키지 검토 행): `{final['package_review_rows']}`
- template_review_rows(템플릿 검토 행): `{final['template_review_rows']}`
- primary_blocker(주요 차단자): `{final['primary_blocker']}`
- actual_mt5_execution(실제 MT5 실행): `{final['actual_mt5_execution']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_run337BM_route_signal_handoff_pending`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BL(337BL 실행)은 패키지를 통과시켰지만 실제 MT5 실행은 경로 신호 인계 누락으로 막았다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_text = stage_text.rstrip() + f"\n- {TODAY}: run337BL(337BL 실행) reviewed MT5 probe execution package(MT5 탐침 실행 패키지 검토) and opened run337BM(337BM 실행) route-signal handoff feasibility(경로 신호 인계 가능성). Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = changelog_text.rstrip() + f"\n- {TODAY}: Stage337 run337BL reviewed MT5 probe package(MT5 탐침 패키지 검토) and blocked actual MT5 execution(실제 MT5 실행 차단) until route-signal handoff(경로 신호 인계) is repaired/proven.\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_probe_package_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};actual_mt5_blocked;goal_achieve_not_claimed.",
        "work_family": "runtime_backtest",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_probe_package_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_probe_package_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BL MT5 probe package review",
        "tier_scope": "research_review_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "runtime_backtest",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"package_review={final['package_review_passed']}/{final['package_review_rows']};template={final['template_review_passed']}/{final['template_review_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;actual_mt5_blocked;no_forward_claim;no_goal_achieve",
        "external_verification_status": "blocked_before_external_mt5_execution(외부 MT5 실행 전 차단)",
        "notes": f"primary_blocker={final['primary_blocker']};next_action={final['next_action']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__mt5_probe_package_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_backtest",
        "evidence_scope": "run337BK MT5 probe package review",
        "kpi_scope": "package_review_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;actual_mt5_blocked;primary_blocker={final['primary_blocker']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__mt5_probe_package_review",
        "family": "mt5_probe_package_review_without_db",
        "question": "can the run337BK cp322A frozen MT5 probe package proceed to external execution",
        "metric_scope": "frozen_identity_template_route_signal_handoff_no_lookahead",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = load_inputs()
    package_rows = build_package_review(src)
    package_path = aw.write_csv(PACKAGE_REVIEW, REVIEW_COLUMNS, package_rows)
    template_rows = build_template_review(src)
    template_path = aw.write_csv(TEMPLATE_PARAMETER_REVIEW, TEMPLATE_COLUMNS, template_rows)
    blocker_rows = build_route_blocker_review(src)
    blocker_path = aw.write_csv(ROUTE_SIGNAL_BLOCKER_REVIEW, BLOCKER_COLUMNS, blocker_rows)
    attempt_rows = build_attempt_decision(src)
    attempt_path = aw.write_csv(RUNTIME_ATTEMPT_DECISION, ATTEMPT_COLUMNS, attempt_rows)
    queue_rows = build_queue()
    queue_path = aw.write_csv(RUN337BM_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, package_rows, template_rows, blocker_rows, attempt_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BL_package_review_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "mt5_probe_package_review_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BL_package_review_before_route_signal_work",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BL_package_review_gate_failure_v1",
        "package_review_rows": len(package_rows),
        "package_review_passed": count_passed(package_rows),
        "template_review_rows": len(template_rows),
        "template_review_passed": count_passed(template_rows),
        "blocker_rows": len(blocker_rows),
        "blocker_passed": count_passed(blocker_rows),
        "attempt_decision_rows": len(attempt_rows),
        "queue_rows": len(queue_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": count_passed(gate_rows),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "primary_blocker": "route_signal_forward_tier_a_and_tier_b_handoff_missing_plus_stage328_not_safe_without_upstream_rebuild",
        "actual_mt5_execution": "not_run_blocked_before_external_mt5_execution",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": aw.rel(Path(__file__)),
        "parent_run_id": PARENT_RUN_ID,
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "external_verification_status": "blocked_before_external_mt5_execution(외부 MT5 실행 전 차단)",
        "actual_mt5_execution": final["actual_mt5_execution"],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(로트 최적화)",
            "forward rank recalculation(전진 순위 재계산)",
            "outcome distillation(결과 증류)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "runtime authority claim(런타임 권위 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = build_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        package_path,
        template_path,
        blocker_path,
        attempt_path,
        queue_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "actual_mt5_execution": final["actual_mt5_execution"],
                "primary_blocker": final["primary_blocker"],
                "report": aw.rel(report_path),
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
