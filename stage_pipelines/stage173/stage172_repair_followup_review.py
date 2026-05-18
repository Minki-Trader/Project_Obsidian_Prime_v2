from __future__ import annotations

import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)

STAGE_ID = "173_adapter_research__stage172_repair_followup_review"
RUN_ID = "run173A_stage173_stage172_repair_followup_review_v1"
PACKET_ID = "stage173_stage172_repair_followup_review_v1"
PARENT_RUN_ID = "run172A_stage172_validation_drawdown_concentration_repair_v1"
SOURCE_STAGE_ID = "172_adapter_research__validation_drawdown_concentration_repair"
SOURCE_RUN_ID = "run172A_stage172_validation_drawdown_concentration_repair_v1"
SOURCE_STAGE172_CLOSEOUT_COMMIT = "37d15f6a29a56b01da448134d5bc03af467203fe"
SOURCE_STAGE172_HASH_RECORD_COMMIT = "8d182d513e2e18d35d2773f656eeeea9e00aab4f"
NEXT_STAGE_ID = "174_adapter_research__wide_gate_mid_segment_recovery_repair"
NEXT_RUN_ID = "run174A_stage174_wide_gate_mid_segment_recovery_repair_v1"
NEXT_PACKET_ID = "stage174_wide_gate_mid_segment_recovery_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "review_only_source_stage172_mt5_reports_completed"
DECISION = "open_stage174_wide_gate_mid_segment_recovery_repair_candidate_not_final"

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE172_REPORT = Path("stages/172_adapter_research__validation_drawdown_concentration_repair/03_reviews/stage172_validation_drawdown_concentration_repair_report.md")
SOURCE_STAGE172_QUALITY = Path("stages/172_adapter_research__validation_drawdown_concentration_repair/03_reviews/stage172_quality_matrix.csv")
SOURCE_STAGE172_BALANCE = Path("stages/172_adapter_research__validation_drawdown_concentration_repair/03_reviews/stage172_balance_curve_audit.csv")
SOURCE_STAGE172_MONTHLY = Path("stages/172_adapter_research__validation_drawdown_concentration_repair/03_reviews/stage172_monthly_kpi_summary.csv")
SOURCE_STAGE172_RISK_ATR = Path("stages/172_adapter_research__validation_drawdown_concentration_repair/03_reviews/stage172_risk_atr_telemetry.csv")
SOURCE_STAGE172_DECISION = Path("stages/172_adapter_research__validation_drawdown_concentration_repair/03_reviews/stage172_decision.md")

REPORT_PATH = REVIEWS_ROOT / "stage173_stage172_repair_followup_review.md"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage173_route_matrix.csv"
LESSON_MATRIX_PATH = REVIEWS_ROOT / "stage173_stage172_lesson_matrix.csv"
DECISION_PATH = REVIEWS_ROOT / "stage173_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage173/stage172_repair_followup_review.py")
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
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def load_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        value = row.get(key, default)
        if value in (None, ""):
            return default
        return float(str(value).replace(",", "").replace("%", ""))
    except (TypeError, ValueError):
        return default


def quality_flag(row: Mapping[str, Any]) -> str:
    return str(row.get("quality_flags", ""))


def build_lesson_rows(quality_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        flags = quality_flag(row)
        val_dd_margin = as_float(row, "validation_dd_margin_vs_34d")
        val_net_gap = as_float(row, "validation_net_gap_vs_34d")
        val_late_share = as_float(row, "validation_late_net_share")
        oos_dd = as_float(row, "oos_balance_dd_percent")
        clue = "negative_memory"
        lesson = "No bounded pass."
        if "short_wide" in adapter_id:
            clue = "dd_concentration_control_clue"
            lesson = "wide gate lowered validation DD and late share but damaged net/PF and OOS DD."
        elif "sl195_risk0360" in adapter_id:
            clue = "oos_net_sl_clue"
            lesson = "tight SL plus mild risk recapture lifted OOS net above 34D but damaged validation PF/net/DD."
        elif "control" in adapter_id:
            clue = "control_failure_memory"
            lesson = "original anchor remains near 34D net but keeps DD, early/mid PF, and late concentration failures."
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "adapter_id": adapter_id,
                "clue_type": clue,
                "validation_net": as_float(row, "validation_net"),
                "validation_net_gap_vs_34d": val_net_gap,
                "validation_balance_dd_percent": as_float(row, "validation_balance_dd_percent"),
                "validation_dd_margin_vs_34d": val_dd_margin,
                "validation_early_pf": as_float(row, "validation_early_pf"),
                "validation_mid_pf": as_float(row, "validation_mid_pf"),
                "validation_late_share": val_late_share,
                "oos_pf": as_float(row, "oos_pf"),
                "oos_net": as_float(row, "oos_net"),
                "oos_balance_dd_percent": oos_dd,
                "hard_quality_pass": str(row.get("hard_quality_pass", "")).lower() == "true",
                "quality_flags": flags,
                "lesson": lesson,
            }
        )
    return rows


def build_route_rows(lesson_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    wide = next((row for row in lesson_rows if row.get("clue_type") == "dd_concentration_control_clue"), {})
    sl = next((row for row in lesson_rows if row.get("clue_type") == "oos_net_sl_clue"), {})
    control = next((row for row in lesson_rows if row.get("clue_type") == "control_failure_memory"), {})
    return [
        {
            "run_id": RUN_ID,
            "route": "stage174_primary",
            "decision": DECISION,
            "source_clue": wide.get("adapter_id", ""),
            "repair_question": "Can wide short-context DD control recover validation mid PF/net without losing validation DD and OOS DD?",
            "why": "wide gate is the only Stage172 clue that brought validation balance DD under 34D and late share under 50 percent.",
            "guardrails": "no date-specific filter; keep v2 source model; preserve risk/ATR telemetry; require validation/OOS segment read.",
        },
        {
            "run_id": RUN_ID,
            "route": "stage174_supporting_control",
            "decision": DECISION,
            "source_clue": sl.get("adapter_id", ""),
            "repair_question": "Use SL 1.95 only as a supporting clue, not as the main route.",
            "why": "SL 1.95 improved OOS net/PF but made validation PF/net/DD worse.",
            "guardrails": "do not treat OOS-only improvement as success.",
        },
        {
            "run_id": RUN_ID,
            "route": "failure_memory",
            "decision": DECISION,
            "source_clue": control.get("adapter_id", ""),
            "repair_question": "Do not re-run the unchanged Stage169 anchor as if it were repaired.",
            "why": "control reproduced the known Stage171 failures.",
            "guardrails": "avoid final claim from near-34D net alone.",
        },
    ]


def report_markdown(lesson_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]]) -> str:
    wide = next((row for row in lesson_rows if row.get("clue_type") == "dd_concentration_control_clue"), {})
    sl = next((row for row in lesson_rows if row.get("clue_type") == "oos_net_sl_clue"), {})
    return f"""# Stage173 Stage172 Repair Follow-up Review(173단계 172단계 수정 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## KPI Meaning(KPI 의미)

Stage172(172단계)는 hard quality pass(강한 품질 통과)를 만들지 못했다. Effect(효과): 전체 목표(overall goal, 전체 목표)는 계속 열려 있고 Stage174(174단계)로 넘어간다.

- wide gate clue(넓은 제한문 단서): `{wide.get("adapter_id", "none")}`는 validation DD(검증 낙폭) `{as_float(wide, "validation_balance_dd_percent"):.4f}%`와 late share(후반 비중) `{as_float(wide, "validation_late_share"):.4f}`를 개선했다. Effect(효과): DD/concentration control(낙폭/집중도 제어) 단서는 살아 있다.
- wide gate damage(넓은 제한문 손상): 같은 후보의 validation net(검증 순손익)은 `{as_float(wide, "validation_net"):.2f}`로 34D(34D)보다 `{as_float(wide, "validation_net_gap_vs_34d"):.2f}` 낮고, mid PF(중반 수익요인)는 `{as_float(wide, "validation_mid_pf"):.6f}`다. Effect(효과): Stage174(174단계)는 mid segment recovery(중반 구간 회복)를 중심 질문으로 잡아야 한다.
- SL clue(손절 단서): `{sl.get("adapter_id", "none")}`는 OOS net(표본외 순손익) `{as_float(sl, "oos_net"):.2f}`까지 올렸지만 validation(검증)을 훼손했다. Effect(효과): SL 1.95(손절 1.95)는 보조 단서이지 성공 후보가 아니다.

## Route(경로)

Stage174(174단계) bounded question(경계 질문): wide short-context gate(넓은 숏 문맥 제한문)의 validation DD/concentration(검증 낙폭/집중도) 개선을 보존하면서 validation mid PF/net(검증 중반 수익요인/순손익)과 OOS DD(표본외 낙폭)를 회복할 수 있는가?

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage173 Decision(173단계 판정)

- decision(판정): `{DECISION}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage172_closeout_commit(원천 172단계 종료 커밋): `{SOURCE_STAGE172_CLOSEOUT_COMMIT}`
- source_stage172_hash_record_commit(원천 172단계 해시 기록 커밋): `{SOURCE_STAGE172_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage173(173단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다. Effect(효과): Stage174(174단계)는 wide gate(넓은 제한문) 단서를 중심으로 validation mid recovery(검증 중반 회복)를 좁게 시험한다.
"""


def artifact_rows() -> list[dict[str, Any]]:
    now = utc_now()
    rows = []
    for path in (
        PRODUCER_PATH,
        REPORT_PATH,
        ROUTE_MATRIX_PATH,
        LESSON_MATRIX_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
        SOURCE_STAGE172_REPORT,
        SOURCE_STAGE172_QUALITY,
        SOURCE_STAGE172_BALANCE,
        SOURCE_STAGE172_RISK_ATR,
        SOURCE_STAGE172_DECISION,
    ):
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage173_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": now,
                    "notes": "Stage173 follow-up review evidence.",
                }
            )
    return rows


def write_ledgers(decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage173_stage172_repair_followup_review",
                "status": "reviewed",
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage172_closeout_commit", SOURCE_STAGE172_CLOSEOUT_COMMIT),
                        ("source_stage172_hash_record_commit", SOURCE_STAGE172_HASH_RECORD_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only_no_inheritance"),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage172_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage172_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "followup_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage172_kpi_tradeoff_review",
            "scoreboard_lane": "review",
            "status": "reviewed",
            "judgment": decision,
            "path": rel(REPORT_PATH),
            "primary_kpi": "wide_gate_validation_dd=11.7848;wide_gate_validation_net=760.45;sl195_risk0360_oos_net=999.52",
            "guardrail_kpi": "no_hard_pass;no_deployment;no_overall_goal_complete",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage173 is review-only using completed Stage172 MT5 evidence.",
        }
    ]
    return {
        "run_registry": run_payload,
        "alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id"),
    }


def write_packet_files(decision: str, ledger_payload: Mapping[str, Any], lesson_rows: Sequence[Mapping[str, Any]], route_rows: Sequence[Mapping[str, Any]]) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": "reviewed",
        "decision": decision,
        "report_path": rel(REPORT_PATH),
        "decision_path": rel(DECISION_PATH),
        "route_matrix": rel(ROUTE_MATRIX_PATH),
        "lesson_matrix": rel(LESSON_MATRIX_PATH),
        "ledger_payload": ledger_payload,
        "lesson_rows": list(lesson_rows),
        "route_rows": list(route_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", payload)
    write_json(PACKET_ROOT / "result_judgment_gate.json", payload)
    write_json(PACKET_ROOT / "packet_receipt.json", payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage173 Closeout Packet(173단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `reviewed`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed(decision: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage174(174단계)는 Stage173(173단계) review(검토)에서 살아남은 wide gate(넓은 제한문) 단서를 bounded repair(경계 수정)로 시험한다.

## Bounded Question(경계 질문)

Can the Stage172(172단계) wide short-context gate(넓은 숏 문맥 제한문) keep validation DD/concentration(검증 낙폭/집중도) control while recovering validation mid PF/net(검증 중반 수익요인/순손익) and preventing OOS DD(표본외 낙폭) damage?

Effect(효과): Stage174(174단계)는 새 모델 사냥(new model hunt, 새 모델 탐색)이 아니라 wide gate(넓은 제한문)의 손상 구간만 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage174 Inputs(174단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- source_stage172_quality(원천 172단계 품질): `{rel(SOURCE_STAGE172_QUALITY)}`
- source_stage172_balance(원천 172단계 잔고): `{rel(SOURCE_STAGE172_BALANCE)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage174 Review Index(174단계 검토 색인)

- status(상태): `open_planned_from_stage173`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage174 Selection Status(174단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage173`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage173(173단계) closed(종료) as `{decision}` and Stage174(174단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage172(172단계)의 wide gate DD/concentration clue(넓은 제한문 낙폭/집중도 단서)를 mid segment recovery(중반 구간 회복) 수리로 넘긴다.
- >-
  Stage173 evidence(173단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(ROUTE_MATRIX_PATH)}`, `{rel(LESSON_MATRIX_PATH)}`에 있다. Effect(효과): 실패한 SL-only(손절 단독) 개선과 살아남은 wide gate(넓은 제한문) 단서를 분리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    state = re.sub(r"(?ms)^stage173_stage172_repair_followup_review:\r?\n.*?(?=^stage\d+_|\Z)", "", state)
    block = f"""
stage173_stage172_repair_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  route_matrix_path: {rel(ROUTE_MATRIX_PATH)}
  lesson_matrix_path: {rel(LESSON_MATRIX_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage174_wide_gate_mid_segment_recovery_surface`
- status(상태): `stage173_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage173(173단계)는 Stage172(172단계) 결과를 follow-up review(후속 검토)로 판독했다. Effect(효과): Stage174(174단계)는 wide gate(넓은 제한문)의 validation DD/concentration(검증 낙폭/집중도) 장점은 살리고 validation mid PF/net(검증 중반 수익요인/순손익) 손상만 좁게 수리한다.

## Latest Stage173 Evidence(최신 173단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str) -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage173 Selection Status(173단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage173 Review Index(173단계 검토 색인)

- status(상태): `closed_{decision}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- lesson_matrix(교훈 행렬): `{rel(LESSON_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage173 Stage172 repair follow-up review closeout(173단계 172단계 수정 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage172(172단계)의 DD/concentration(낙폭/집중도) 개선 단서와 net/PF(순손익/수익요인) 손상을 분리해 Stage174(174단계) 수리 질문으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    quality = load_csv(SOURCE_STAGE172_QUALITY)
    lesson_rows = build_lesson_rows(quality)
    route_rows = build_route_rows(lesson_rows)
    write_csv(LESSON_MATRIX_PATH, lesson_rows)
    write_csv(ROUTE_MATRIX_PATH, route_rows)
    write_md(REPORT_PATH, report_markdown(lesson_rows, route_rows))
    write_md(DECISION_PATH, decision_markdown())
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(DECISION, artifacts)
    write_packet_files(DECISION, ledger_payload, lesson_rows, route_rows)
    write_next_stage_seed(DECISION)
    update_current_truth(DECISION)
    write_status_files(DECISION)
    append_changelog(DECISION)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "external_verification_status": EXTERNAL_STATUS,
                    "report": rel(REPORT_PATH),
                    "next_stage": NEXT_STAGE_ID,
                    "overall_goal_complete": False,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
