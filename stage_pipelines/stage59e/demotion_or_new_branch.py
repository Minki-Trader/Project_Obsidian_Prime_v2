from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


REPO_ROOT = Path(__file__).resolve().parents[2]

STAGE_ID = "59E_adapter_repair__demotion_or_new_branch"
STAGE_ROOT = Path("stages") / STAGE_ID
REVIEW_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

SOURCE_STAGE_ID = "59D_adapter_repair__source_lifecycle_or_demote"
SOURCE_REVIEW_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_REVIEW_ROOT / "source_lifecycle_or_demote_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEW_ROOT / "source_lifecycle_or_demote_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEW_ROOT / "source_lifecycle_or_demote_risk_atr_telemetry.csv"
SOURCE_DECISION = SOURCE_REVIEW_ROOT / "stage59d_decision.md"
SOURCE_REPORT = SOURCE_REVIEW_ROOT / "source_lifecycle_or_demote_report.md"

NEXT_STAGE_ID = "59F_adapter_repair__new_model_branch_from_failure_memory"
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

PACKET_ID = "stage59e_demotion_or_new_branch_v1"
RUN_ID = "run58A_stage59e_demotion_or_new_branch_v1"
NEXT_PACKET_ID = "stage59f_new_model_branch_from_failure_memory_v1"
NEXT_RUN_ID = "run59A_stage59f_new_model_branch_from_failure_memory_v1"

SOURCE_ADAPTER = "ba14_no_atr_sd5_lot025"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
SOURCE_STAGE59D_PUSHED_COMMIT = "d508f35bc5910eb9ff594bc49b2b25432fd6df58"

BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "open_new_model_branch"
ROUTE_ACTION = "demote_current_adapter_and_open_stage59f_new_model_branch"
EXTERNAL_STATUS = "completed_existing_stage59d_mt5_evidence_integrated"

SUMMARY_JSON = REVIEW_ROOT / "demotion_or_new_branch_summary.json"
SUMMARY_CSV = REVIEW_ROOT / "demotion_or_new_branch_summary.csv"
REPORT_MD = REVIEW_ROOT / "demotion_or_new_branch_report.md"
DECISION_MD = REVIEW_ROOT / "stage59e_decision.md"
STAGE_LEDGER = REVIEW_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")
CHANGELOG = Path("docs/workspace/changelog.md")
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID

FORBIDDEN_CLAIMS = {
    "deployment": False,
    "live_readiness": False,
    "production_baseline": False,
    "operating_promotion": False,
    "operating_reference": False,
    "runtime_authority": False,
    "overall_goal_complete": False,
}


def io_path(path: Path | str) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return REPO_ROOT / candidate


def rel(path: Path | str) -> str:
    candidate = Path(path)
    try:
        return io_path(candidate).resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    existing: list[dict[str, str]] = []
    target = io_path(path)
    if target.exists():
        with target.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            existing = [dict(row) for row in reader if row.get(key) not in {str(new.get(key)) for new in rows}]
    merged = existing + [{column: csv_value(row.get(column)) for column in columns} for row in rows]
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_key(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", rel(path)).strip("_")


def replace_artifact_rows(rows: Sequence[Mapping[str, Any]]) -> None:
    columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"]
    target = io_path(ARTIFACT_REGISTRY)
    existing: list[dict[str, str]] = []
    if target.exists():
        with target.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            existing = [
                dict(row)
                for row in reader
                if not (row.get("stage_id") == STAGE_ID and row.get("run_id") == RUN_ID)
            ]
    merged = existing + [{column: csv_value(row.get(column)) for column in columns} for row in rows]
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(merged)


def number(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


def by_adapter_split(summary_rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, Mapping[str, str]]]:
    grouped: dict[str, dict[str, Mapping[str, str]]] = defaultdict(dict)
    for row in summary_rows:
        if row.get("view") != "actual_routed_total":
            continue
        if row.get("status") != "completed":
            continue
        split = row.get("split", "")
        if split not in {"validation_is", "oos"}:
            continue
        grouped[row.get("adapter_id", "unknown")][split] = row
    return grouped


def segment_flags(segment_rows: Sequence[Mapping[str, str]], adapter_id: str) -> list[str]:
    flags: list[str] = []
    for row in segment_rows:
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("view") != "actual_routed_total":
            continue
        flag = row.get("quality_flag", "")
        if flag and flag != "acceptable_measurement_only":
            flags.extend(part for part in flag.split(";") if part)
    return sorted(set(flags))


def classify_adapter(adapter_id: str, validation: Mapping[str, str], oos: Mapping[str, str], flags: Sequence[str]) -> tuple[str, list[str]]:
    validation_net = number(validation.get("net_profit")) or 0.0
    validation_pf = number(validation.get("profit_factor")) or 0.0
    validation_cost = number(validation.get("cost_stressed_expectancy")) or 0.0
    validation_dd = number(validation.get("max_drawdown_amount")) or 0.0
    oos_net = number(oos.get("net_profit")) or 0.0
    oos_pf = number(oos.get("profit_factor")) or 0.0
    oos_cost = number(oos.get("cost_stressed_expectancy")) or 0.0
    oos_dd = number(oos.get("max_drawdown_amount")) or 0.0

    reasons: list[str] = []
    if validation_net <= 0:
        reasons.append("validation_net_not_positive")
    if validation_pf < 1.10:
        reasons.append("validation_pf_lt_1_10")
    if validation_cost <= 0:
        reasons.append("validation_cost_stressed_expectancy_not_positive")
    if oos_net <= 0:
        reasons.append("oos_net_not_positive")
    if oos_pf < 1.10:
        reasons.append("oos_pf_lt_1_10")
    if oos_cost <= 0:
        reasons.append("oos_cost_stressed_expectancy_not_positive")
    if flags:
        reasons.append("segment_flags_present")
    if adapter_id.endswith("hold3_thr57_mr03_wideatr_sd5") and oos_net > 1000 and validation_net <= 0:
        reasons.append("oos_spike_or_late_concentration_risk")
    if oos_dd >= 500:
        reasons.append("oos_drawdown_too_large_for_hardening")
    if validation_dd >= 300:
        reasons.append("validation_drawdown_not_controlled")

    if adapter_id.endswith("closeonlyopp_thr57_mr03_wideatr_sd5"):
        signal = "best_balanced_failure_memory"
    elif adapter_id.endswith("hold3_thr57_mr03_wideatr_sd5"):
        signal = "oos_spike_risk_failure_memory"
    elif not reasons:
        signal = "would_be_stage60_candidate"
    else:
        signal = "demotion_evidence"
    return signal, reasons


def build_summary_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    source_rows = read_csv(SOURCE_SUMMARY)
    segment_rows = read_csv(SOURCE_SEGMENTS)
    grouped = by_adapter_split(source_rows)
    rows: list[dict[str, Any]] = []
    for adapter_id in sorted(grouped):
        validation = grouped[adapter_id].get("validation_is")
        oos = grouped[adapter_id].get("oos")
        if not validation or not oos:
            continue
        flags = segment_flags(segment_rows, adapter_id)
        signal, reasons = classify_adapter(adapter_id, validation, oos, flags)
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": validation.get("run_id", ""),
                "adapter_id": adapter_id,
                "validation_net": number(validation.get("net_profit")),
                "validation_pf": number(validation.get("profit_factor")),
                "validation_cost_stressed_expectancy": number(validation.get("cost_stressed_expectancy")),
                "validation_drawdown": number(validation.get("max_drawdown_amount")),
                "oos_net": number(oos.get("net_profit")),
                "oos_pf": number(oos.get("profit_factor")),
                "oos_cost_stressed_expectancy": number(oos.get("cost_stressed_expectancy")),
                "oos_drawdown": number(oos.get("max_drawdown_amount")),
                "validation_segment_flags": ";".join(flag for flag in flags if flag.startswith("validation")),
                "all_segment_flags": ";".join(flags),
                "model_risk_enabled": validation.get("model_risk_enabled"),
                "atr_enabled": validation.get("atr_enabled"),
                "risk_floor_applied_count_validation": number(validation.get("risk_floor_applied_count")),
                "risk_floor_applied_count_oos": number(oos.get("risk_floor_applied_count")),
                "decision_signal": signal,
                "demotion_reason": ";".join(reasons),
            }
        )

    closeonly = next((row for row in rows if row["decision_signal"] == "best_balanced_failure_memory"), None)
    hold3 = next((row for row in rows if row["decision_signal"] == "oos_spike_risk_failure_memory"), None)
    decision_payload = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_stage59d_pushed_commit": SOURCE_STAGE59D_PUSHED_COMMIT,
        "source_adapter": SOURCE_ADAPTER,
        "decision": DECISION,
        "route_action": ROUTE_ACTION,
        "current_adapter_disposition": "demoted_adapter",
        "best_balanced_failure_memory": closeonly["adapter_id"] if closeonly else None,
        "oos_spike_risk_failure_memory": hold3["adapter_id"] if hold3 else None,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "next_packet_id": NEXT_PACKET_ID,
        "next_run_id": NEXT_RUN_ID,
        "external_verification_status": EXTERNAL_STATUS,
        "overall_goal_complete": False,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "reason": [
            "Stage59D lifecycle variants did not produce a validation-strong full adapter.",
            "ATR SL/TP and model-controlled risk% are present in evidence, but validation cost-stressed behavior remains weak.",
            "Stage60 ONNX hardening is blocked until a post-risk/ATR adapter is genuinely strong.",
        ],
    }
    return rows, decision_payload


def write_reports(rows: Sequence[Mapping[str, Any]], decision_payload: Mapping[str, Any]) -> None:
    columns = [
        "run_id",
        "source_run_id",
        "adapter_id",
        "validation_net",
        "validation_pf",
        "validation_cost_stressed_expectancy",
        "validation_drawdown",
        "oos_net",
        "oos_pf",
        "oos_cost_stressed_expectancy",
        "oos_drawdown",
        "model_risk_enabled",
        "atr_enabled",
        "risk_floor_applied_count_validation",
        "risk_floor_applied_count_oos",
        "decision_signal",
        "demotion_reason",
        "all_segment_flags",
    ]
    write_csv(SUMMARY_CSV, rows, columns)
    write_json(
        SUMMARY_JSON,
        {
            **decision_payload,
            "summary_rows": list(rows),
            "required_input_paths": {
                "source_summary": rel(SOURCE_SUMMARY),
                "source_segment_kpi": rel(SOURCE_SEGMENTS),
                "source_risk_atr_telemetry": rel(SOURCE_RISK_ATR),
                "source_decision": rel(SOURCE_DECISION),
            },
        },
    )

    best_memory = decision_payload.get("best_balanced_failure_memory") or "none"
    spike_memory = decision_payload.get("oos_spike_risk_failure_memory") or "none"
    row_lines = []
    for row in rows:
        row_lines.append(
            "- adapter(어댑터) `{adapter}`: validation PF(검증 수익 팩터) `{vpf:.2f}`, "
            "validation net(검증 순손익) `{vnet:.2f}`, OOS PF(표본외 수익 팩터) `{opf:.2f}`, "
            "OOS net(표본외 순손익) `{onet:.2f}`, signal(신호) `{signal}`".format(
                adapter=row["adapter_id"],
                vpf=row["validation_pf"] or 0.0,
                vnet=row["validation_net"] or 0.0,
                opf=row["oos_pf"] or 0.0,
                onet=row["oos_net"] or 0.0,
                signal=row["decision_signal"],
            )
        )
    write_md(
        REPORT_MD,
        f"""# Stage59E Demotion Or New Branch Report(59E단계 강등 또는 새 분기 보고서)

- stage_id(단계 ID): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- bounded_question(경계 질문): `Should the current adapter be demoted or replaced by a new bounded model branch after Stage59D?`
- decision(판정): `{DECISION}`
- route_action(라우팅 행동): `{ROUTE_ACTION}`
- current_adapter_disposition(현재 어댑터 처리): `demoted_adapter`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage59E(59E단계)는 Stage59D(59D단계) 결과를 decision gate(판정 게이트)로 묶었다. Effect(효과): 약한 validation(검증) 상태에서 Stage60 ONNX hardening(60단계 ONNX 경화)으로 넘어가지 않는다.

## Evidence Read(근거 읽기)

{chr(10).join(row_lines)}

## Decision Basis(판정 근거)

- best_balanced_failure_memory(최선 균형 실패 기억): `{best_memory}`
- oos_spike_risk_failure_memory(표본외 급등 위험 실패 기억): `{spike_memory}`
- mandatory_capabilities(필수 능력): ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)는 Stage59D(59D단계) 근거 안에 있었지만 sufficient condition(충분 조건)이 아니다.
- hardening_gate(경화 게이트): validation PF/cost/equity(검증 수익 팩터/비용/자금 곡선)가 약해서 Stage60 ONNX(60단계 ONNX)는 열지 않는다.

## Result Judgment(결과 판정)

판정(decision, 판정)은 `{DECISION}`이다. Effect(효과): 현재 adapter(어댑터)는 demoted_adapter(강등 어댑터)로 보존하고, Stage59F(59F단계)에서 failure memory(실패 기억)를 입력으로 새 bounded model branch(경계 모델 분기)를 연다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
""",
    )
    write_md(
        DECISION_MD,
        f"""# Stage59E Decision(59E단계 판정)

decision(판정): `{DECISION}`

Stage59E(59E단계)는 current adapter(현재 어댑터) `ba14_no_atr_sd5_lot025` 계열을 active repair path(활성 수리 경로)에서 demote(강등)하고 Stage59F(59F단계) new model branch(새 모델 분기)를 연다. Effect(효과): Stage60 ONNX hardening(60단계 ONNX 경화)은 아직 시작하지 않는다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_MD)}`
- summary_json(요약 JSON): `{rel(SUMMARY_JSON)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV)}`
- source_stage59d_decision(원천 59D단계 판정): `{rel(SOURCE_DECISION)}`
- source_stage59d_pushed_commit(원천 59D단계 푸시 커밋): `{SOURCE_STAGE59D_PUSHED_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`

## Reason(이유)

- Stage59D(59D단계) best(최선) `s59d_v64_hold3_thr57_mr03_wideatr_sd5`는 OOS(표본외)가 강했지만 validation net/PF/cost(검증 순손익/수익 팩터/비용)가 약했다.
- `s59d_v64_closeonlyopp_thr57_mr03_wideatr_sd5`는 best_balanced_failure_memory(최선 균형 실패 기억)로 보존하지만 validation cost(검증 비용)가 음수라 hardening candidate(경화 후보)가 아니다.
- ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험률)는 necessary condition(필요 조건)이지만 sufficient condition(충분 조건)이 아니다.

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage59E closeout(59E단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): research-grade BaselineAdapter package(연구급 기준선 어댑터 패키지)는 계속 미완료 상태로 남는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
""",
    )


def write_stage_and_next_docs() -> None:
    write_md(
        REVIEW_ROOT / "review_index.md",
        f"""# Stage59E Review Index(59E단계 검토 색인)

- demotion_or_new_branch_report(강등 또는 새 분기 보고서): `{rel(REPORT_MD)}`
- demotion_or_new_branch_summary_json(강등 또는 새 분기 요약 JSON): `{rel(SUMMARY_JSON)}`
- demotion_or_new_branch_summary_csv(강등 또는 새 분기 요약 CSV): `{rel(SUMMARY_CSV)}`
- stage59e_decision(59E단계 판정): `{rel(DECISION_MD)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE_LEDGER)}`

Effect(효과): Stage59E(59E단계) closeout(종료) 근거를 한 위치에서 확인한다.
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage59E Selection Status(59E단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_demotion_or_new_branch`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- stage59e_decision(59E단계 판정): `{DECISION}`
- route_action(라우팅 행동): `{ROUTE_ACTION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): current adapter(현재 어댑터)는 demoted_adapter(강등 어댑터)로 기록되고 Stage60 ONNX(60단계 ONNX)는 열리지 않는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# Stage59F Brief(59F단계 개요)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- bounded_question(경계 질문): `Can a new bounded model branch, informed by Stage59D/59E failure memory, produce a post-ATR/risk adapter candidate without starting ONNX?`
- boundary(경계): `{BOUNDARY}`

Stage59F(59F단계)는 new model branch(새 모델 분기)만 다룬다. Effect(효과): Stage59D(59D단계)의 close-only-on-opposite(반대 신호에서만 청산) 단서와 hold3(3봉 보유) 급등 위험을 failure memory(실패 기억)로 쓰되, Stage60 ONNX(60단계 ONNX)나 deployment(배포)로 넘어가지 않는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage59F Input References(59F단계 입력 참조)

- stage59e_decision(59E단계 판정): `{rel(DECISION_MD)}`
- stage59e_report(59E단계 보고서): `{rel(REPORT_MD)}`
- stage59e_summary(59E단계 요약): `{rel(SUMMARY_CSV)}`
- stage59d_summary(59D단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage59d_segment_kpi(59D단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage59d_risk_atr_telemetry(59D단계 위험/ATR 원격측정): `{rel(SOURCE_RISK_ATR)}`

Effect(효과): Stage59F(59F단계)는 실패 기억(failure memory, 실패 기억)을 숨기지 않고 새 branch(분기)의 입력으로 사용한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage59F Review Index(59F단계 검토 색인)

Stage59F(59F단계)는 active_planned(활성 계획) 상태다. Effect(효과): 새 모델 분기(new model branch, 새 모델 분기)의 산출물은 이 색인에 추가된다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage59F Selection Status(59F단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59e`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): 다음 작업은 Stage59F(59F단계) 안에서만 bounded(경계)로 진행된다.
""",
    )


def write_ledgers(rows: Sequence[Mapping[str, Any]], decision_payload: Mapping[str, Any]) -> None:
    best_memory = decision_payload.get("best_balanced_failure_memory") or "none"
    spike_memory = decision_payload.get("oos_spike_risk_failure_memory") or "none"
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__aggregate_demotion_or_new_branch",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate_demotion_or_new_branch",
            "parent_run_id": "run57A_stage59d_source_lifecycle_or_demote_v1",
            "record_view": "demotion_or_new_branch_decision",
            "tier_scope": "Tier A+B",
            "kpi_scope": "baseline_adapter_repair",
            "scoreboard_lane": "decision_gate",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_MD),
            "primary_kpi": f"decision={DECISION};route_action={ROUTE_ACTION}",
            "guardrail_kpi": (
                f"best_balanced_failure_memory={best_memory};"
                f"oos_spike_risk_failure_memory={spike_memory};"
                "stage60_onnx_opened=0;overall_goal_complete=0"
            ),
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage59E bounded decision gate(경계 판정 게이트); not final package completion(최종 패키지 완료 아님).",
        }
    ]
    ledger_columns = [
        "ledger_row_id",
        "stage_id",
        "run_id",
        "subrun_id",
        "parent_run_id",
        "record_view",
        "tier_scope",
        "kpi_scope",
        "scoreboard_lane",
        "status",
        "judgment",
        "path",
        "primary_kpi",
        "guardrail_kpi",
        "external_verification_status",
        "notes",
    ]
    write_csv(STAGE_LEDGER, ledger_rows, ledger_columns)
    upsert_csv(PROJECT_LEDGER, ledger_columns, ledger_rows, key="ledger_row_id")

    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_demotion_or_new_branch",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_MD),
            "notes": (
                f"source_adapter={SOURCE_ADAPTER};disposition=demoted_adapter;"
                f"best_balanced_failure_memory={best_memory};next_stage={NEXT_STAGE_ID};boundary={BOUNDARY}"
            ),
        }
    ]
    upsert_csv(RUN_REGISTRY, ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"], run_rows, key="run_id")


def write_packet_files(decision_payload: Mapping[str, Any]) -> None:
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-artifact-lineage", "obsidian-reentry-read"],
            "decision": DECISION,
            "route_action": ROUTE_ACTION,
            "effect": "Stage59D evidence is converted into a bounded demotion/new-branch handoff.",
        },
    )
    write_json(
        PACKET_ROOT / "experiment_design_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "work_type": "decision_gate_no_new_experiment",
            "bounded_question": "Should the current adapter be demoted or replaced by a new bounded model branch after Stage59D?",
            "new_mt5_run": False,
            "effect": "No open-ended tuning is added inside Stage59E.",
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "external_verification_status": EXTERNAL_STATUS,
            "source_runtime_stage": SOURCE_STAGE_ID,
            "new_runtime_execution": False,
            "effect": "Existing Stage59D MT5 runtime evidence is referenced without claiming new runtime authority.",
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "source_summary": rel(SOURCE_SUMMARY),
            "source_segments": rel(SOURCE_SEGMENTS),
            "source_risk_atr": rel(SOURCE_RISK_ATR),
            "validation_oos_rows_present": True,
            "mandatory_risk_atr_evidence_present": True,
            "effect": "The decision uses segmented KPI and risk/ATR evidence, not final net alone.",
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            **decision_payload,
            "judgment_boundary": "research_development_only",
            "stage60_onnx_allowed": False,
            "effect": "The current adapter is demoted and a new bounded model branch is opened.",
        },
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "overall_goal_complete": False,
            "effect": "Stage59E closeout cannot be misread as final package completion.",
        },
    )


def write_artifact_lineage_and_registry() -> None:
    stage_outputs = [
        REPORT_MD,
        SUMMARY_JSON,
        SUMMARY_CSV,
        DECISION_MD,
        STAGE_LEDGER,
        REVIEW_ROOT / "review_index.md",
        SELECTED_ROOT / "selection_status.md",
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
    ]
    packet_outputs = [
        PACKET_ROOT / "routing_receipt.json",
        PACKET_ROOT / "experiment_design_receipt.json",
        PACKET_ROOT / "runtime_evidence_gate.json",
        PACKET_ROOT / "kpi_contract_audit.json",
        PACKET_ROOT / "result_judgment_gate.json",
        PACKET_ROOT / "final_claim_guard.json",
    ]
    lineage_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_artifacts": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_DECISION)],
        "created_artifacts": [
            {"path": rel(path), "sha256": sha256_file(path)} for path in stage_outputs + packet_outputs
        ],
        "effect": "Stage59E preserves the handoff from Stage59D to Stage59F with hashes.",
    }
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", lineage_payload)
    write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "required_gates": [
                "routing_receipt",
                "experiment_design_receipt",
                "runtime_evidence_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
            ],
            "coverage": "complete",
            "effect": "Closeout claims are tied to actual packet receipts.",
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "route_action": ROUTE_ACTION,
            "next_stage_or_branch": NEXT_STAGE_ID,
            "external_verification_status": EXTERNAL_STATUS,
            "overall_goal_complete": False,
            "required_outputs": {
                "demotion_or_new_branch_report": rel(REPORT_MD),
                "demotion_or_new_branch_summary_json": rel(SUMMARY_JSON),
                "demotion_or_new_branch_summary_csv": rel(SUMMARY_CSV),
                "stage59e_decision": rel(DECISION_MD),
                "stage_run_ledger": rel(STAGE_LEDGER),
            },
        },
    )

    all_outputs = stage_outputs + packet_outputs + [
        PACKET_ROOT / "artifact_lineage_audit.json",
        PACKET_ROOT / "required_gate_coverage_audit.json",
        PACKET_ROOT / "aggregate_summary.json",
    ]
    timestamp = now_utc()
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{artifact_key(path)}",
            "artifact_type": "stage59e_demotion_or_new_branch_evidence",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": timestamp,
            "notes": "Stage59E bounded demotion or new branch artifact.",
        }
        for path in all_outputs
    ]
    replace_artifact_rows(artifact_rows)


def update_current_truth() -> None:
    write_md(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER}`
- status(상태): `stage59e_closed_{DECISION}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59E(59E단계) closed(종료) as bounded demotion or new branch gate(경계 강등 또는 새 분기 게이트). Effect(효과): current adapter(현재 어댑터)는 demoted_adapter(강등 어댑터)로 보존하고 Stage59F(59F단계) new model branch(새 모델 분기)를 active/planned(활성/계획) 상태로 연다.

## Latest Stage59E Evidence(최신 59E단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- route_action(라우팅 행동): `{ROUTE_ACTION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- report(보고서): `{rel(REPORT_MD)}`
- stage59e_decision(59E단계 판정): `{rel(DECISION_MD)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )

    state_path = io_path(WORKSPACE_STATE)
    text = state_path.read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus_insert = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage59E(59E단계) `{STAGE_ID}` closed(종료) as bounded demotion or new branch gate(경계 강등 또는 새 분기 게이트); decision(판정)=`{DECISION}`. "
        f"Effect(효과): current adapter(현재 어댑터)는 demoted_adapter(강등 어댑터)로 보존되고 Stage60 ONNX(60단계 ONNX)는 열리지 않는다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{NEXT_STAGE_ID}` is active/planned(활성/계획). Effect(효과): Stage59D/59E(59D/59E단계) failure memory(실패 기억)를 새 bounded model branch(경계 모델 분기)의 입력으로 넘긴다.\n"
    )
    text = re.sub(r"current_focus:\n", focus_insert, text, count=1)
    block = f"""

stage59e_demotion_or_new_branch:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_bounded_demotion_or_new_branch
  current_run_id: {RUN_ID}
  source_adapter: {SOURCE_ADAPTER}
  source_stage59d_pushed_commit: {SOURCE_STAGE59D_PUSHED_COMMIT}
  decision: {DECISION}
  route_action: {ROUTE_ACTION}
  current_adapter_disposition: demoted_adapter
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_MD)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  boundary: {BOUNDARY}
"""
    if "stage59e_demotion_or_new_branch:" in text:
        text = re.sub(r"\nstage59e_demotion_or_new_branch:\n(?:  .*\n)*", block, text, count=1)
    else:
        text = text.rstrip() + block
    state_path.write_text(text, encoding="utf-8-sig")


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-15 - Stage59E demotion or new branch closeout(59E단계 강등 또는 새 분기 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        f"- effect(효과): Stage59D(59D단계)의 validation weakness(검증 약점)를 숨기지 않고 current adapter(현재 어댑터)를 demoted_adapter(강등 어댑터)로 기록한 뒤 Stage59F(59F단계) new model branch(새 모델 분기)를 연다.\n"
    )
    path = io_path(CHANGELOG)
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        path.write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def validate_outputs() -> None:
    required = [
        REPORT_MD,
        SUMMARY_JSON,
        SUMMARY_CSV,
        DECISION_MD,
        STAGE_LEDGER,
        REVIEW_ROOT / "review_index.md",
        SELECTED_ROOT / "selection_status.md",
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        PACKET_ROOT / "aggregate_summary.json",
        CURRENT_WORKING_STATE,
        WORKSPACE_STATE,
    ]
    missing = [rel(path) for path in required if not io_path(path).exists()]
    if missing:
        raise FileNotFoundError(f"missing Stage59E outputs: {missing}")
    final_guard = json.loads(io_path(PACKET_ROOT / "final_claim_guard.json").read_text(encoding="utf-8"))
    if final_guard.get("overall_goal_complete") is not False:
        raise RuntimeError("final claim guard failed: overall_goal_complete must be false")
    if any(final_guard.get("forbidden_claims", {}).values()):
        raise RuntimeError("final claim guard failed: forbidden claim flag is true")


def run() -> dict[str, Any]:
    rows, decision_payload = build_summary_rows()
    write_reports(rows, decision_payload)
    write_stage_and_next_docs()
    write_ledgers(rows, decision_payload)
    write_packet_files(decision_payload)
    write_artifact_lineage_and_registry()
    update_current_truth()
    append_changelog()
    validate_outputs()
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "decision": DECISION,
        "route_action": ROUTE_ACTION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "overall_goal_complete": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Close Stage59E demotion/new branch decision gate.")
    parser.add_argument("--json", action="store_true", help="Print result as JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = run()
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            f"{payload['stage_id']} decision={payload['decision']} "
            f"next={payload['next_stage_or_branch']} overall_goal_complete={payload['overall_goal_complete']}"
        )


if __name__ == "__main__":
    main()
