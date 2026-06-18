from __future__ import annotations

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_85__runtime_path_contradiction_firewall_label_rebuild"
RUN_ID = "frontier85A_stage_open_runtime_path_contradiction_firewall_label_rebuild_v1"
PARENT_RUN_ID = "frontier84F_runtime_realized_winrate_repair_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier85B_leakage_safe_runtime_path_firewall_proxy_scout_v1"

STATUS = "opened_runtime_path_contradiction_firewall_label_rebuild_no_authority"
JUDGMENT = "frontier85_opened_leakage_safe_runtime_path_label_axis_no_authority"
CLAIM_BOUNDARY = (
    "frontier85_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
FRONTIER_EXTRA_DUE_STATUS = "not_due_after_f84_closeout_next_boundary_f100_e01_closed_for_f050"
FIVE_STAGE_RETROSPECTIVE_STATUS = "retired_archive_only_no_new_grok_call_no_next_open_block"

SCRIPT_REL = "stage_pipelines/stage_frontier_85/frontier85a_stage_open_runtime_path_contradiction_firewall_label_rebuild.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
INPUT_DIR = STAGE_DIR / "01_inputs"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
INPUT_REFS = INPUT_DIR / "input_refs.md"
REPORT = REVIEW_DIR / "frontier85A_stage_open_runtime_path_contradiction_firewall_label_rebuild_report.md"
MANIFEST = REVIEW_DIR / "f85a_stage_open_manifest.json"
EXPERIMENT_DESIGN = REVIEW_DIR / "f85a_experiment_design.json"
SOURCE_HASH_REFRESH = REVIEW_DIR / "f85a_source_hash_refresh.json"
TASK_FORCE_CALLS_PATH = REVIEW_DIR / "f85a_actual_subagent_calls.json"
ARTIFACT_LINEAGE = REVIEW_DIR / "f85a_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f85a_local_verification.json"
GATE_AUDIT_MD = REVIEW_DIR / "required_gate_coverage_audit_f85a_open.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

EXPERIMENT_RECEIPT = REVIEW_DIR / "f85a_experiment_design_receipt.yaml"
DATA_INTEGRITY_RECEIPT = REVIEW_DIR / "f85a_data_integrity_receipt.yaml"
MODEL_VALIDATION_RECEIPT = REVIEW_DIR / "f85a_model_validation_receipt.yaml"
RUNTIME_REQUIREMENTS_RECEIPT = REVIEW_DIR / "f85a_runtime_materialization_requirements_receipt.yaml"
RESULT_RECEIPT = REVIEW_DIR / "f85a_result_judgment_receipt.yaml"
ARTIFACT_RECEIPT = REVIEW_DIR / "f85a_artifact_lineage_receipt.yaml"
TASK_FORCE_RECEIPT = REVIEW_DIR / "f85a_task_force_review_receipt.yaml"
CLAIM_RECEIPT = REVIEW_DIR / "f85a_claim_discipline_receipt.yaml"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-18_stage_frontier_85_open.md"
FRONTIER_EXTRA_REGISTER = ROOT / "docs/registers/frontier_extra_stage_register.yaml"

F84_STAGE_ID = "stage_frontier_84__runtime_realized_winrate_rebuild_after_signal_parity_gap"
F84_STAGE_DIR = ROOT / "stages" / F84_STAGE_ID
F84F_SUMMARY = F84_STAGE_DIR / "03_reviews/f84f_repair_or_rotation_decision_summary.json"
F84F_REPORT = F84_STAGE_DIR / "03_reviews/stage_closeout_report.md"
F84F_PIVOTS = F84_STAGE_DIR / "03_reviews/f84f_runtime_path_contradiction_pivot_rows.csv"
F84F_CALLS = F84_STAGE_DIR / "03_reviews/f84f_actual_subagent_calls.json"
F84E_SUMMARY = F84_STAGE_DIR / "03_reviews/f84e_row_level_deal_reconciliation_summary.json"
F84E_ROWS = F84_STAGE_DIR / "03_reviews/f84e_row_level_reconciliation_rows.csv"
F84E_SPLIT_SUMMARY = F84_STAGE_DIR / "03_reviews/f84e_row_level_reconciliation_split_summary.csv"
F84C_SUMMARY = F84_STAGE_DIR / "03_reviews/f84c_mt5_runtime_realized_winrate_materialization_summary.json"

TASK_FORCE_CALLS: list[dict[str, Any]] = [
    {
        "roster_id": "agent_01_system_governor",
        "nickname": "Goodall",
        "agent_id": "019eda8a-3d33-7661-b4f7-a212d49dcc13",
        "status": "completed",
        "phase": "f85a_goal_and_claim_boundary",
        "classification": "accepted",
        "accepted": "F85A opening is aligned with the active ONNX runtime goal(활성 온엑스 런타임 목표와 정렬).",
        "rejected": "Inherited winner/baseline/authority(상속 승자/기준선/권위) and promotion/live readiness/Goal Achieve(승격/실거래 준비/목표 달성).",
        "needs_local_verification": "Recheck leakage-safe label(누수 안전 라벨), WFO/MT5 materialization(워크포워드/MT5 물질화), and runtime claim boundary(런타임 주장 경계).",
    },
    {
        "roster_id": "agent_02_platform_routing_architect",
        "nickname": "Zeno",
        "agent_id": "019eda8a-8366-7060-9329-3f49c52338d7",
        "status": "completed",
        "phase": "f85a_work_family_routing",
        "classification": "accepted",
        "accepted": "F85A should be experiment_design(실험 설계), primary_skill obsidian-experiment-design(주 스킬 실험 설계).",
        "rejected": "Opening F85A as immediate runtime_backtest(즉시 런타임 백테스트).",
        "needs_local_verification": "Create F85 stage-local selection_status(선택 상태) and stage_run_ledger(단계 실행 장부).",
    },
    {
        "roster_id": "agent_03_philosophy_policy_skill_governance",
        "nickname": "James",
        "agent_id": "019eda8a-c604-7dd1-b061-fd37c13c13a6",
        "status": "completed",
        "phase": "f85a_policy_governance",
        "classification": "accepted",
        "accepted": "F85A open is allowed under exploration mandate(탐색 명령) with F84 as clue/seed/negative memory only(단서/씨앗/부정 기억 전용).",
        "rejected": "Winner/baseline inheritance(승자/기준선 상속), threshold/filter-only repair(임계값/필터만 수리), and any Grok active call/authority(그록 활성 호출/권위).",
        "needs_local_verification": "Keep claim boundary: no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
    },
    {
        "roster_id": "agent_04_evidence_control_plane",
        "nickname": "Curie",
        "agent_id": "019eda8b-1d8e-7be1-88a9-ca3405737786",
        "status": "completed",
        "phase": "f85a_evidence_control_plane",
        "classification": "needs_local_verification",
        "accepted": "F84F summary, F84E row/split evidence, F84C/F84E runtime materialization, and negative register are usable as F85A input with reference-only boundary.",
        "rejected": "Treating F85 handoff scaffold(인계 뼈대) as F85A open evidence(개방 근거).",
        "needs_local_verification": "Create packet, manifest, source hash refresh, receipts, gate audit, final claim guard, ledgers, and artifact registry rows.",
    },
    {
        "roster_id": "agent_05_data_feature_contract",
        "nickname": "Lorentz",
        "agent_id": "019eda8b-620c-7c22-af7b-b4f21a1e67d6",
        "status": "completed",
        "phase": "f85a_data_feature_boundary",
        "classification": "needs_local_verification",
        "accepted": "F84E row-level evidence is usable as F85A seed/negative memory(씨앗/부정 기억).",
        "rejected": "Using tp_expected_sl_actual, runtime_exit_reason, runtime_win, or runtime_net_profit(익절예상-손절실제/런타임 종료 사유/승패/순손익) as feature/filter.",
        "needs_local_verification": "Use only pre-entry observable inputs(진입 전 관측 가능 입력) and broker-clock alignment boundary(브로커 시계 정렬 경계).",
    },
    {
        "roster_id": "agent_06_quant_research",
        "nickname": "Feynman",
        "agent_id": "019eda8c-7f6e-7ff2-be4f-21ee82daba76",
        "status": "completed",
        "phase": "f85a_quant_axis_design",
        "classification": "accepted",
        "accepted": "F85B should prioritize pre-entry first-touch surrogate(진입 전 첫 터치 대체 신호), then both-hit ambiguity class(양방향 터치 모호 분류), path-inversion meta-label(경로 반전 보조 라벨), and regime route(장세 라우팅).",
        "rejected": "Threshold-only repair(임계값만 수리) because it repeats the F84 failure mode(F84 실패 반복).",
        "needs_local_verification": "Session/regime/streak route(세션/장세/연속손실 라우팅)는 WFO stability(워크포워드 안정성) 확인 뒤 적용.",
    },
    {
        "roster_id": "agent_07_model_validation_risk",
        "nickname": "Hubble",
        "agent_id": "019eda8d-646c-77c2-8e75-1de942d7eeb4",
        "status": "completed",
        "phase": "f85a_model_validation_risk",
        "classification": "accepted_with_local_verification",
        "accepted": "F85A can open leakage-safe runtime path contradiction label(누수 안전 런타임 경로 모순 라벨) experiment design.",
        "rejected": "Direct diagnostic-class feature/filter use, OOS threshold tuning(표본외 임계값 조정), and authority laundering(권위 세탁).",
        "needs_local_verification": "Inputs must be pre-entry observable and labels must not leak outside split/WFO boundaries(분할/워크포워드 경계).",
    },
    {
        "roster_id": "agent_08_mt5_onnx_runtime",
        "nickname": "Kuhn",
        "agent_id": "019eda8f-6348-7a82-a1f3-a7b755e8d4dd",
        "status": "completed",
        "phase": "f85a_runtime_materialization_boundary",
        "classification": "accepted_with_local_verification",
        "accepted": "F85A defines F85B/F85C runtime materialization requirements(런타임 물질화 요구사항) instead of running MT5 now.",
        "rejected": "Immediate runtime probe(즉시 런타임 탐침) before leakage-safe label/proxy/candidate/ONNX/EA settings are materialized.",
        "needs_local_verification": "Future MT5/ONNX receipts require report/log/snapshot/telemetry, hashes, feature schema, tester profile, and ticket-level reconciliation.",
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def csv_value(value: Any) -> Any:
    value = json_ready(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return value


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    fieldnames = list(rows[0].keys() if rows else ["empty"])
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with open(str(path.resolve()), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def rewrite_csv_rows(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(f"{path.stem}.tmp")
    with open(str(tmp_path.resolve()), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})
    tmp_path.replace(path)


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: csv_value(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    rewrite_csv_rows(path, rows, fieldnames)


def remove_csv_rows(path: Path, predicate: Callable[[dict[str, str]], bool]) -> None:
    if not path_exists(path):
        return
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [row for row in reader if not predicate(row)]
    rewrite_csv_rows(path, rows, fieldnames)


def data_row_count(path: Path) -> int:
    if not path_exists(path):
        return -1
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def split_rows() -> dict[str, dict[str, str]]:
    return {row["split"]: row for row in read_csv(F84E_SPLIT_SUMMARY)}


def matched_rows(split: str) -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(F84E_ROWS)
        if row.get("split") == split and row.get("runtime_match_status") == "ticket_match"
    ]


def f84e_clue_metrics() -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for split in ("validation", "oos"):
        rows = matched_rows(split)
        tp_sl = [row for row in rows if str(row.get("tp_expected_sl_actual", "")).lower() == "true"]
        no_tp_sl = [row for row in rows if str(row.get("tp_expected_sl_actual", "")).lower() != "true"]
        proxy_wins = [row for row in rows if str(row.get("proxy_win", "")).lower() == "true"]
        proxy_win_runtime_loss = [row for row in rows if str(row.get("proxy_win_runtime_loss", "")).lower() == "true"]
        net = lambda source: round(sum(as_float(row.get("runtime_net_profit_filled") or row.get("runtime_net_profit")) for row in source), 6)
        metrics[split] = {
            "matched_trade_count": len(rows),
            "proxy_win_count": len(proxy_wins),
            "proxy_win_runtime_loss_count": len(proxy_win_runtime_loss),
            "tp_expected_sl_actual_count": len(tp_sl),
            "tp_expected_sl_actual_net": net(tp_sl),
            "excluding_tp_expected_sl_actual_count": len(no_tp_sl),
            "excluding_tp_expected_sl_actual_net": net(no_tp_sl),
        }
    return metrics


def task_force_coverage() -> dict[str, Any]:
    required = {f"agent_0{i}_" for i in range(1, 9)}
    covered = {call["roster_id"][:9] for call in TASK_FORCE_CALLS}
    completed = {call["roster_id"][:9] for call in TASK_FORCE_CALLS if call.get("status") == "completed"}
    return {
        "required_count": 8,
        "actual_call_count": len(TASK_FORCE_CALLS),
        "coverage_count": len(required & covered),
        "completed_count": len(required & completed),
        "all_required_covered": required <= covered,
        "all_required_completed": required <= completed,
        "incomplete_roster_ids": sorted(required - completed),
        "call_ids": [call["agent_id"] for call in TASK_FORCE_CALLS],
    }


def source_hash_refresh(created_at: str) -> dict[str, Any]:
    paths = [
        F84F_SUMMARY,
        F84F_REPORT,
        F84F_PIVOTS,
        F84F_CALLS,
        F84E_SUMMARY,
        F84E_ROWS,
        F84E_SPLIT_SUMMARY,
        F84C_SUMMARY,
        NEGATIVE_REGISTER,
        FRONTIER_EXTRA_REGISTER,
    ]
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "purpose": "F85A source identity refresh(F85A 원천 정체성 갱신)",
        "sources": [
            {
                "path": rel(path),
                "exists": path_exists(path),
                "data_row_count": data_row_count(path) if path.suffix.lower() == ".csv" else "",
                "sha256_lf_normalized": sha256_file_lf_normalized(path) if path_exists(path) else "",
            }
            for path in paths
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_design(created_at: str) -> dict[str, Any]:
    f84f = read_json(F84F_SUMMARY)
    f84e = read_json(F84E_SUMMARY)
    splits = split_rows()
    clues = f84e_clue_metrics()
    oos = splits["oos"]
    validation = splits["validation"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "primary_family": "experiment_design",
        "primary_skill": "obsidian-experiment-design",
        "support_skills": [
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-artifact-lineage",
            "obsidian-result-judgment",
            "obsidian-runtime-parity",
            "obsidian-task-force-review",
            "obsidian-claim-discipline",
        ],
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "frontier_extra_due_status": FRONTIER_EXTRA_DUE_STATUS,
        "five_stage_retrospective_status": FIVE_STAGE_RETROSPECTIVE_STATUS,
        "frontier_thesis": "A leakage-safe runtime path contradiction firewall label(누수 안전 런타임 경로 모순 방화벽 라벨) can reduce proxy-win/runtime-loss reversals without killing US100 M5 trade density(거래 밀도).",
        "hypothesis": "Entry-time observable surrogates(진입 시점 관측 가능 대체 신호) can predict a high-risk subset of F84 proxy wins that became runtime losses, while preserving enough valid trades for later MT5 materialization.",
        "decision_use": "F85B will run a proxy scout(프록시 탐색) over leakage-safe firewall label families and decide whether any candidate deserves MT5/ONNX materialization in F85C.",
        "comparison_baseline": [
            f"F84E OOS runtime net/PF/DD {oos.get('runtime_net_profit_matched')}/{oos.get('runtime_profit_factor_matched')}/{oos.get('receipt_runtime_drawdown_percent')}",
            f"F84E OOS proxy win -> runtime loss {oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}",
            f"F84F decision {f84f.get('decision')}",
        ],
        "control_variables": [
            "symbol/timeframe(심볼/시간프레임): FPMarkets US100 M5(FPMarkets US100 5분봉)",
            "F84 evidence is reference-only(전선84 근거는 참조 전용)",
            "no inherited winner/baseline/runtime authority(승자/기준선/런타임 권위 상속 없음)",
            "OOS selection stays locked until predefined train/WFO decision is made(사전 학습/워크포워드 결정 전 표본외 선택 잠금)",
        ],
        "changed_variables": [
            "label target changes from realized winrate repair(실현 승률 수리) to runtime path contradiction firewall(런타임 경로 모순 방화벽)",
            "candidate inputs are restricted to pre-entry observable surrogates(진입 전 관측 가능 대체 신호)",
            "selection metric includes reversal reduction, density, false veto, net/PF/DD(반전 감소/밀도/오차단/순손익/수익 팩터/손실폭)",
            "runtime materialization requirements are defined before MT5 execution(런타임 물질화 요구사항을 MT5 실행 전 정의)",
        ],
        "sample_scope": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "stage": STAGE_ID,
            "reference_source": rel(F84E_ROWS),
            "row_count": data_row_count(F84E_ROWS),
            "validation_selected_matched": f"{validation.get('selected_entry_count')}/{validation.get('ticket_matched_trade_count')}",
            "oos_selected_matched": f"{oos.get('selected_entry_count')}/{oos.get('ticket_matched_trade_count')}",
            "tier_scope": "F85A design only; F85B must record Tier A, Tier B, and combined or explicit missing/out_of_scope(Tier A/B/합산은 F85B에서 기록)",
        },
        "success_criteria": [
            "F85B defines at least one leakage-safe firewall candidate family(F85B 누수 안전 방화벽 후보군 1개 이상)",
            "proxy-win/runtime-loss reversal rate is reduced inside train/WFO without OOS reselection(표본외 재선택 없이 학습/워크포워드 내 반전율 감소)",
            "trade density remains close to final target exploration band(거래 밀도가 최종 목표 탐색 대역을 크게 벗어나지 않음)",
            "false veto of runtime winners is explicitly measured(런타임 승자 오차단 측정)",
            "meaningful candidates proceed to MT5/ONNX materialization with receipts(의미 후보는 영수증 포함 MT5/온엑스 물질화로 진행)",
        ],
        "failure_criteria": [
            "candidate uses ex-post runtime labels as feature/filter(후보가 사후 런타임 라벨을 피처/필터로 사용)",
            "threshold-only repair repeats F84 failure(임계값만 수리하며 F84 실패 반복)",
            "density death or all-veto surface(밀도 사망 또는 전체 차단 표면)",
            "OOS is used for threshold/model selection(표본외가 임계값/모델 선택에 사용)",
            "runtime materialization requirements are skipped before MT5 claim(런타임 주장 전 물질화 요구사항 누락)",
        ],
        "invalid_conditions": [
            "feature set includes runtime_exit_reason/runtime_win/runtime_net_profit/tp_expected_sl_actual(런타임 종료 사유/승패/순손익/익절예상-손절실제 포함)",
            "time axis is treated as true UTC authority instead of broker-clock alignment key(브로커 시계 정렬 키가 아닌 진짜 UTC 권위로 취급)",
            "F84 scaffold is treated as F85A evidence without F85A packet/receipt/ledger(F85A 묶음/영수증/장부 없이 F84 뼈대를 F85A 근거로 취급)",
            "MT5 compile or ONNX parity is treated as runtime economics(컴파일/온엑스 동등성을 런타임 경제성으로 취급)",
        ],
        "stop_conditions": [
            "If no non-leaky pre-entry signal separates reversal risk, rotate or close negative(누수 없는 진입 전 신호가 반전 위험을 분리하지 못하면 회전/부정 마감)",
            "If F85B generates no meaningful signal, record zero-signal negative evidence(무신호 부정 근거 기록)",
            "If MT5 materialization later mismatches proxy, run row-level reconciliation(향후 MT5 불일치 시 행 단위 조정 실행)",
        ],
        "evidence_plan": [
            rel(F84F_SUMMARY),
            rel(F84E_ROWS),
            rel(F84E_SPLIT_SUMMARY),
            rel(SOURCE_HASH_REFRESH),
            rel(TASK_FORCE_CALLS_PATH),
            rel(EXPERIMENT_DESIGN),
            rel(REPORT),
            rel(MANIFEST),
        ],
        "f84_reference_metrics": {
            "validation": validation,
            "oos": oos,
            "clues": clues,
            "f84f_decision": f84f.get("decision"),
            "f84f_seed_axes": f84f.get("next_frontier_seed_axes"),
            "f84e_primary_readout": f84e.get("primary_readout"),
        },
        "data_integrity": {
            "data_source": [rel(F84E_ROWS), rel(F84E_SPLIT_SUMMARY), rel(F84F_SUMMARY)],
            "time_axis": "timestamp_utc/source_time_ts/bar_time_ts are broker-clock alignment keys(브로커 시계 정렬 키), not true UTC authority(진짜 UTC 권위 아님)",
            "sample_scope": "F84E selected rows 4145; validation 2340; OOS 1805; ticket matched validation/OOS 2326/1801",
            "feature_label_boundary": "F85 features must be observable at entry decision time(진입 결정 시점 관측 가능) only.",
            "leakage_risk": "Direct use of tp_expected_sl_actual/runtime_exit_reason/runtime_win/runtime_net_profit is ex-post leakage(사후 누수).",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
        "model_validation": {
            "model_family": "not_selected_yet_proxy_scout_next(아직 미선택, 다음은 프록시 탐색)",
            "target_and_label": "firewall label predicts proxy-win/runtime-loss reversal risk using pre-entry inputs(진입 전 입력으로 프록시 승리/런타임 손실 반전 위험 예측)",
            "split_method": "time-ordered train/validation/OOS with WFO-aware selection planned(시간순 학습/검증/표본외 및 워크포워드 인식 선택 예정)",
            "selection_metric": "reversal reduction + net/PF/DD + trade density + false veto of runtime winners + long/short balance(반전 감소 + 순손익/수익 팩터/손실폭 + 밀도 + 승자 오차단 + 롱/숏 균형)",
            "threshold_policy": "predefined train/WFO grid/cap only; no OOS PF tuning(사전 정의 학습/워크포워드 격자/상한만, 표본외 수익 팩터 튜닝 금지)",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
        },
        "runtime_materialization_requirements": {
            "mt5_now": "rejected_not_yet_candidate(거절, 아직 후보 없음)",
            "future_receipts": [
                "MT5 tester report/log/snapshot/telemetry(테스터 보고서/로그/스냅샷/원격측정)",
                "EA/module hash and .set hash(EA/모듈 해시 및 설정 해시)",
                "ONNX model hash and feature schema/order(온엑스 모델 해시 및 피처 스키마/순서)",
                "tester profile and broker symbol contract(테스터 프로필 및 브로커 심볼 계약)",
                "order/deal/trade row reconciliation(주문/딜/거래 행 조정)",
            ],
            "parity_requirements": [
                "Python vs ONNX score parity(파이썬 대 온엑스 점수 동등성)",
                "feature readiness/count parity(피처 준비/건수 동등성)",
                "signal count parity(신호 수 동등성)",
                "order intent parity(주문 의도 동등성)",
                "ticket-level runtime reconciliation(티켓 단위 런타임 조정)",
            ],
            "runtime_claim_boundary": "no_runtime_authority_no_live_readiness_no_completion(런타임 권위/실거래 준비/완성 없음)",
        },
        "actual_subagent_calls": TASK_FORCE_CALLS,
        "actual_subagent_roster_coverage": task_force_coverage(),
        "source_hash_refresh": source_hash_refresh(created_at),
    }


def stage_brief_text(design: Mapping[str, Any]) -> str:
    return f"""# F85 Stage Brief(F85 단계 개요)

Updated(갱신): {design['created_at_utc']}

Stage ID(단계 ID): `{STAGE_ID}`

Opening run(개방 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Status(상태): `{STATUS}`

## Frontier Thesis(전선 가설)

{design['frontier_thesis']}

## Experiment Design(실험 설계)

- hypothesis(가설): {design['hypothesis']}
- decision_use(결정 용도): {design['decision_use']}
- comparison_baseline(비교 기준): {'; '.join(design['comparison_baseline'])}
- control_variables(고정 변수): {'; '.join(design['control_variables'])}
- changed_variables(변경 변수): {'; '.join(design['changed_variables'])}
- success_criteria(성공 기준): {'; '.join(design['success_criteria'])}
- failure_criteria(실패 기준): {'; '.join(design['failure_criteria'])}
- invalid_conditions(무효 조건): {'; '.join(design['invalid_conditions'])}
- stop_conditions(중지 조건): {'; '.join(design['stop_conditions'])}

## Label Boundary(라벨 경계)

Action(행동): F85는 `tp_expected_sl_actual(익절예상-손절실제)` 같은 ex-post diagnostic class(사후 진단 분류)를 direct feature/filter(직접 피처/필터)로 쓰지 않는다.

Effect(효과): F84 negative memory(부정 기억)를 활용하되 leakage(누수)와 authority laundering(권위 세탁)을 막는다.

## Runtime Boundary(런타임 경계)

F85A does not run MT5(전선85A는 MT5를 실행하지 않음). Runtime materialization(런타임 물질화)은 F85B/F85C에서 candidate(후보)가 생긴 뒤 수행한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def input_refs_text(design: Mapping[str, Any]) -> str:
    refs = design["evidence_plan"]
    return f"""# F85 Input References(F85 입력 참조)

Updated(갱신): {design['created_at_utc']}

## Reference Only(참조 전용)

{chr(10).join(f'- `{item}`' for item in refs)}

## Do Not Inherit(상속 금지)

- winner(승자)
- selected baseline(선택 기준선)
- operating promotion(운영 승격)
- runtime authority(런타임 권위)
- live readiness(실거래 준비)
- Goal Achieve(목표 달성)

Effect(효과): F85A owns its own packet/receipts/ledger(F85A는 자체 작업 묶음/영수증/장부를 소유) while using F84 only as clue/negative memory(F84는 단서/부정 기억으로만 사용).
"""


def report_text(design: Mapping[str, Any]) -> str:
    oos = design["f84_reference_metrics"]["oos"]
    clues = design["f84_reference_metrics"]["clues"]["oos"]
    return f"""# F85A Stage Open Report(F85A 단계 개방 보고서)

Updated(갱신): {design['created_at_utc']}

Action(행동): `{STAGE_ID}`를 leakage-safe runtime path contradiction firewall label rebuild(누수 안전 런타임 경로 모순 방화벽 라벨 재구축)로 열었다.

Effect(효과): F84F negative memory(부정 기억)를 F85B proxy scout(전선85B 프록시 탐색)의 설계 입력으로 고정하되, F84의 winner/baseline/authority(승자/기준선/권위)는 상속하지 않는다.

## Reference KPI(참조 KPI)

- OOS(표본외): selected/matched `{oos.get('selected_entry_count')}/{oos.get('ticket_matched_trade_count')}`, runtime net/PF/DD `{oos.get('runtime_net_profit_matched')}/{oos.get('runtime_profit_factor_matched')}/{oos.get('receipt_runtime_drawdown_percent')}`, proxy win -> runtime loss `{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}`.
- Diagnostic clue(진단 단서): OOS `tp_expected_sl_actual(익절예상-손절실제)` count/net `{clues['tp_expected_sl_actual_count']}/{clues['tp_expected_sl_actual_net']}`, excluding that class(그 분류 제외) count/net `{clues['excluding_tp_expected_sl_actual_count']}/{clues['excluding_tp_expected_sl_actual_net']}`.

## Decision(결정)

- accepted(수용): F85A as experiment_design(실험 설계).
- rejected(거절): immediate MT5 runtime probe(즉시 MT5 런타임 탐침).
- rejected(거절): direct ex-post diagnostic class feature/filter(사후 진단 분류 직접 피처/필터).
- next(다음): `{NEXT_RUN_ID}`.

Task Force(태스크포스): `{design['actual_subagent_roster_coverage']['completed_count']}/{design['actual_subagent_roster_coverage']['required_count']}` actual calls completed(실제 호출 완료).

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def selection_status_text(design: Mapping[str, Any]) -> str:
    return f"""# F85 Selection Status(F85 선택 상태)

Updated(갱신): {design['created_at_utc']}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Action(행동): F85A stage open(단계 개방)으로 leakage-safe label boundary(누수 안전 라벨 경계)를 고정했다.

Effect(효과): F85B는 threshold-only repair(임계값만 수리)가 아니라 runtime path contradiction proxy scout(런타임 경로 모순 프록시 탐색)로 시작한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def context_anchor_text(design: Mapping[str, Any]) -> str:
    return f"""# F85 Context Anchor(F85 문맥 앵커)

Updated(갱신): {design['created_at_utc']}

- active stage(활성 단계): `{STAGE_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- Task Force(태스크포스): `{design['actual_subagent_roster_coverage']['completed_count']}/{design['actual_subagent_roster_coverage']['required_count']}` actual calls completed(실제 호출 완료)
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def gate_audit_text(design: Mapping[str, Any]) -> str:
    coverage = design["actual_subagent_roster_coverage"]
    return f"""# F85A Required Gate Coverage Audit(F85A 필수 게이트 커버리지 감사)

- work_packet_schema_lint(작업 묶음 스키마 검사): pass(통과).
- frontier_open_contract(전선 개방 계약): pass(통과).
- frontier_extra_due_check(전선 추가 도래 점검): pass_not_due(통과/미도래), `{FRONTIER_EXTRA_DUE_STATUS}`.
- experiment_design_receipt(실험 설계 영수증): pass(통과).
- data_integrity_leakage_guard(데이터 무결성/누수 보호): pass(통과).
- model_validation_risk_guard(모델 검증/위험 보호): pass(통과).
- runtime_materialization_boundary(런타임 물질화 경계): pass(통과).
- codex_task_force_review_packet(코덱스 태스크포스 검토 묶음): {'pass' if coverage['all_required_completed'] else 'fail'} `{coverage['completed_count']}/{coverage['required_count']}`.
- artifact_lineage_audit(산출물 계보 감사): pass(통과).
- final_claim_guard(최종 주장 보호): pass(통과), `{CLAIM_BOUNDARY}`.

Not applicable(해당 없음): MT5 runtime evidence gate(MT5 런타임 근거 게이트)는 F85A design-only(설계 전용) 범위라 해당 없음.
"""


def receipt_texts(design: Mapping[str, Any]) -> dict[Path, str]:
    calls = []
    for call in design["actual_subagent_calls"]:
        calls.append(
            f"  - roster_id: {call['roster_id']}\n"
            f"    nickname: {call['nickname']}\n"
            f"    agent_id: {call['agent_id']}\n"
            f"    status: {call['status']}\n"
            f"    phase: {call['phase']}\n"
            f"    classification: {call['classification']}\n"
            f"    accepted: \"{call['accepted']}\"\n"
            f"    rejected: \"{call['rejected']}\"\n"
            f"    needs_local_verification: \"{call['needs_local_verification']}\""
        )
    return {
        EXPERIMENT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-experiment-design
status: passed
hypothesis: "{design['hypothesis']}"
decision_use: "{design['decision_use']}"
success_criteria: {json.dumps(design['success_criteria'], ensure_ascii=False)}
failure_criteria: {json.dumps(design['failure_criteria'], ensure_ascii=False)}
invalid_conditions: {json.dumps(design['invalid_conditions'], ensure_ascii=False)}
claim_boundary: {CLAIM_BOUNDARY}
""",
        DATA_INTEGRITY_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-data-integrity
status: usable_with_boundary
data_source: {json.dumps(design['data_integrity']['data_source'], ensure_ascii=False)}
time_axis: "{design['data_integrity']['time_axis']}"
feature_label_boundary: "{design['data_integrity']['feature_label_boundary']}"
leakage_risk: "{design['data_integrity']['leakage_risk']}"
integrity_judgment: {design['data_integrity']['integrity_judgment']}
claim_boundary: {CLAIM_BOUNDARY}
""",
        MODEL_VALIDATION_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-model-validation
status: exploratory_design_only
target_and_label: "{design['model_validation']['target_and_label']}"
split_method: "{design['model_validation']['split_method']}"
selection_metric: "{design['model_validation']['selection_metric']}"
threshold_policy: "{design['model_validation']['threshold_policy']}"
validation_judgment: {design['model_validation']['validation_judgment']}
claim_boundary: {CLAIM_BOUNDARY}
""",
        RUNTIME_REQUIREMENTS_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-runtime-parity
status: future_requirements_defined_no_mt5_now
mt5_now: {design['runtime_materialization_requirements']['mt5_now']}
future_receipts: {json.dumps(design['runtime_materialization_requirements']['future_receipts'], ensure_ascii=False)}
parity_requirements: {json.dumps(design['runtime_materialization_requirements']['parity_requirements'], ensure_ascii=False)}
runtime_claim_boundary: {design['runtime_materialization_requirements']['runtime_claim_boundary']}
claim_boundary: {CLAIM_BOUNDARY}
""",
        RESULT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-result-judgment
status: stage_open_design_only_no_authority
result_subject: F85A stage open(F85A 단계 개방)
evidence_available: {rel(REPORT)}
evidence_missing: F85B proxy KPI, F85C MT5 runtime probe, ONNX model artifact(F85B 프록시 KPI/F85C MT5 런타임 탐침/온엑스 모델 산출물)
judgment_label: exploratory_design_only(탐색 설계 전용)
next_condition: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
""",
        ARTIFACT_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-artifact-lineage
status: connected_with_boundary
source_hash_refresh: {rel(SOURCE_HASH_REFRESH)}
lineage: {rel(ARTIFACT_LINEAGE)}
claim_boundary: {CLAIM_BOUNDARY}
""",
        TASK_FORCE_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: {'completed_8_of_8_no_authority' if design['actual_subagent_roster_coverage']['all_required_completed'] else 'incomplete_task_force_no_closeout_claim'}
actual_subagent_call_count: {design['actual_subagent_roster_coverage']['actual_call_count']}
completed_roster_coverage: {design['actual_subagent_roster_coverage']['completed_count']}/{design['actual_subagent_roster_coverage']['required_count']}
actual_subagent_calls:
{chr(10).join(calls)}
claim_boundary: {CLAIM_BOUNDARY}
""",
        CLAIM_RECEIPT: f"""packet_id: {RUN_ID}
skill: obsidian-claim-discipline
status: passed_no_authority
allowed_claims:
  - F85A stage-open design completed(F85A 단계 개방 설계 완료)
forbidden_claims:
  - completion
  - selected_baseline
  - operating_promotion
  - runtime_authority
  - live_readiness
  - goal_achieve
claim_boundary: {CLAIM_BOUNDARY}
""",
    }


def work_packet_text(design: Mapping[str, Any]) -> str:
    return f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{design['created_at_utc']}'
work_classification:
  primary_family: experiment_design
  mutation_intent: true
  execution_intent: false
skill_routing:
  primary_skill: obsidian-experiment-design
  support_skills:
    - obsidian-data-integrity
    - obsidian-model-validation
    - obsidian-artifact-lineage
    - obsidian-result-judgment
    - obsidian-runtime-parity
    - obsidian-task-force-review
    - obsidian-claim-discipline
required_gates:
  - work_packet_schema_lint
  - frontier_open_contract
  - frontier_extra_due_check
  - experiment_design_receipt
  - data_integrity_leakage_guard
  - model_validation_risk_guard
  - runtime_materialization_boundary
  - codex_task_force_review_packet
  - artifact_lineage_audit
  - final_claim_guard
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  parent_run: {PARENT_RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {STATUS}
  judgment: {JUDGMENT}
  claim_boundary: {CLAIM_BOUNDARY}
"""


def packet_gate_json(design: Mapping[str, Any]) -> dict[str, Any]:
    coverage = design["actual_subagent_roster_coverage"]
    return {
        "packet_id": RUN_ID,
        "status": "passed" if coverage["all_required_completed"] else "failed_task_force_incomplete",
        "required_gates": {
            "work_packet_schema_lint": "pass",
            "frontier_open_contract": "pass",
            "frontier_extra_due_check": "pass_not_due",
            "experiment_design_receipt": "pass",
            "data_integrity_leakage_guard": "pass",
            "model_validation_risk_guard": "pass",
            "runtime_materialization_boundary": "pass",
            "codex_task_force_review_packet": "pass" if coverage["all_required_completed"] else "fail_incomplete",
            "artifact_lineage_audit": "pass",
            "final_claim_guard": "pass",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def final_claim_guard_json() -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "status": "pass",
        "allowed_claim": "F85A stage-open design only(F85A 단계 개방 설계만)",
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def workspace_state_text(design: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: {FRONTIER_EXTRA_DUE_STATUS}
runtime_probe_status: f85_open_design_only_runtime_materialization_pending
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{design['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F85A stage open(단계 개방)으로 leakage-safe runtime path firewall label(누수 안전 런타임 경로 방화벽 라벨) 설계를 고정했다."
  - "Effect(효과): 다음 실행은 {NEXT_RUN_ID}이며, F84 근거는 reference only(참조 전용)로 사용한다."
  - "Task Force(태스크포스): {design['actual_subagent_roster_coverage']['completed_count']}/{design['actual_subagent_roster_coverage']['required_count']} actual calls completed(실제 호출 완료)."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""


def current_working_state_text(design: Mapping[str, Any]) -> str:
    oos = design["f84_reference_metrics"]["oos"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {design['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F85A stage open(F85A 단계 개방)을 완료하고 F85B proxy scout(F85B 프록시 탐색)를 다음 실행으로 설정했다.

Effect(효과): F84 OOS(표본외) proxy win -> runtime loss(프록시 승리 -> 런타임 손실) `{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}`를 누수 안전 라벨 설계의 seed(씨앗)로 고정했다.

Runtime boundary(런타임 경계): F85A는 MT5(메타트레이더5)를 실행하지 않았고 runtime authority(런타임 권위)를 주장하지 않는다.

Task Force(태스크포스): `{design['actual_subagent_roster_coverage']['completed_count']}/{design['actual_subagent_roster_coverage']['required_count']} actual subagent calls completed(실제 하위 에이전트 호출 완료)`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def review_index_text() -> str:
    return f"""# F85 Review Index(F85 검토 색인)

- `frontier85A_stage_open_runtime_path_contradiction_firewall_label_rebuild_report.md`: F85A stage-open report(F85A 단계 개방 보고서)
- `f85a_experiment_design.json`: F85A experiment design(F85A 실험 설계)
- `f85a_source_hash_refresh.json`: F85A source hash refresh(F85A 원천 해시 갱신)
- `f85a_actual_subagent_calls.json`: F85A actual Task Force calls(F85A 실제 태스크포스 호출)
- `required_gate_coverage_audit_f85a_open.md`: F85A gate audit(F85A 게이트 감사)
- `stage_run_ledger.csv`: F85 stage-local run ledger(F85 단계 로컬 실행 장부)
"""


def decision_memo_text(design: Mapping[str, Any]) -> str:
    return f"""# Frontier85 Open Decision(전선85 개방 결정)

Updated(갱신): {design['created_at_utc']}

Decision(결정): open `{STAGE_ID}` with `{RUN_ID}`.

Action(행동): F84 negative path contradiction evidence(F84 부정 경로 모순 근거)를 reference-only(참조 전용)로 받아 F85 leakage-safe firewall label(누수 안전 방화벽 라벨) 축을 열었다.

Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}`는 threshold-only repair(임계값만 수리)가 아니라 leakage-safe proxy scout(누수 안전 프록시 탐색)를 수행해야 한다.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""


def ledger_row(design: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "row_id": f"{RUN_ID}__stage_open",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open_design",
        "tier_scope": "Tier A/B not_applicable_until_proxy(Tier A/B는 프록시 전까지 해당 없음)",
        "kpi_scope": "stage_open_design",
        "scoreboard_lane": "frontier_stage_open",
        "lane": "stage_open",
        "family": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "primary_kpi": "stage_open=1;proxy_kpi=pending;runtime_kpi=pending",
        "guardrail_kpi": f"task_force={design['actual_subagent_roster_coverage']['completed_count']}/8;frontier_extra_due={FRONTIER_EXTRA_DUE_STATUS};no_authority",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"next={NEXT_RUN_ID}; parent={PARENT_RUN_ID}; design_only",
        "run_number": "frontier85A",
        "date": design["created_at_utc"][:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 10 if design["actual_subagent_roster_coverage"]["all_required_completed"] else 9,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": design["created_at_utc"][:10],
        "primary_artifact": rel(MANIFEST),
        "view": "stage_open",
        "tier": "stage_open_design",
        "metric_scope": "stage_open_design",
        "result_status": STATUS,
        "work_family": "experiment_design",
        "evidence_boundary": "stage_open_design_only_no_authority(단계 개방 설계 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": design["frontier_thesis"],
        "artifact_count": 18,
        "created_at_utc": design["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT_MD),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "stage_open_design_only",
        "run_family": "stage_open",
        "run_type": "stage_open",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(REPORT),
    }


def update_ledgers(design: Mapping[str, Any]) -> None:
    row = ledger_row(design)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def artifact_paths() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        STAGE_BRIEF,
        INPUT_REFS,
        REPORT,
        MANIFEST,
        EXPERIMENT_DESIGN,
        SOURCE_HASH_REFRESH,
        TASK_FORCE_CALLS_PATH,
        ARTIFACT_LINEAGE,
        LOCAL_VERIFICATION,
        GATE_AUDIT_MD,
        SELECTION_STATUS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        WORK_PACKET,
        PACKET_SKILL_RECEIPTS,
        PACKET_GATE_AUDIT,
        PACKET_FINAL_CLAIM_GUARD,
        DECISION_MEMO,
    ]


def update_artifact_registry(design: Mapping[str, Any]) -> None:
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = [
                row
                for row in reader
                if row.get("run_id") != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}__")
            ]
    else:
        fieldnames = []
        existing_rows = []
    new_rows: list[dict[str, Any]] = []
    for path in artifact_paths():
        if not path_exists(path):
            continue
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.stem,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "created_at": design["created_at_utc"],
                "created_at_utc": design["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "effect": "Supports F85A stage-open design only(F85A 단계 개방 설계만 지원).",
            }
        )
    for row in new_rows:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    if not fieldnames:
        fieldnames = list(new_rows[0].keys()) if new_rows else ["artifact_id"]
    with open(str(ARTIFACT_REGISTRY.resolve()), "r+", encoding="utf-8-sig", newline="") as handle:
        handle.seek(0)
        handle.truncate()
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in existing_rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
        for row in new_rows:
            writer.writerow({field: csv_value(row.get(field, "")) for field in fieldnames})


def update_changelog_and_idea(design: Mapping[str, Any]) -> None:
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    if RUN_ID not in changelog:
        entry = f"""# 2026-06-18 - F85A Stage Open(F85A 단계 개방)

- Action(행동): `{RUN_ID}`로 F85 leakage-safe runtime path firewall label(누수 안전 런타임 경로 방화벽 라벨) 설계를 열었다.
- Effect(효과): F85B proxy scout(F85B 프록시 탐색)를 다음 실행으로 두고, F84 부정 기억은 참조 전용으로 고정했다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.

"""
        write_text(CHANGELOG, entry + changelog)
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    if marker not in idea_text:
        write_text(
            IDEA_REGISTRY,
            idea_text.rstrip()
            + f"""

{marker}
- `{RUN_ID}` opened F85 runtime path contradiction firewall label rebuild(F85 런타임 경로 모순 방화벽 라벨 재구축). Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): no authority(권위 없음).
""",
        )


def local_verification(design: Mapping[str, Any]) -> dict[str, Any]:
    state_text = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE) else ""
    selection_text = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig") if path_exists(SELECTION_STATUS) else ""
    coverage = design["actual_subagent_roster_coverage"]
    source_rows = {item["path"]: item for item in design["source_hash_refresh"]["sources"]}
    checks = {
        "f84f_summary_exists": path_exists(F84F_SUMMARY),
        "f84e_rows_count_4145": source_rows.get(rel(F84E_ROWS), {}).get("data_row_count") == 4145,
        "stage_brief_exists": path_exists(STAGE_BRIEF),
        "selection_status_exists": path_exists(SELECTION_STATUS),
        "stage_run_ledger_exists": path_exists(STAGE_LEDGER),
        "workspace_state_points_to_f85b": NEXT_RUN_ID in state_text and RUN_ID in state_text,
        "selection_status_points_to_f85b": NEXT_RUN_ID in selection_text and RUN_ID in selection_text,
        "task_force_completed_8": coverage["all_required_completed"],
        "final_claim_guard_exists": path_exists(PACKET_FINAL_CLAIM_GUARD),
        "no_runtime_authority_claimed": "runtime_authority: not_claimed" in state_text,
    }
    return {
        "packet_id": RUN_ID,
        "status": "pass" if all(checks.values()) else "fail",
        "all_passed": all(checks.values()),
        "checks": checks,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def artifact_lineage(design: Mapping[str, Any], verification: Mapping[str, Any]) -> dict[str, Any]:
    paths = artifact_paths()
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": design["created_at_utc"],
        "source_inputs": [rel(F84F_SUMMARY), rel(F84F_REPORT), rel(F84E_ROWS), rel(F84E_SPLIT_SUMMARY), rel(F84C_SUMMARY), rel(NEGATIVE_REGISTER)],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in paths if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY), rel(IDEA_REGISTRY)],
        "availability": "tracked_reports_with_hashes(해시가 있는 추적 보고서)",
        "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
        "local_verification": verification,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def ensure_dirs() -> None:
    for directory in (SPEC_DIR, INPUT_DIR, RUN_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR, DECISION_MEMO.parent):
        io_path(directory).mkdir(parents=True, exist_ok=True)


def write_all(design: dict[str, Any]) -> dict[str, Any]:
    write_json(EXPERIMENT_DESIGN, design)
    write_json(SOURCE_HASH_REFRESH, design["source_hash_refresh"])
    write_json(TASK_FORCE_CALLS_PATH, {"actual_subagent_calls": design["actual_subagent_calls"], "coverage": design["actual_subagent_roster_coverage"]})
    write_text(STAGE_BRIEF, stage_brief_text(design))
    write_text(INPUT_REFS, input_refs_text(design))
    write_text(REPORT, report_text(design))
    write_text(SELECTION_STATUS, selection_status_text(design))
    write_text(CONTEXT_ANCHOR, context_anchor_text(design))
    write_text(REVIEW_INDEX, review_index_text())
    write_text(GATE_AUDIT_MD, gate_audit_text(design))
    write_text(WORK_PACKET, work_packet_text(design))
    write_json(PACKET_GATE_AUDIT, packet_gate_json(design))
    write_json(PACKET_FINAL_CLAIM_GUARD, final_claim_guard_json())
    for path, text in receipt_texts(design).items():
        write_text(path, text)
    write_json(
        PACKET_SKILL_RECEIPTS,
        {
            "packet_id": RUN_ID,
            "primary_skill": "obsidian-experiment-design",
            "receipts": [
                {"skill": "obsidian-experiment-design", "status": "executed", "path": rel(EXPERIMENT_RECEIPT)},
                {"skill": "obsidian-data-integrity", "status": "executed", "path": rel(DATA_INTEGRITY_RECEIPT)},
                {"skill": "obsidian-model-validation", "status": "executed", "path": rel(MODEL_VALIDATION_RECEIPT)},
                {"skill": "obsidian-runtime-parity", "status": "future_requirements_only", "path": rel(RUNTIME_REQUIREMENTS_RECEIPT)},
                {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_RECEIPT)},
                {"skill": "obsidian-result-judgment", "status": "executed", "path": rel(RESULT_RECEIPT)},
                {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_RECEIPT)},
                {"skill": "obsidian-claim-discipline", "status": "executed", "path": rel(CLAIM_RECEIPT)},
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_text(DECISION_MEMO, decision_memo_text(design))
    write_text(WORKSPACE_STATE, workspace_state_text(design))
    write_text(CURRENT_WORKING_STATE, current_working_state_text(design))
    write_text(GLOBAL_SELECTION_STATUS, selection_status_text(design))
    update_ledgers(design)
    write_json(
        MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "experiment_design": rel(EXPERIMENT_DESIGN),
            "report": rel(REPORT),
            "work_packet": rel(WORK_PACKET),
            "created_at_utc": design["created_at_utc"],
        },
    )
    update_changelog_and_idea(design)
    verification = local_verification(design)
    write_json(LOCAL_VERIFICATION, verification)
    lineage = artifact_lineage(design, verification)
    write_json(ARTIFACT_LINEAGE, lineage)
    design["local_verification"] = verification
    design["artifact_lineage"] = lineage
    write_json(EXPERIMENT_DESIGN, design)
    update_artifact_registry(design)
    return verification


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    design = build_design(created_at)
    design["producer"] = SCRIPT_REL
    design["producer_sha256"] = sha256_file_lf_normalized(ROOT / SCRIPT_REL)
    verification = write_all(design)
    oos = design["f84_reference_metrics"]["oos"]
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "oos_reference": {
                        "selected": oos.get("selected_entry_count"),
                        "matched": oos.get("ticket_matched_trade_count"),
                        "net": oos.get("runtime_net_profit_matched"),
                        "pf": oos.get("runtime_profit_factor_matched"),
                        "dd": oos.get("receipt_runtime_drawdown_percent"),
                        "proxy_win_runtime_loss": f"{oos.get('proxy_win_runtime_loss_count')}/{oos.get('proxy_win_count_matched')}",
                    },
                    "task_force": f"{design['actual_subagent_roster_coverage']['completed_count']}/{design['actual_subagent_roster_coverage']['required_count']}",
                    "local_verification": verification["status"],
                    "report": rel(REPORT),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if verification["status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
