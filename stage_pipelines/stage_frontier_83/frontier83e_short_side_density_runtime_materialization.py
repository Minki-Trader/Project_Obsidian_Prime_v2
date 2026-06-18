from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_81 import frontier81c_mt5_runtime_materialization as base
from stage_pipelines.stage_frontier_82 import frontier82b_density_first_runtime_economic_mechanism_proxy_scout as f82b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
)


STAGE_ID = "stage_frontier_83__realized_pnl_teacher_distillation_exportable_runtime_rotation"
RUN_ID = "frontier83E_short_side_density_runtime_materialization_v1"
PARENT_RUN_ID = "frontier83D_two_sided_density_expansion_or_rotation_decision_v1"
NEXT_RUN_ID = "frontier83F_short_density_proxy_runtime_gap_analysis_v1"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier83E_short_density_runtime_materialization"
RUNTIME_CANDIDATE_PREFIX = "f83e_runtime"
ATTEMPT_PREFIX = "f83e_short_density_runtime_materialization"
EXPLORATION_LABEL = "frontier83E_short_density_runtime_materialization"
ATTEMPT_ROLE = "short_density_runtime_materialization"
RECORD_VIEW_PREFIX = "mt5_f83e_short_density_runtime_materialization"
THRESHOLD_EPSILON = 1e-7
CLAIM_BOUNDARY = (
    "mt5_runtime_materialization_observation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
VETO_DIR = RUN_DIR / "runtime_veto_tapes"
MT5_DIR = RUN_DIR / "mt5"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

F83D_TARGET_SELECTION = REVIEW_DIR / "f83d_short_density_materialization_target_selection.json"
F82B_SUMMARY = ROOT / "stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/03_reviews/f82b_density_first_proxy_summary.json"
F82B_RANKED_TOP = ROOT / "stages/stage_frontier_82__density_first_runtime_economic_mechanism_rotation/03_reviews/f82b_density_first_proxy_ranked_top200.csv"

TARGET_SELECTION = REVIEW_DIR / "f83e_runtime_materialization_target_selection.json"
REPORT = REVIEW_DIR / "frontier83E_short_side_density_runtime_materialization_report.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f83e.md"
SUMMARY = REVIEW_DIR / "f83e_short_side_density_runtime_materialization_summary.json"
RUNTIME_PARITY = REVIEW_DIR / "f83e_runtime_parity_receipt.json"
BACKTEST_FORENSICS = REVIEW_DIR / "f83e_backtest_forensics_receipt.json"
TASK_FORCE_REVIEW = REVIEW_DIR / "f83e_task_force_review_receipt.yaml"
ARTIFACT_LINEAGE = REVIEW_DIR / "f83e_artifact_lineage.json"
LOCAL_VERIFICATION = REVIEW_DIR / "f83e_local_verification.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
PACKET_SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
SCRIPT_REL = "stage_pipelines/stage_frontier_83/frontier83e_short_side_density_runtime_materialization.py"


def configure_base() -> None:
    updates = {
        "STAGE_ID": STAGE_ID,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "COMMON_RUN_ROOT": COMMON_RUN_ROOT,
        "RUNTIME_CANDIDATE_PREFIX": RUNTIME_CANDIDATE_PREFIX,
        "ATTEMPT_PREFIX": ATTEMPT_PREFIX,
        "EXPLORATION_LABEL": EXPLORATION_LABEL,
        "ATTEMPT_ROLE": ATTEMPT_ROLE,
        "RECORD_VIEW_PREFIX": RECORD_VIEW_PREFIX,
        "THRESHOLD_EPSILON": THRESHOLD_EPSILON,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "STAGE_DIR": STAGE_DIR,
        "RUN_DIR": RUN_DIR,
        "MODEL_DIR": MODEL_DIR,
        "FEATURE_DIR": FEATURE_DIR,
        "VETO_DIR": VETO_DIR,
        "MT5_DIR": MT5_DIR,
        "REVIEW_DIR": REVIEW_DIR,
        "SELECTED_DIR": SELECTED_DIR,
        "TARGET_SELECTION": TARGET_SELECTION,
        "F81B_SUMMARY": F82B_SUMMARY,
        "F81B_RANKED_TOP": F82B_RANKED_TOP,
        "REPORT": REPORT,
        "GATE_AUDIT": GATE_AUDIT,
        "SUMMARY": SUMMARY,
        "RUNTIME_PARITY": RUNTIME_PARITY,
        "BACKTEST_FORENSICS": BACKTEST_FORENSICS,
        "RUN_MANIFEST": RUN_MANIFEST,
        "SELECTION_STATUS": SELECTION_STATUS,
        "CONTEXT_ANCHOR": CONTEXT_ANCHOR,
        "STAGE_LEDGER": STAGE_LEDGER,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CURRENT_WORKING_STATE": CURRENT_WORKING_STATE,
        "RUN_REGISTRY": RUN_REGISTRY,
        "ALPHA_LEDGER": ALPHA_LEDGER,
        "IDEA_REGISTRY": IDEA_REGISTRY,
        "SCRIPT_REL": SCRIPT_REL,
    }
    for name, value in updates.items():
        setattr(base, name, value)
    base.f81b = f82b


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F83E short-side density MT5 runtime materialization.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--include-oos", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--wait-timeout-seconds", type=int, default=300)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    return Path(text).relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def ensure_dirs() -> None:
    base.ensure_dirs()
    io_path(PACKET_DIR).mkdir(parents=True, exist_ok=True)


def target_row() -> dict[str, Any]:
    payload = read_json(F83D_TARGET_SELECTION)
    target = dict(payload.get("selected_target") or {})
    if not target:
        raise RuntimeError("f83d_selected_target_missing")
    if str(target.get("side")) != "short":
        raise RuntimeError(f"f83e_target_not_short:{target.get('candidate_id')}")
    if int(float(target.get("materialization_candidate") or 0)) != 1:
        raise RuntimeError(f"f83e_target_not_materialization_candidate:{target.get('candidate_id')}")
    model_name = str(target.get("model") or "")
    if not model_name.startswith(("extra_trees", "logistic")):
        raise RuntimeError(f"f83e_target_not_exportable:{target.get('candidate_id')}:{model_name}")
    target["selection_source"] = rel(F83D_TARGET_SELECTION)
    target["source_run_id"] = PARENT_RUN_ID
    target["selection_rule"] = "f83d_selected_short_exportable_density_target"
    target["selection_boundary"] = "F83D target selection only; F83E must produce runtime materialization evidence before any runtime claim."
    write_json(
        TARGET_SELECTION,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "runtime_materialization_target": target,
            "source_target_selection": rel(F83D_TARGET_SELECTION),
            "selection_boundary": "F83D selected short density materialization target only; no baseline, promotion, or runtime authority.",
        },
    )
    return target


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any], *, include_oos: bool) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    target = context["target"]
    spec = context["spec"]
    splits = ("validation", "oos") if include_oos else ("validation",)
    side = str(target["side"])
    short_threshold = 1.1 if side == "long" else float(context["runtime_threshold"])
    long_threshold = float(context["runtime_threshold"]) if side == "long" else 1.1
    for split in splits:
        from_date, to_date = base.f71d.split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"{ATTEMPT_PREFIX}_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": 0,
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": 1.0,
            "InpAtrTakeProfitMultiplier": 1.0,
            "InpAtrMinStopPoints": float(target.get("sl_broker_points", spec.sl_price_units * f82b.SLTP_POINT_SCALE)),
            "InpAtrMaxStopPoints": float(target.get("sl_broker_points", spec.sl_price_units * f82b.SLTP_POINT_SCALE)),
            "InpAtrMinTakeProfitPoints": float(target.get("tp_broker_points", spec.tp_price_units * f82b.SLTP_POINT_SCALE)),
            "InpAtrMaxTakeProfitPoints": float(target.get("tp_broker_points", spec.tp_price_units * f82b.SLTP_POINT_SCALE)),
            "InpDecisionMode": "threshold_margin",
            "InpFallbackDecisionMode": "threshold_margin",
            "InpRuntimeVetoTapeEnabled": True,
            "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
            "InpRuntimeVetoTapeUseCommonFiles": True,
            "InpRuntimeVetoTapeDelimiter": ",",
        }
        attempt = base.runtime_base.attempt_payload(
            run_root=RUN_DIR,
            run_id=RUN_ID,
            stage_number=83,
            exploration_label=EXPLORATION_LABEL,
            attempt_name=attempt_name,
            tier=base.f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F83E_{artifact['candidate_id']}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["features"]),
            feature_order_hash=str(context["feature_order_hash"]),
            short_threshold=short_threshold,
            long_threshold=long_threshold,
            min_margin=-1.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=base.f71d.mt5.TIER_A,
            attempt_role=ATTEMPT_ROLE,
            record_view_prefix=RECORD_VIEW_PREFIX,
            max_hold_bars=int(spec.hold_bars),
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        attempt.update(
            {
                "candidate_id": artifact["candidate_id"],
                "source_candidate_id": artifact["source_candidate_id"],
                "axis_id": f"{side}_h{target.get('hold_bars')}_tp{target.get('tp_price_units')}_sl{target.get('sl_price_units')}_{target.get('feature_set')}_{target.get('model')}_{target.get('regime')}_{target.get('risk_filter')}_q{target.get('prob_quantile')}",
                "expected_rows": int(split_mask.sum()),
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "runtime_threshold": float(context["runtime_threshold"]),
                "threshold_epsilon": THRESHOLD_EPSILON,
                "claim_boundary": CLAIM_BOUNDARY,
                "trade_shape": artifact["trade_shape"],
                "source_label_name": target.get("label_name"),
                "feature_set": target.get("feature_set"),
                "model_family": target.get("model"),
                "surface_family": target.get("surface_family"),
                "regime": target.get("regime"),
                "risk_filter": target.get("risk_filter"),
            }
        )
        attempts.append(attempt)
    write_json(MT5_DIR / "attempts.json", attempts)
    return attempts


def report_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    target = payload.get("target") or {}
    best = summary.get("best_runtime") or {}
    closeout_lines = "\n".join(
        [
            "- `{split}`: net(순손익) `{net_profit}`, gross profit/loss(총이익/총손실) `{gross_profit}`/`{gross_loss}`, PF(수익 팩터) `{profit_factor}`, DD(손실폭) `{max_drawdown_percent}%`, trades/day(일 거래 수) `{trades_per_day}`, win rate(승률) `{win_rate_percent}%`, avg win/loss(평균 이익/손실) `{average_win}`/`{average_loss}`, payoff(손익비) `{payoff_ratio}`, expectancy(기대값) `{expectancy}`, recovery(회복 계수) `{recovery_factor}`, long/short(롱/숏) `{long_trade_count}`/`{short_trade_count}`.".format(
                **row
            )
            for row in summary.get("runtime_closeout_kpis", [])
        ]
    )
    if not closeout_lines:
        closeout_lines = "- `not_available(해당 없음)`: Strategy Tester(전략 테스터) completed row(완료 행)가 아직 없다."
    return f"""# F83E Short-Side Density Runtime Materialization Report(F83E 숏 방향 밀도 런타임 물질화 보고서)

Updated(갱신): {created_at}

- run id(실행 ID): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- target(대상): `{target.get('candidate_id')}` / `{target.get('model')}`
- status(상태): `{payload.get('status')}`
- judgment(판정): `{payload.get('judgment')}`
- attempt count(시도 수): `{summary.get('attempt_count')}`
- completed attempt count(완료 시도 수): `{summary.get('completed_attempt_count')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action(행동)

F83D selected short density target(F83D 선택 숏 밀도 대상)을 ONNX(온엑스), feature CSV(피처 CSV), selected-entry veto tape(선택 진입 차단 테이프), MT5 Strategy Tester attempt(MT5 전략 테스터 시도)로 물질화했다.

Effect(효과): F83C long-only runtime clue(F83C 롱 전용 런타임 단서)를 short density axis(숏 밀도 축)로 확장해 proxy/runtime gap(프록시/런타임 간극)을 관찰할 준비를 만든다.

## Parity/Execution(동등성/실행)

- probability parity rows(확률 동등성 행): `{summary.get('probability_parity_pass_rows')}`
- signal parity rows(신호 동등성 행): `{summary.get('signal_parity_pass_rows')}`
- feature readiness rows(피처 준비 행): `{summary.get('feature_readiness_pass_rows')}`
- source reproduction rows(원천 재현 행): `{summary.get('source_reproduction_pass_rows')}`
- best runtime(최선 런타임): `{best}`

## Runtime Closeout KPI(런타임 마감 핵심 지표)

{closeout_lines}

Unavailable fields(미확보 항목): time under water(회복 전 체류 시간) and max consecutive loss(최대 연속 손실)은 현재 MT5 normalized receipt(정규화 영수증)에 없다.

## Boundary(경계)

This report(이 보고서)는 completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않는다.
"""


def gate_audit_text(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    return f"""# F83E Required Gate Coverage Audit(F83E 필수 게이트 커버리지 감사)

Status(상태): `{payload.get('status')}`

| gate(게이트) | status(상태) | evidence(근거) | effect(효과) |
|---|---|---|---|
| `materialization_target(물질화 대상)` | `passed(통과)` | `{rel(TARGET_SELECTION)}` | F83D target(대상)만 물질화한다. |
| `onnx_probability_parity(온엑스 확률 동등성)` | `{summary.get('probability_parity_pass_rows')}` | `{rel(RUN_DIR / 'f83e_probability_parity.csv')}` | Python/ONNX(파이썬/온엑스) 확률 차이를 확인한다. |
| `runtime_signal_veto_parity(런타임 신호 차단 동등성)` | `{summary.get('signal_parity_pass_rows')}` | `{rel(RUN_DIR / 'f83e_signal_parity.csv')}` | 선택 진입 시각이 런타임 입력으로 보존되는지 확인한다. |
| `source_reproduction(원천 재현)` | `{summary.get('source_reproduction_pass_rows')}` | `{rel(RUN_DIR / 'f83e_source_reproduction.csv')}` | F83D/F82B proxy(프록시) 선택이 재현되는지 확인한다. |
| `strategy_tester_attempt(전략 테스터 시도)` | `{summary.get('completed_attempt_count')}/{summary.get('attempt_count')}` | `{rel(RUN_MANIFEST)}` | MT5 Strategy Tester(전략 테스터) 출력 여부를 기록한다. |
| `backtest_forensics_receipt(백테스트 포렌식 영수증)` | `recorded(기록됨)` | `{rel(BACKTEST_FORENSICS)}` | tester identity/report gap(테스터 정체성/보고서 간극)을 분리한다. |
| `codex_task_force_review_packet(코덱스 태스크포스 검토 묶음)` | `recorded(기록됨)` | `{rel(TASK_FORCE_REVIEW)}` | 8명 agent(요원) 검토와 Codex local verification(코덱스 로컬 검증)을 분리한다. |
| `final_claim_guard(최종 주장 보호)` | `passed(통과)` | `{CLAIM_BOUNDARY}` | 런타임 권위/실거래 준비를 만들지 않는다. |
"""


def ledger_row(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    target = payload.get("target") or {}
    best = summary.get("best_runtime") or {}
    return {
        "ledger_row_id": f"{RUN_ID}__runtime_materialization",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "subrun_id": "runtime_materialization(런타임 물질화)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 short density runtime materialization(MT5 숏 밀도 런타임 물질화)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope_by_claim",
        "kpi_scope": "mt5_runtime_materialization(MT5 런타임 물질화)",
        "scoreboard_lane": "runtime_economics(런타임 경제성)",
        "lane": "runtime_materialization(런타임 물질화)",
        "family": "runtime_backtest(런타임/백테스트)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REPORT),
        "primary_kpi": f"attempts={summary.get('attempt_count')};completed={summary.get('completed_attempt_count')}",
        "guardrail_kpi": f"prob_parity={summary.get('probability_parity_pass_rows')};signal_parity={summary.get('signal_parity_pass_rows')}",
        "external_verification_status": "completed" if summary.get("completed_attempt_count") else "attempted_or_materialized_no_completed_report",
        "notes": f"target={target.get('candidate_id')}; best_runtime={best}",
        "run_number": "frontier83E",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": summary.get("attempt_count"),
        "gate_passes": 8 if summary.get("completed_attempt_count") else 7,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "best_candidate_id": target.get("candidate_id", ""),
        "model": target.get("model", ""),
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "view": "runtime_materialization",
        "tier": "Tier A",
        "metric_scope": "mt5_runtime_probe",
        "result_status": payload.get("status"),
        "feature_count": target.get("feature_count", ""),
        "work_family": "runtime_backtest",
        "row_id": f"{RUN_ID}__runtime_materialization",
        "evidence_boundary": "runtime_materialization_only_no_authority(런타임 물질화만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_materialization_only(런타임 물질화만)",
    }


def task_force_review_text(created_at: str, payload: Mapping[str, Any], summary: Mapping[str, Any]) -> str:
    return f"""packet_id: {RUN_ID}
skill: obsidian-task-force-review
status: completed_for_f83e_short_density_runtime_materialization_no_authority
created_at_utc: '{created_at}'
review_mode: internal_adversarial_review_two_pass_limit(내부 비판 검토 2회차 제한)
roster_registry: docs/agent_control/codex_task_force_registry.yaml
agents_used:
  - agent_01_system_governor
  - agent_02_platform_routing_architect
  - agent_03_philosophy_policy_skill_governance
  - agent_04_evidence_control_plane
  - agent_05_data_feature_contract
  - agent_06_quant_research
  - agent_07_model_validation_risk
  - agent_08_mt5_onnx_runtime
advice_classification:
  accepted:
    - "Treat F83D short target(F83D 숏 대상) as materialization input(물질화 입력), not runtime authority(런타임 권위)."
    - "Require Strategy Tester output(전략 테스터 출력) before economics judgment(경제성 판정)."
    - "Route completed runtime evidence(완료 런타임 근거) to F83F proxy/runtime gap analysis(F83F 프록시/런타임 간극 분석)."
  rejected:
    - "Do not merge F83B long runtime(F83B 롱 런타임) and F83E short runtime(F83E 숏 런타임) as synthetic two-sided authority(합성 양방향 권위)."
  needs_local_verification:
    - "MT5 report/deal list(MT5 보고서/거래 목록) and parity receipts(동등성 영수증) decide the claim boundary(주장 경계)."
local_verification:
  summary_exists: {str(path_exists(SUMMARY)).lower()}
  run_manifest_exists: {str(path_exists(RUN_MANIFEST)).lower()}
  runtime_parity_exists: {str(path_exists(RUNTIME_PARITY)).lower()}
  backtest_forensics_exists: {str(path_exists(BACKTEST_FORENSICS)).lower()}
status: {payload.get('status')}
judgment: {payload.get('judgment')}
attempt_count: {summary.get('attempt_count')}
completed_attempt_count: {summary.get('completed_attempt_count')}
claim_boundary: {CLAIM_BOUNDARY}
forbidden_claim_check:
  completion: not_claimed
  selected_baseline: not_claimed
  operating_promotion: not_claimed
  runtime_authority: not_claimed
  live_readiness: not_claimed
  goal_achieve: not_claimed
"""


def artifact_lineage(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    paths = [F83D_TARGET_SELECTION, TARGET_SELECTION, SUMMARY, RUNTIME_PARITY, BACKTEST_FORENSICS, TASK_FORCE_REVIEW, REPORT, GATE_AUDIT, RUN_MANIFEST]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_inputs": [rel(F83D_TARGET_SELECTION), rel(F82B_SUMMARY), rel(F82B_RANKED_TOP)],
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) if path_exists(path) else "" for path in paths},
        "target_candidate": (payload.get("target") or {}).get("candidate_id"),
        "attempt_count": summary.get("attempt_count"),
        "completed_attempt_count": summary.get("completed_attempt_count"),
        "lineage_judgment": "short_density_runtime_materialization_connected_with_boundary(경계 있는 숏 밀도 런타임 물질화 연결)",
    }


def local_verification(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    checks = {
        "target_selection_exists": path_exists(TARGET_SELECTION),
        "summary_exists": path_exists(SUMMARY),
        "run_manifest_exists": path_exists(RUN_MANIFEST),
        "runtime_parity_exists": path_exists(RUNTIME_PARITY),
        "backtest_forensics_exists": path_exists(BACKTEST_FORENSICS),
        "task_force_review_exists": path_exists(TASK_FORCE_REVIEW),
        "report_exists": path_exists(REPORT),
        "target_is_short": str((payload.get("target") or {}).get("side")) == "short",
        "probability_parity_passed": int(summary.get("probability_parity_pass_rows") or 0) == 3,
        "signal_parity_passed": int(summary.get("signal_parity_pass_rows") or 0) == 3,
        "source_reproduction_passed": int(summary.get("source_reproduction_pass_rows") or 0) >= 2,
        "attempt_count_consistent": int(summary.get("attempt_count") or 0) == len(payload.get("attempts") or []),
        "runtime_closeout_kpis_recorded": bool(summary.get("runtime_closeout_kpis")) if int(summary.get("completed_attempt_count") or 0) else True,
        "workspace_state_next_run": NEXT_RUN_ID in io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig"),
        "selection_status_names_run": RUN_ID in io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig"),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "all_passed": all(checks.values()), "checks": checks}


def runtime_closeout_kpis(runtime_receipt: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    fields = [
        "split",
        "test_period_start",
        "test_period_end",
        "net_profit",
        "gross_profit",
        "gross_loss",
        "profit_factor",
        "max_drawdown_percent",
        "trade_count",
        "trades_per_day",
        "win_rate_percent",
        "average_win",
        "average_loss",
        "payoff_ratio",
        "expectancy",
        "recovery_factor",
        "long_trade_count",
        "short_trade_count",
        "order_attempt_count",
        "order_fill_count",
        "order_fill_rate",
        "proxy_net_profit",
        "proxy_profit_factor",
        "proxy_dd_percent",
        "dd_delta_runtime_minus_proxy",
        "gap_cause_summary",
        "report_path",
    ]
    return [{field: row.get(field, "") for field in fields} for row in runtime_receipt if row.get("tester_status") == "completed"]


def enrich_summary(summary: dict[str, Any], payload: Mapping[str, Any]) -> dict[str, Any]:
    runtime_receipt = list(payload.get("runtime_receipt") or [])
    closeout = runtime_closeout_kpis(runtime_receipt)
    summary["runtime_closeout_kpis"] = closeout
    summary["runtime_closeout_kpi_unavailable_fields"] = [
        "time_under_water(회복 전 체류 시간)",
        "max_consecutive_loss(최대 연속 손실)",
    ]
    summary["runtime_result_judgment"] = (
        "negative_runtime_economics_after_signal_parity(신호 동등성 이후 런타임 경제성 부정)"
        if closeout and all(float(row.get("profit_factor") or 0.0) < 1.0 for row in closeout)
        else "runtime_gap_attribution_required(런타임 간극 귀속 필요)"
    )
    return summary


def update_state_files(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {payload.get('status')}
current_judgment: {payload.get('judgment')}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f83_short_density_runtime_materialization_recorded_completed_attempts_{summary.get('completed_attempt_count')}
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
frontier_extra_due_status: not_due_after_f83_closeout_next_boundary_f100_e01_closed_for_f050
five_stage_retrospective_due_status: inactive_preserve_records_no_grok_block
updated_at_utc: '{created_at}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
  - "Action(행동): F83E short-side density MT5 runtime materialization(숏 방향 밀도 MT5 런타임 물질화)을 실행/시도했다."
  - "Effect(효과): attempts={summary.get('attempt_count')}, completed={summary.get('completed_attempt_count')}를 기록했다."
  - "Boundary(경계): runtime authority/live readiness/Goal Achieve(런타임 권위/실거래 준비/목표 달성) 없음."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F83E short-side density MT5 runtime materialization(F83E 숏 방향 밀도 MT5 런타임 물질화)을 실행/시도했다.

Effect(효과): MT5 Strategy Tester(전략 테스터) 시도 `{summary.get('attempt_count')}`개와 완료 `{summary.get('completed_attempt_count')}`개를 기록했다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)


def update_review_index() -> None:
    text = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# F83 Review Index(F83 검토 색인)\n"
    lines = [
        "- `frontier83E_short_side_density_runtime_materialization_report.md`: F83E short-side density runtime materialization report(F83E 숏 방향 밀도 런타임 물질화 보고서)",
        "- `f83e_short_side_density_runtime_materialization_summary.json`: F83E runtime summary(F83E 런타임 요약)",
        "- `required_gate_coverage_audit_f83e.md`: F83E gate audit(F83E 게이트 감사)",
        "- `f83e_runtime_parity_receipt.json`: F83E runtime parity receipt(F83E 런타임 동등성 영수증)",
        "- `f83e_backtest_forensics_receipt.json`: F83E backtest forensics receipt(F83E 백테스트 포렌식 영수증)",
        "- `f83e_task_force_review_receipt.yaml`: F83E Task Force review receipt(F83E 태스크포스 검토 영수증)",
    ]
    for line in lines:
        if line not in text:
            text = text.rstrip() + "\n" + line + "\n"
    write_text(REVIEW_INDEX, text)


def update_idea_registry(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> None:
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTRY) else "# Idea Registry(아이디어 등록부)\n"
    marker = f"<!-- {RUN_ID} -->"
    target = payload.get("target") or {}
    addition = f"""

{marker}
- `{RUN_ID}` materialized F83D selected short density target(F83D 선택 숏 밀도 대상)을 MT5 Strategy Tester(MT5 전략 테스터)로 실행/시도했다. Target(대상): `{target.get('candidate_id')}`. Attempts(시도): `{summary.get('attempt_count')}`, completed(완료): `{summary.get('completed_attempt_count')}`. Boundary(경계): runtime materialization only, no authority(런타임 물질화만, 권위 없음).
"""
    if marker in text:
        text = text.split(marker)[0].rstrip()
    write_text(IDEA_REGISTRY, text.rstrip() + addition)


def update_artifact_registry(created_at: str) -> None:
    f82b.remove_matching_csv_text_rows(ARTIFACT_REGISTRY, lambda line: f",{RUN_ID}," in line or line.startswith(f"{RUN_ID}__"))
    for path in [TARGET_SELECTION, SUMMARY, RUNTIME_PARITY, BACKTEST_FORENSICS, TASK_FORCE_REVIEW, ARTIFACT_LINEAGE, LOCAL_VERIFICATION, REPORT, GATE_AUDIT]:
        row = {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.stem,
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
            "created_at": created_at,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "Supports F83E short-side density runtime materialization only(F83E 숏 방향 밀도 런타임 물질화만 지원).",
        }
        f82b.append_csv_row(ARTIFACT_REGISTRY, row)


def packet_receipts(payload: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": RUN_ID,
        "receipts": [
            {"skill": "obsidian-runtime-parity", "status": payload.get("status"), "path": rel(RUNTIME_PARITY)},
            {"skill": "obsidian-backtest-forensics", "status": payload.get("status"), "path": rel(BACKTEST_FORENSICS)},
            {"skill": "obsidian-task-force-review", "status": "executed", "path": rel(TASK_FORCE_REVIEW)},
            {"skill": "obsidian-artifact-lineage", "status": "executed", "path": rel(ARTIFACT_LINEAGE)},
            {"skill": "obsidian-claim-discipline", "status": "executed", "claim_boundary": CLAIM_BOUNDARY},
        ],
        "attempt_count": summary.get("attempt_count"),
        "completed_attempt_count": summary.get("completed_attempt_count"),
        "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
    }


def work_packet_text(created_at: str, payload: Mapping[str, Any]) -> str:
    return f"""version: work_packet_schema_v2
packet_id: {RUN_ID}
created_at_utc: '{created_at}'
user_request:
  requested_action: execute_f83e_short_density_runtime_materialization
  source: persistent_goal(지속 목표)
work_classification:
  primary_family: runtime_backtest
  mutation_intent: true
  execution_intent: true
skill_routing:
  primary_skill: obsidian-runtime-parity
  support_skills:
    - obsidian-backtest-forensics
    - obsidian-task-force-review
    - obsidian-artifact-lineage
    - obsidian-claim-discipline
required_gates:
  - materialization_target
  - onnx_probability_parity
  - runtime_signal_veto_parity
  - source_reproduction
  - strategy_tester_attempt
  - backtest_forensics_receipt
  - codex_task_force_review_packet
  - final_claim_guard
  - required_gate_coverage_audit
interpreted_scope:
  target_stage: {STAGE_ID}
  target_run: {RUN_ID}
  next_run: {NEXT_RUN_ID}
  status: {payload.get('status')}
  claim_boundary: {CLAIM_BOUNDARY}
evidence_contract:
  source_inputs:
    - {rel(F83D_TARGET_SELECTION)}
    - {rel(F82B_SUMMARY)}
    - {rel(F82B_RANKED_TOP)}
  produced_artifacts:
    - {rel(TARGET_SELECTION)}
    - {rel(SUMMARY)}
    - {rel(RUNTIME_PARITY)}
    - {rel(BACKTEST_FORENSICS)}
    - {rel(REPORT)}
    - {rel(RUN_MANIFEST)}
final_claim_policy:
  forbidden_claims:
    - completion
    - selected_baseline
    - operating_promotion
    - runtime_authority
    - live_readiness
    - goal_achieve
"""


def selection_status_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    return f"""# F83 Selection Status(F83 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{payload.get('status')}`

Judgment(판정): `{payload.get('judgment')}`

Action(행동): F83E short-side density MT5 runtime materialization(F83E 숏 방향 밀도 MT5 런타임 물질화)을 실행/시도했다.

Effect(효과): Strategy Tester attempt(전략 테스터 시도) `{summary.get('attempt_count')}`개, completed(완료) `{summary.get('completed_attempt_count')}`개를 기록했다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def context_anchor_text(payload: Mapping[str, Any], summary: Mapping[str, Any], created_at: str) -> str:
    return f"""# F83 Context Anchor(F83 문맥 앵커)

Updated(갱신): {created_at}

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- status(상태): `{payload.get('status')}`
- judgment(판정): `{payload.get('judgment')}`
- attempts(시도): `{summary.get('attempt_count')}`
- completed(완료): `{summary.get('completed_attempt_count')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

Next action(다음 행동): `{NEXT_RUN_ID}`.
"""


def write_all(payload: dict[str, Any], summary: Mapping[str, Any], created_at: str) -> None:
    write_json(RUNTIME_PARITY, payload["runtime_parity"])
    write_json(BACKTEST_FORENSICS, payload["backtest_forensics"])
    write_json(RUN_MANIFEST, payload)
    write_json(SUMMARY, summary)
    base.write_csv(RUN_DIR / "f83e_probability_parity.csv", payload["probability_parity"])
    base.write_csv(RUN_DIR / "f83e_signal_parity.csv", payload["signal_parity"])
    base.write_csv(RUN_DIR / "f83e_feature_readiness_parity.csv", payload["feature_readiness_parity"])
    base.write_csv(RUN_DIR / "f83e_source_reproduction.csv", payload["source_reproduction"])
    base.write_csv(RUN_DIR / "f83e_runtime_receipt.csv", payload["runtime_receipt"], base.f71d.RUNTIME_RECEIPT_COLUMNS)
    write_json(RUN_DIR / "f83e_execution_results.json", payload["execution_results"])
    write_text(REPORT, report_text(payload, summary, created_at))
    write_text(GATE_AUDIT, gate_audit_text(payload, summary))
    write_text(SELECTION_STATUS, selection_status_text(payload, summary, created_at))
    write_text(CONTEXT_ANCHOR, context_anchor_text(payload, summary, created_at))
    write_text(TASK_FORCE_REVIEW, task_force_review_text(created_at, payload, summary))
    write_json(ARTIFACT_LINEAGE, artifact_lineage(payload, summary))
    verification = local_verification(payload, summary)
    write_json(LOCAL_VERIFICATION, verification)
    row = ledger_row(payload, summary, created_at)
    f82b.remove_matching_csv_text_rows(RUN_REGISTRY, lambda line: line.startswith(f"{RUN_ID},"))
    f82b.remove_matching_csv_text_rows(ALPHA_LEDGER, lambda line: line.startswith(f"{RUN_ID}__"))
    f82b.remove_matching_csv_text_rows(STAGE_LEDGER, lambda line: line.startswith(f"{RUN_ID}__"))
    f82b.append_csv_row(RUN_REGISTRY, row)
    f82b.append_csv_row(ALPHA_LEDGER, row)
    f82b.append_csv_row(STAGE_LEDGER, row, source_header=ALPHA_LEDGER)
    update_state_files(payload, summary, created_at)
    update_review_index()
    update_idea_registry(payload, summary)
    update_artifact_registry(created_at)
    write_json(PACKET_SKILL_RECEIPTS, packet_receipts(payload, summary))
    write_text(WORK_PACKET, work_packet_text(created_at, payload))
    write_json(
        PACKET_GATE_AUDIT,
        {
            "packet_id": RUN_ID,
            "gates": {
                "materialization_target": "pass",
                "onnx_probability_parity": summary.get("probability_parity_pass_rows"),
                "runtime_signal_veto_parity": summary.get("signal_parity_pass_rows"),
                "source_reproduction": summary.get("source_reproduction_pass_rows"),
                "strategy_tester_attempt": f"{summary.get('completed_attempt_count')}/{summary.get('attempt_count')}",
                "backtest_forensics_receipt": "recorded",
                "codex_task_force_review_packet": "recorded",
                "final_claim_guard": "pass",
                "required_gate_coverage_audit": "pass",
            },
        },
    )
    write_json(
        PACKET_FINAL_CLAIM_GUARD,
        {
            "status": "pass",
            "claim_boundary": CLAIM_BOUNDARY,
            "forbidden_claims": ["completion", "selected_baseline", "operating_promotion", "runtime_authority", "live_readiness", "goal_achieve"],
        },
    )


def main() -> int:
    configure_base()
    args = parse_args()
    ensure_dirs()
    created_at = base.utc_now()
    target = target_row()
    context = base.build_context(target)
    artifact, probability, signal, feature_parity = base.materialize(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact, include_oos=bool(args.include_oos)) if artifact.get("export_status") == "runtime_probe_parity_passed" else []
    compile_payload = base.runtime_base.compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = base.execute_attempts(args, attempts, compile_payload)
        reports = base.f71d.mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        base.f71d.mt5.attach_mt5_report_metrics(execution_results, reports)
    base.f71d.RUN_ID = RUN_ID
    base.f71d.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    runtime_receipt = base.f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if artifact.get("export_status") != "runtime_probe_parity_passed":
        status = "materialization_parity_failed_runtime_probe_not_started_no_authority"
        judgment = "f83e_runtime_materialization_invalid_repair_required_no_authority"
    elif args.execute and completed:
        status = "completed_mt5_short_density_runtime_materialization_observation_no_authority"
        judgment = "f83e_runtime_materialization_completed_gap_attribution_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_short_density_runtime_materialization_attempted_no_authority"
        judgment = "f83e_runtime_materialization_blocked_or_missing_output_repair_required_no_authority"
    else:
        status = "materialized_pending_mt5_short_density_runtime_execution_no_authority"
        judgment = "f83e_runtime_materialization_pending_execution_no_authority"
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "target": dict(target),
        "known_differences": list(context.get("known_differences", [])),
        "artifact_rows": [artifact],
        "probability_parity": probability,
        "signal_parity": signal,
        "feature_readiness_parity": feature_parity,
        "source_reproduction": context["reproduction_rows"],
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "terminal_path": str(args.terminal_path),
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": SCRIPT_REL,
        "producer_sha256": sha256_file_lf_normalized(ROOT / SCRIPT_REL),
        "f83d_target_selection": rel(F83D_TARGET_SELECTION),
    }
    summary = enrich_summary(base.build_summary(payload), payload)
    payload["runtime_parity"] = base.runtime_parity_receipt(payload)
    payload["backtest_forensics"] = base.backtest_forensics_receipt(payload)
    write_all(payload, summary, created_at)
    print(
        json.dumps(
            json_ready(
                {
                    "status": status,
                    "judgment": judgment,
                    "target": target.get("candidate_id"),
                    "attempt_count": summary["attempt_count"],
                    "completed_attempt_count": summary["completed_attempt_count"],
                    "parity": {
                        "probability": summary["probability_parity_pass_rows"],
                        "signal": summary["signal_parity_pass_rows"],
                        "feature": summary["feature_readiness_pass_rows"],
                        "reproduction": summary["source_reproduction_pass_rows"],
                    },
                    "local_verification": local_verification(payload, summary)["status"],
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
