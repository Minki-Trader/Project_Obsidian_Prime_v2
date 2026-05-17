from __future__ import annotations

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "69_adapter_research__branch_or_candidate_review"
RUN_ID = "run69A_stage69_branch_or_candidate_review_v1"
RUN_NUMBER = "run69A"
PACKET_ID = "stage69_branch_or_candidate_review_v1"
PARENT_RUN_ID = "run68A_stage68_dd_net_balance_repair_v1"
SOURCE_STAGE68_COMMIT = "7ebe1fcfb05fbcd9df60007ca5b8050230a4d0f3"
NEXT_STAGE_ID = "70_adapter_research__new_model_branch_from_short_gate_limit"
NEXT_RUN_ID = "run70A_stage70_new_model_branch_from_short_gate_limit_v1"
NEXT_PACKET_ID = "stage70_new_model_branch_from_short_gate_limit_v1"
SOURCE_ADAPTER_ID = "s62_v41_sd8_h5"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "open_new_model_branch_in_stage70"
EXTERNAL = "not_applicable"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

STAGE66_SUMMARY = Path("stages/66_adapter_research__soft_gate_kpi_repair/03_reviews/stage66_soft_gate_kpi_summary.csv")
STAGE67_SUMMARY = Path("stages/67_adapter_research__short_gate_net_scale_review/03_reviews/stage67_short_gate_net_scale_summary.csv")
STAGE68_SUMMARY = Path("stages/68_adapter_research__dd_net_balance_repair/03_reviews/stage68_dd_net_balance_summary.csv")
SUMMARY_CSV = REVIEWS_ROOT / "stage69_branch_candidate_review.csv"
REPORT_MD = REVIEWS_ROOT / "stage69_branch_candidate_report.md"
DECISION_MD = REVIEWS_ROOT / "stage69_decision.md"
STAGE_LEDGER = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
PACKET_SUMMARY = PACKET_ROOT / "aggregate_summary.json"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")
CHANGELOG = Path("docs/workspace/changelog.md")

LATEST_TARGET = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
EXTENDED_TARGET = {
    "profit_factor": 1.302494,
    "net_profit": 2950.79,
    "max_drawdown_percent": 18.760867,
    "trade_count": 1134,
}


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def read_rows(path: Path, stage_label: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("view") != "actual_routed_total" or row.get("status") != "completed":
                continue
            rows.append(
                {
                    "stage_label": stage_label,
                    "adapter_id": row.get("adapter_id", ""),
                    "split": row.get("split", ""),
                    "profit_factor": float(row.get("profit_factor") or 0.0),
                    "net_profit": float(row.get("net_profit") or 0.0),
                    "max_drawdown_percent": float(row.get("max_drawdown_percent") or 0.0),
                    "expectancy": float(row.get("expectancy") or 0.0),
                    "trade_count": int(float(row.get("trade_count") or 0.0)),
                    "cost_stressed_expectancy": float(row.get("cost_stressed_expectancy") or 0.0),
                }
            )
    return rows


def grouped(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Mapping[str, Any]]]:
    groups: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        key = f"{row['stage_label']}::{row['adapter_id']}"
        split = "validation" if row["split"] == "validation_is" else str(row["split"])
        groups.setdefault(key, {})[split] = row
    return groups


def review_rows() -> list[dict[str, Any]]:
    rows = []
    rows.extend(read_rows(STAGE66_SUMMARY, "Stage66"))
    rows.extend(read_rows(STAGE67_SUMMARY, "Stage67"))
    rows.extend(read_rows(STAGE68_SUMMARY, "Stage68"))
    output: list[dict[str, Any]] = []
    for key, splits in grouped(rows).items():
        val = splits.get("validation", {})
        oos = splits.get("oos", {})
        if not val or not oos:
            continue
        val_pf = float(val["profit_factor"])
        oos_pf = float(oos["profit_factor"])
        val_net = float(val["net_profit"])
        oos_net = float(oos["net_profit"])
        val_dd = float(val["max_drawdown_percent"])
        oos_dd = float(oos["max_drawdown_percent"])
        latest_pf_gap = min(val_pf, oos_pf) - LATEST_TARGET["profit_factor"]
        latest_dd_gap = max(val_dd, oos_dd) - LATEST_TARGET["max_drawdown_percent"]
        latest_net_gap = min(val_net, oos_net) - LATEST_TARGET["net_profit"]
        candidate_ready = (
            val_pf >= LATEST_TARGET["profit_factor"]
            and oos_pf >= LATEST_TARGET["profit_factor"]
            and val_net >= LATEST_TARGET["net_profit"]
            and oos_net >= LATEST_TARGET["net_profit"]
            and val_dd <= LATEST_TARGET["max_drawdown_percent"]
            and oos_dd <= LATEST_TARGET["max_drawdown_percent"]
        )
        extended_pf_ok = val_pf >= EXTENDED_TARGET["profit_factor"] and oos_pf >= EXTENDED_TARGET["profit_factor"]
        extended_dd_ok = val_dd <= EXTENDED_TARGET["max_drawdown_percent"] and oos_dd <= EXTENDED_TARGET["max_drawdown_percent"]
        branch_score = min(val_net, oos_net) + 75.0 * min(val_pf, oos_pf) - 12.0 * max(val_dd, oos_dd)
        output.append(
            {
                "candidate_key": key,
                "validation_pf": val_pf,
                "oos_pf": oos_pf,
                "validation_net": val_net,
                "oos_net": oos_net,
                "validation_dd_pct": val_dd,
                "oos_dd_pct": oos_dd,
                "validation_trades": int(val["trade_count"]),
                "oos_trades": int(oos["trade_count"]),
                "latest_pf_gap": latest_pf_gap,
                "latest_net_gap_min_split": latest_net_gap,
                "latest_dd_gap_worst_split": latest_dd_gap,
                "extended_pf_ok": extended_pf_ok,
                "extended_dd_ok": extended_dd_ok,
                "candidate_ready": candidate_ready,
                "branch_score": branch_score,
                "review_read": "branch_limit_observed_open_new_model_branch",
            }
        )
    return sorted(output, key=lambda item: float(item["branch_score"]), reverse=True)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = []
        for row in rows:
            for key in row:
                if key not in columns:
                    columns.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| candidate(후보) | val PF/net/DD(검증 수익 팩터/순손익/손실률) | OOS PF/net/DD(표본외 수익 팩터/순손익/손실률) | latest gap(최신 차이) | read(판독) |",
        "|---|---:|---:|---:|---|",
    ]
    for row in rows[:8]:
        lines.append(
            "| {candidate} | {vpf:.2f}/{vnet:.2f}/{vdd:.2f} | {opf:.2f}/{onet:.2f}/{odd:.2f} | PF {pfgap:.2f}, net {netgap:.2f}, DD {ddgap:.2f} | {read} |".format(
                candidate=row["candidate_key"],
                vpf=float(row["validation_pf"]),
                vnet=float(row["validation_net"]),
                vdd=float(row["validation_dd_pct"]),
                opf=float(row["oos_pf"]),
                onet=float(row["oos_net"]),
                odd=float(row["oos_dd_pct"]),
                pfgap=float(row["latest_pf_gap"]),
                netgap=float(row["latest_net_gap_min_split"]),
                ddgap=float(row["latest_dd_gap_worst_split"]),
                read=row["review_read"],
            )
        )
    return "\n".join(lines)


def build_report(rows: Sequence[Mapping[str, Any]]) -> str:
    best = rows[0] if rows else {}
    return f"""# Stage69 Branch Or Candidate Review(69단계 분기 또는 후보 검토)

- run(실행): `{RUN_ID}`
- source_stage68_pushed_commit(원천 68단계 푸시 커밋): `{SOURCE_STAGE68_COMMIT}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- external_verification_status(외부 검증 상태): `{EXTERNAL}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can the Stage68 best branch(68단계 최선 분기) keep validation/OOS PF(검증/표본외 수익 팩터), net(순손익), and DD(손실률) credible enough for candidate review(후보 검토), or should a new model branch(새 모델 분기)를 열어야 하는가?

Effect(효과): Stage69(69단계)는 Stage68(68단계) 결과를 무한 조정하지 않고, 후보 검토 또는 새 분기 결정을 하나의 측정 질문으로 좁힌다.

## Result Matrix(결과 행렬)

{table(rows)}

## Judgment(판정)

- result_subject(판정 대상): Stage66-68 short-gate DD/net branch(66-68단계 숏 게이트 손실률/순손익 분기)
- evidence_available(사용 근거): Stage66-68 MT5 KPI(66-68단계 메타트레이더5 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), stage reports(단계 보고서)
- observed_change(관찰 변화): risk cap(위험 상한)과 cooldown(냉각)을 낮추면 DD(손실률)는 낮아지지만 net(순손익)도 같이 낮아졌다.
- best_reviewed_candidate(최선 검토 후보): `{best.get("candidate_key", "none")}`
- evidence_missing(부족 근거): 현재 branch(분기)는 latest 34D KPI(최신 34D 핵심 성과 지표)의 PF/net/DD(수익 팩터/순손익/손실률)를 동시에 만족하지 못한다.
- judgment_label(판정 라벨): `exploratory_branch_limit_observed`
- next_condition(다음 조건): Stage70(70단계)에서 model source/model branch(모델 원천/모델 분기)를 바꿔 PF/net/DD(수익 팩터/순손익/손실률) 표면 자체를 개선해야 한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def build_decision(rows: Sequence[Mapping[str, Any]]) -> str:
    best = rows[0] if rows else {}
    return f"""# Stage69 Decision(69단계 판정)

decision(판정): `{DECISION}`

Stage69(69단계)는 Stage66-68(66-68단계)의 short-gate branch(숏 게이트 분기)를 candidate review(후보 검토)로 올릴 수 있는지 확인했다. Best reviewed candidate(검토 최선 후보)는 `{best.get("candidate_key", "none")}`였지만, 34D latest target(34D 최신 목표)의 PF(수익 팩터), net(순손익), DD(손실률)를 동시에 만족하지 못했다.

Effect(효과): short-gate branch(숏 게이트 분기)를 무한 수리하지 않고, Stage70(70단계)에서 v2-native new model branch(브이투 고유 새 모델 분기)를 연다.

## Evidence(근거)

- review_matrix(검토 행렬): `{rel(SUMMARY_CSV)}`
- report(보고서): `{rel(REPORT_MD)}`
- source_stage68_report(원천 68단계 보고서): `stages/68_adapter_research__dd_net_balance_repair/03_reviews/stage68_dd_net_balance_report.md`
- external_verification_status(외부 검증 상태): `{EXTERNAL}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    existing: dict[str, dict[str, Any]] = {}
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                existing[str(row.get(key, ""))] = row
    for row in rows:
        existing[str(row[key])] = {column: row.get(column, "") for column in columns}
    write_csv(path, list(existing.values()), columns)


def write_stage_files(rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv(SUMMARY_CSV, rows)
    write_md(REPORT_MD, build_report(rows))
    write_md(DECISION_MD, build_decision(rows))
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "run_number": RUN_NUMBER,
            "packet_id": PACKET_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_stage68_pushed_commit": SOURCE_STAGE68_COMMIT,
            "review_inputs": [rel(STAGE66_SUMMARY), rel(STAGE67_SUMMARY), rel(STAGE68_SUMMARY)],
            "decision": DECISION,
            "external_verification_status": EXTERNAL,
            "claim_boundary": BOUNDARY,
        },
    )


def write_registers(rows: Sequence[Mapping[str, Any]]) -> None:
    best = rows[0] if rows else {}
    run_registry_columns = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
    alpha_columns = [
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
    artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"]
    upsert_csv(
        RUN_REGISTRY,
        run_registry_columns,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_branch_or_candidate_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_MD),
                "notes": f"best_reviewed_candidate={best.get('candidate_key', 'none')};target_surface={TARGET_SURFACE};legacy_relation=lesson_only",
            }
        ],
        "run_id",
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__branch_candidate_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "branch_candidate_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "review_only",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage69_branch_candidate_review",
        "scoreboard_lane": "result_judgment",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(REPORT_MD),
        "primary_kpi": f"best_reviewed_candidate={best.get('candidate_key', 'none')}",
        "guardrail_kpi": f"target_surface={TARGET_SURFACE};forbidden_claims_preserved=true",
        "external_verification_status": EXTERNAL,
        "notes": "Review-only decision from completed Stage66-68 MT5 evidence; not a deployment or runtime authority claim.",
    }
    upsert_csv(ALPHA_LEDGER, alpha_columns, [ledger_row], "ledger_row_id")
    upsert_csv(STAGE_LEDGER, alpha_columns, [ledger_row], "ledger_row_id")
    created = now_utc()
    artifact_rows = []
    for path in [SUMMARY_CSV, REPORT_MD, DECISION_MD, STAGE_LEDGER, RUN_MANIFEST]:
        if path.exists():
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage69_branch_candidate_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage69 review-only branch/candidate evidence.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows, "artifact_id")


def write_packet_files(rows: Sequence[Mapping[str, Any]]) -> None:
    best = rows[0] if rows else {}
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-experiment-design"],
            "required_gates": ["result_judgment_gate", "artifact_lineage_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "best_reviewed_candidate": best.get("candidate_key", "none"),
            "external_verification_status": EXTERNAL,
            "claim_boundary": BOUNDARY,
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
                "legacy_inheritance",
            ],
        },
    )
    write_json(
        PACKET_ROOT / "artifact_lineage_gate.json",
        {
            "packet_id": PACKET_ID,
            "source_stage68_pushed_commit": SOURCE_STAGE68_COMMIT,
            "review_inputs": [rel(STAGE66_SUMMARY), rel(STAGE67_SUMMARY), rel(STAGE68_SUMMARY)],
            "outputs": [rel(SUMMARY_CSV), rel(REPORT_MD), rel(DECISION_MD)],
        },
    )
    write_json(
        PACKET_SUMMARY,
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "best_reviewed_candidate": best.get("candidate_key", "none"),
            "overall_goal_complete": False,
        },
    )


def write_current_truth() -> None:
    text = WORKSPACE_STATE.read_text(encoding="utf-8-sig")
    text = re_sub_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = re_sub_line(text, "active_stage:", f"active_stage: {NEXT_STAGE_ID}")
    focus = f"""current_focus:
- >-
  Stage69(69단계) closed(종료) as `{DECISION}` and Stage70(70단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): short-gate branch limit(숏 게이트 분기 한계)을 보존하고, 새 model branch(모델 분기)로만 넘긴다.
- >-
  Stage69 result(69단계 결과): Stage66-68(66-68단계) KPI(핵심 성과 지표)를 검토한 결과 candidate review(후보 검토)에는 부족하고 new model branch(새 모델 분기)가 필요하다. Effect(효과): 같은 branch(분기)를 무한 수리하지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    import re

    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", focus, text, count=1)
    block = f"""

stage69_branch_or_candidate_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  adapter_under_review: {SOURCE_ADAPTER_ID}
  source_stage68_pushed_commit: {SOURCE_STAGE68_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_MD)}
  packet_summary_path: {rel(PACKET_SUMMARY)}
  external_verification_status: {EXTERNAL}
  boundary: {BOUNDARY}
"""
    if "stage69_branch_or_candidate_review:" not in text:
        text = text.rstrip() + block
    WORKSPACE_STATE.write_text(text.rstrip() + "\n", encoding="utf-8")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage69 Selection Status(69단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- source_stage(원천 단계): `68_adapter_research__dd_net_balance_repair`
- source_decision(원천 판정): `continue_dd_net_balance_repair_in_stage69`
- current_run(현재 실행): `{RUN_ID}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage69_decision(69단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage69(69단계)는 short-gate branch(숏 게이트 분기)를 후보로 올리지 않고, 새 model branch(모델 분기)로 넘긴다.
""",
    )
    write_md(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `{SOURCE_ADAPTER_ID}`
- status(상태): `stage69_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage69(69단계) closed(종료) as review-only branch decision(검토 전용 분기 결정). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage70(70단계) 새 model branch(모델 분기)로 이어진다.

## Latest Stage69 Evidence(최신 69단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL}`
- report(보고서): `{rel(REPORT_MD)}`
- stage69_decision(69단계 판정): `{rel(DECISION_MD)}`
- review_matrix(검토 행렬): `{rel(SUMMARY_CSV)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )


def re_sub_line(text: str, prefix: str, replacement: str) -> str:
    lines = []
    done = False
    for line in text.splitlines():
        if not done and line.startswith(prefix):
            lines.append(replacement)
            done = True
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage70(70단계)는 Stage69(69단계)의 branch limit(분기 한계) 판정을 받아, short-gate parameter repair(숏 게이트 파라미터 수리)가 아니라 v2-native new model branch(브이투 고유 새 모델 분기)를 여는 단계다.

## Bounded Question(경계 질문)

Can a new v2-native model branch(브이투 고유 새 모델 분기) improve PF/net/DD(수익 팩터/순손익/손실률) beyond the short-gate branch limit(숏 게이트 분기 한계) without copying legacy 34D(레거시 34D)?

Effect(효과): Stage70(70단계)는 기존 short-gate branch(숏 게이트 분기)를 무한 수리하지 않고, model source/model branch(모델 원천/모델 분기)를 바꿔 KPI surface(핵심 성과 지표 표면)를 다시 찾는다.

## Boundary(경계)

`{BOUNDARY}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage70 Input References(70단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_external_verification_status(원천 외부 검증 상태): `{EXTERNAL}`
- stage69_report(69단계 보고서): `{rel(REPORT_MD)}`
- stage69_decision(69단계 판정): `{rel(DECISION_MD)}`
- review_matrix(검토 행렬): `{rel(SUMMARY_CSV)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage70(70단계)는 short-gate branch limit(숏 게이트 분기 한계)을 입력으로 삼고, v2 고유 새 모델 분기만 연다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage70 Review Index(70단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage70(70단계)는 Stage69(69단계) closeout(종료 기록)을 이어받아 다음 bounded batch(경계 묶음 실행)만 검토한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage70 Selection Status(70단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage70(70단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def append_changelog() -> None:
    entry = f"""
## 2026-05-17 - Stage69 branch/candidate review closeout(69단계 분기/후보 검토 종료)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- effect(효과): Stage66-68(66-68단계) short-gate branch(숏 게이트 분기)의 KPI(핵심 성과 지표) 한계를 검토하고, 새 model branch(모델 분기)로 넘겼다.
"""
    existing = CHANGELOG.read_text(encoding="utf-8-sig") if CHANGELOG.exists() else ""
    if RUN_ID not in existing:
        CHANGELOG.write_text(existing.rstrip() + "\n" + entry.lstrip(), encoding="utf-8-sig")


def main() -> int:
    rows = review_rows()
    write_stage_files(rows)
    write_registers(rows)
    write_packet_files(rows)
    write_current_truth()
    create_next_stage()
    append_changelog()
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": RUN_ID,
                "decision": DECISION,
                "external_verification_status": EXTERNAL,
                "review_csv": rel(SUMMARY_CSV),
                "decision_path": rel(DECISION_MD),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
