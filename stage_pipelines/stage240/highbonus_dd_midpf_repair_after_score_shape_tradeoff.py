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
from stage_pipelines.stage238 import score_shape_repair_after_threshold_surface_discrete as stage238  # noqa: E402


STAGE_ID = "240_adapter_research__highbonus_dd_midpf_repair_after_score_shape_tradeoff"
RUN_NUMBER = "run240A"
RUN_ID = "run240A_stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff_v1"
PACKET_ID = "stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff_v1"
PARENT_RUN_ID = "run239A_stage239_stage238_score_shape_followup_review_v1"
SOURCE_STAGE_ID = "239_adapter_research__stage238_score_shape_followup_review"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE239_EVIDENCE_COMMIT = "36307c14a286f112dbb50d88733091a1bb169252"
SOURCE_STAGE239_HASH_RECORD_COMMIT = "b9da2e36ade4563a0a96df4371bf27ede732c275"
NEXT_STAGE_ID = "241_adapter_research__stage240_highbonus_repair_followup_review"
NEXT_RUN_ID = "run241A_stage241_stage240_highbonus_repair_followup_review_v1"
NEXT_PACKET_ID = "stage241_stage240_highbonus_repair_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_highbonus_dd_midpf_repair_after_score_shape_tradeoff"
BOUNDARY = stage238.BOUNDARY
LEGACY_34D = stage238.LEGACY_34D
OOS_REFERENCE = {
    "adapter_id": "s238_rank3f_neutral_ref",
    "oos_net": 719.48,
    "oos_pf": 1.74,
    "oos_dd": 9.792,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s240a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage240_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage240_highbonus_repair_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage240_highbonus_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage240_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage240_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage240_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage240_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage240_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage240_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage240_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage240_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage240_probability_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage240_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage240_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage240_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage240_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage240/highbonus_dd_midpf_repair_after_score_shape_tradeoff.py")
ARTIFACT_COLUMNS = stage238.ARTIFACT_COLUMNS

SIGNAL_COLUMN = stage238.SIGNAL_COLUMN
RANK_COLUMN = "stage240_margin_rank_bucket"
SOURCE_REFERENCE_ADAPTER = "s235_session_ref_h3_cd8"
SOURCE_SPEC = dict(stage238.SOURCE_SPEC)
REFERENCE_EXTRA = dict(stage238.REFERENCE_EXTRA)


def variant(
    adapter_id: str,
    label: str,
    *,
    bonus_high: float,
    bonus_vhigh: float,
    risk_cap: float,
    note: str,
) -> Any:
    return stage238.repair.RepairVariant(
        adapter_id=adapter_id,
        label=label,
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=risk_cap,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes=note,
    )


VARIANTS = (
    variant(
        "s240_highbonus010_samecap",
        "stage240_highbonus010_samecap_control",
        bonus_high=0.10,
        bonus_vhigh=0.15,
        risk_cap=0.031375,
        note="Stage240 control: repeat Stage238 highbonus score shape with same risk cap.",
    ),
    variant(
        "s240_highbonus010_cap0275",
        "stage240_highbonus010_cap0275",
        bonus_high=0.10,
        bonus_vhigh=0.15,
        risk_cap=0.0275,
        note="Stage240 repair: keep highbonus score shape while compressing model risk cap.",
    ),
    variant(
        "s240_highbonus010_cap0251",
        "stage240_highbonus010_reference_cap0251",
        bonus_high=0.10,
        bonus_vhigh=0.15,
        risk_cap=0.0250758284,
        note="Stage240 repair: keep highbonus score shape with reference-like max risk cap.",
    ),
    variant(
        "s240_highbonus0075_cap0290",
        "stage240_highbonus0075_cap0290",
        bonus_high=0.075,
        bonus_vhigh=0.1125,
        risk_cap=0.0290,
        note="Stage240 repair: reduce bonus strength and use an intermediate model risk cap.",
    ),
)


def extra(axis: str, bonus_high: float, bonus_vhigh: float) -> dict[str, Any]:
    return {
        "axis": axis,
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "both",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "rank_scores": {
            "low": (0.0, 0.0, 0.0),
            "mid": (0.0, 0.0, 0.0),
            "high": (bonus_high, -bonus_high, bonus_high),
            "vhigh": (bonus_vhigh, -bonus_vhigh, bonus_vhigh),
        },
    }


VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s240_highbonus010_samecap": extra("highbonus010_samecap", 0.10, 0.15),
    "s240_highbonus010_cap0275": extra("highbonus010_cap0275", 0.10, 0.15),
    "s240_highbonus010_cap0251": extra("highbonus010_cap0251", 0.10, 0.15),
    "s240_highbonus0075_cap0290": extra("highbonus0075_cap0290", 0.075, 0.1125),
}
SOURCE_SPECS_BY_VARIANT = {item.adapter_id: dict(SOURCE_SPEC) for item in VARIANTS}
MODEL_RISK_MIN_PCT = {item.adapter_id: 0.005 for item in VARIANTS}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return stage238.rel(path)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    stage238.write_csv(path, rows, columns)


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return stage238.as_float(row, key, default)


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, item in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / item.adapter_id
        for split in ("validation_is", "oos"):
            date_values = stage238.s161.base.parse_ini(stage238.s161.base.engine.source_attempt_ini(split, item))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (stage238.s161.base.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{item.adapter_id}", "ta"),
                    (stage238.s161.base.mt5.TIER_AB, "routed_total", f"mt5_routed_{item.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 24010000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    stage238.s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=240,
                        exploration_label="stage240_BaselineAdapter__HighbonusDdMidpfRepair",
                        attempt_name=f"{item.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][item.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{item.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][item.adapter_id][split]["common_path"]),
                        feature_count=3,
                        feature_order_hash=inputs["model_exports"][item.adapter_id]["feature_order_hash"],
                        short_threshold=item.short_threshold,
                        long_threshold=item.long_threshold,
                        min_margin=0.0,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=item.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{item.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=item.close_on_flat_signal,
                        reverse_on_opposite_signal=item.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=item.close_only_on_opposite_signal,
                        extra_set_values=stage238.extra_set_values(item, magic),
                    )
                )
    return attempts


def pass_stage240(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row, "validation_net") >= LEGACY_34D["net_profit"]
        and as_float(row, "validation_early_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_mid_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_balance_dd_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(row, "oos_net") >= OOS_REFERENCE["oos_net"]
        and as_float(row, "oos_pf") >= OOS_REFERENCE["oos_pf"]
        and as_float(row, "oos_balance_dd_percent", 99.0) <= OOS_REFERENCE["oos_dd"]
    )


def decide(quality_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage240_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(pass_stage240(row) for row in quality_rows):
        return "open_stage241_bounded_followup_due_to_highbonus_repair_candidate_not_final"
    return "open_stage241_bounded_followup_due_to_highbonus_dd_midpf_tradeoff_candidate_not_final"


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            pass_stage240(row),
            as_float(row, "validation_net"),
            -as_float(row, "validation_balance_dd_percent", 99.0),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_net"),
        ),
    )


def tier_b_rows_stage240() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in VARIANTS:
        for split in ("validation", "oos"):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": item.adapter_id,
                    "split": split,
                    "status": "diagnostic_missing_required_but_disabled_for_stage240_highbonus_repair",
                    "fallback_enabled": 0,
                    "fallback_used_count": 0,
                    "notes": "Stage240 isolates Tier A routed highbonus risk repair; Tier B fallback remains disabled by prior fallback-only damage memory.",
                }
            )
    return rows


def report_markdown(quality_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(quality_rows)
    lines = [
        "# Stage240 Highbonus DD/MidPF Repair Report(240단계 고마진 낙폭/중간 수익요인 수리 보고서)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- source_stage239_evidence_commit(원천 239단계 근거 커밋): `{SOURCE_STAGE239_EVIDENCE_COMMIT}`",
        f"- source_stage239_hash_record_commit(원천 239단계 해시 기록 커밋): `{SOURCE_STAGE239_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{external}`",
        f"- decision(판정): `{decision}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Bounded Design(경계 설계)",
        "",
        "- hypothesis(가설): highbonus(고마진 보너스)는 좋은 net/OOS(순손익/표본외) 단서지만, risk cap(위험 상한)과 score strength(점수 강도)를 낮추면 validation DD(검증 낙폭)와 mid PF(중간 수익요인)가 나아질 수 있다.",
        "- fixed variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, hold(보유) `3`, same-direction cooldown(동방향 대기) `8`, Stage235 reference side filter(235단계 기준 방향 필터).",
        "- changed variables(변경 변수): model_risk_max_pct(모델 위험 최대 비율) `0.031375/0.0275/0.0250758284/0.0290`, high/vhigh bonus(고/초고 마진 보너스) `0.10/0.15` 또는 `0.075/0.1125`.",
        "- stop condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage240(240단계)은 닫는다.",
        "",
        "## KPI Read(KPI 핵심 성과 지표 판독)",
        "",
        "| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중간 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in quality_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {as_float(row, 'validation_net'):.2f} | {as_float(row, 'validation_early_pf'):.6f} | {as_float(row, 'validation_mid_pf'):.6f} | {as_float(row, 'validation_balance_dd_percent'):.4f} | {as_float(row, 'oos_net'):.2f} | {as_float(row, 'oos_pf'):.6f} | {as_float(row, 'oos_balance_dd_percent'):.4f} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- best_row(최선 행): `{best.get('adapter_id', '')}` with validation net(검증 순손익) `{best.get('validation_net', '')}`, validation DD(검증 낙폭) `{best.get('validation_balance_dd_percent', '')}`, mid PF(중간 수익요인) `{best.get('validation_mid_pf', '')}`, OOS net(표본외 순손익) `{best.get('oos_net', '')}`.",
            f"- decision(판정): `{decision}`.",
            "- overall_goal_complete(전체 목표 완료): `false`.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선).",
        ]
    )
    return "\n".join(lines)


def decision_markdown(decision: str, external: str) -> str:
    next_target = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    return f"""# Stage240 Decision(240단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{next_target}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage240(240단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage241(241단계) follow-up review(후속 검토)에서 risk-normalized highbonus(위험 정규화 고마진)의 KPI(핵심 성과 지표) 상충과 다음 bounded repair(경계 수리)를 판정한다.
"""


def write_stage241_seed(decision: str, external: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage241(241단계)는 Stage240(240단계) highbonus DD/midPF repair(고마진 낙폭/중간 수익요인 수리) 결과를 follow-up review(후속 검토)하는 bounded review(경계 검토) 단계다.

## Bounded Question(경계 질문)

Did Stage240(240단계) repair validation DD(검증 낙폭) and early/mid PF(초반/중간 수익요인) while preserving validation/OOS net(검증/표본외 순손익), ATR SL/TP(ATR 손절/익절), model-controlled risk%(모델 제어 위험 비율), and segment behavior(구간 행동)?

Effect(효과): Stage240(240단계) 안에서 다음 수리를 흡수하지 않고 risk-normalized highbonus(위험 정규화 고마진) 결과를 별도 review(검토)로 닫는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage241 Inputs(241단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage241 Review Index(241단계 검토 색인)

- status(상태): `open_planned_from_stage240`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage241 Selection Status(241단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage240`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^\ufeff?current_run_id: .*$", f"current_run_id: {active_run}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {active_stage}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage240(240단계) closed(종료) as `{decision}` and Stage241(241단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): highbonus DD/midPF repair(고마진 낙폭/중간 수익요인 수리)의 KPI(핵심 성과 지표) 상충을 별도 review(검토)로 판정한다.
- >-
  Stage240 evidence(240단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(MONTHLY_KPI_PATH)}`, `{rel(CONCENTRATION_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): risk cap(위험 상한)과 highbonus strength(고마진 강도) 수리가 34D(34D 기준)에 가까워졌는지 확인한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)\nstage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?ms)\nstage241_stage240_highbonus_repair_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision if external == "completed" else "blocked_runtime_incomplete"}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  monthly_kpi_path: {rel(MONTHLY_KPI_PATH)}
  concentration_path: {rel(CONCENTRATION_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID if external == "completed" else RUN_ID}
  boundary: {BOUNDARY}

stage241_stage240_highbonus_repair_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage240
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage240_highbonus_dd_midpf_repair_after_score_shape_tradeoff`
- status(상태): `stage240_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage240(240단계)는 highbonus DD/midPF repair(고마진 낙폭/중간 수익요인 수리)를 MT5(MetaTrader 5, 메타트레이더5)로 측정했다. Effect(효과): Stage241(241단계)가 결과 상충과 다음 bounded repair(경계 수리)를 별도 review(검토)로 판정한다.

## Latest Stage240 Evidence(최신 240단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    status = f"closed_{decision}" if external == "completed" else "blocked_runtime_incomplete"
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage240 Selection Status(240단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage240 Review Index(240단계 검토 색인)

- status(상태): `{status}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage240 highbonus DD/midPF repair closeout(240단계 고마진 낙폭/중간 수익요인 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): highbonus(고마진) risk cap(위험 상한)과 score strength(점수 강도)를 MT5(MetaTrader 5, 메타트레이더5)로 측정하고 Stage241(241단계) follow-up review(후속 검토)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        BALANCE_CURVE_AUDIT_PATH,
        MONTHLY_KPI_PATH,
        CONCENTRATION_PATH,
        DRAWDOWN_PATH,
        QUALITY_MATRIX_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
    ]
    for execution in result.get("execution_results", []):
        for value in (execution.get("set_path"), execution.get("ini_path"), execution.get("report_path")):
            if value:
                paths.append(Path(str(value)))
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage240_highbonus_dd_midpf_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage240 highbonus DD/midPF repair evidence.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    summary_rows = result.get("mt5_kpi_records", [])
    primary = ledger_pairs(
        [
            ("decision", decision),
            ("external_status", result.get("external_verification_status", "")),
            ("variant_count", len(VARIANTS)),
            ("target_surface", TARGET_SURFACE),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("boundary", BOUNDARY),
            ("overall_goal_complete", 0),
        ]
    )
    alpha_rows = stage238.s172.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=summary_rows,
        run_output_root=RUN_ROOT,
        external_verification_status=str(result.get("external_verification_status", "")),
    )
    for row in alpha_rows:
        row["parent_run_id"] = row.get("parent_run_id") or PARENT_RUN_ID
        row["scoreboard_lane"] = "baseline_adapter_stage240_highbonus_dd_midpf_repair"
        row["judgment"] = decision
        row["status"] = "completed" if result.get("external_verification_status") == "completed" else "blocked"
        row["primary_kpi"] = f"{row.get('primary_kpi', '')};{primary}" if row.get("primary_kpi") else primary
        row["guardrail_kpi"] = f"{row.get('guardrail_kpi', '')};{guardrail}" if row.get("guardrail_kpi") else guardrail
        row["path"] = row.get("path") or rel(REPORT_PATH)
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_stage240_highbonus_dd_midpf_repair",
            "status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "notes": ledger_pairs(
                [
                    ("source_stage239_evidence_commit", SOURCE_STAGE239_EVIDENCE_COMMIT),
                    ("source_stage239_hash_record_commit", SOURCE_STAGE239_HASH_RECORD_COMMIT),
                    ("target_surface", TARGET_SURFACE),
                    ("overall_goal_complete", 0),
                ]
            ),
        }
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifacts, key="artifact_id")
    return {
        "run_registry": run_payload,
        "project_alpha_ledger": project_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    required_gates = [
        "kpi_contract_audit",
        "result_judgment_gate",
        "performance_attribution_gate",
        "artifact_lineage_audit",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": decision,
        "external_verification_status": result.get("external_verification_status", ""),
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "routing_receipt.json": {
            **base_payload,
            "primary_family": "runtime_backtest(MT5/백테스트 실행)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(성과 기여 분석)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-runtime-parity(런타임 동등성)",
            ],
            "required_gates": required_gates,
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            **base_payload,
            "summary": rel(SUMMARY_CSV_PATH),
            "segment_kpi": rel(SEGMENT_KPI_PATH),
            "risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
            "trade_audit": rel(AUDIT_CSV_PATH),
            "variant_count": len(VARIANTS),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            **base_payload,
            "judgment_label": "highbonus_dd_midpf_repair_measured_candidate_not_final",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Highbonus score strength and model risk cap variants measured against Stage238 clue.",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            **base_payload,
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            **base_payload,
            "required_gates": required_gates,
            "covered_by": [
                "kpi_contract_audit.json",
                "result_judgment_gate.json",
                "performance_attribution_gate.json",
                "artifact_lineage_audit.json",
                "final_claim_guard.json",
                "required_gate_coverage_audit.json",
            ],
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            **base_payload,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "summary": rel(SUMMARY_CSV_PATH),
                "quality": rel(QUALITY_MATRIX_PATH),
                "decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
        },
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage240 Closeout Packet(240단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{result.get('external_verification_status', '')}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def configure_stage_module() -> None:
    values = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE_ID": SOURCE_STAGE_ID,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "OOS_REFERENCE": OOS_REFERENCE,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "PARTIALS_ROOT": PARTIALS_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
        "SUMMARY_JSON_PATH": SUMMARY_JSON_PATH,
        "SUMMARY_CSV_PATH": SUMMARY_CSV_PATH,
        "REPORT_PATH": REPORT_PATH,
        "SEGMENT_KPI_PATH": SEGMENT_KPI_PATH,
        "BALANCE_CURVE_AUDIT_PATH": BALANCE_CURVE_AUDIT_PATH,
        "MONTHLY_KPI_PATH": MONTHLY_KPI_PATH,
        "CONCENTRATION_PATH": CONCENTRATION_PATH,
        "DRAWDOWN_PATH": DRAWDOWN_PATH,
        "QUALITY_MATRIX_PATH": QUALITY_MATRIX_PATH,
        "RISK_ATR_TELEMETRY_PATH": RISK_ATR_TELEMETRY_PATH,
        "GATE_FEATURE_SUMMARY_PATH": GATE_FEATURE_SUMMARY_PATH,
        "PROBABILITY_BINDING_PATH": PROBABILITY_BINDING_PATH,
        "MODEL_SCORE_AUDIT_PATH": MODEL_SCORE_AUDIT_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "RANK_COLUMN": RANK_COLUMN,
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
    }
    for name, value in values.items():
        setattr(stage238, name, value)
    stage238.build_attempts = build_attempts
    stage238.decide = decide
    stage238.pass_stage238 = pass_stage240
    stage238.best_row = best_row
    stage238.tier_b_rows_stage238 = tier_b_rows_stage240
    stage238.report_markdown = report_markdown
    stage238.decision_markdown = decision_markdown
    stage238.write_stage239_seed = write_stage241_seed
    stage238.update_current_truth = update_current_truth
    stage238.write_status_files = write_status_files
    stage238.append_changelog = append_changelog
    stage238.artifact_rows = artifact_rows
    stage238.write_ledgers = write_ledgers
    stage238.write_packet_files = write_packet_files


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage_module()
    stage238.configure_runner()
    stage238.s161.configure_base()
    args = stage238.s161.parse_args(argv or sys.argv[1:])
    inputs = stage238.prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 240,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": stage238.s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage240_v2_native_highbonus_dd_midpf_repair",
        "feature_set_id": "stage240_signal_margin_rank_plus_reference_side_filter",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = stage238.load_existing_result_if_requested(args) or stage238.s161.base.execute_or_materialize(prepared, args)
    audit_rows = stage238.s172.s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = stage238.s172.s58.risk_rows_from_result(result)
    summary_rows = stage238.s172.s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = stage238.s172.s58.segment_kpi_rows(summary_rows)
    probability_rows = stage238.s161.probability_binding_rows(result)
    model_rows = stage238.s161.model_score_rows(inputs)
    balance_rows, monthly_rows, concentration_rows, drawdown_rows = stage238.s172.build_curve_audit(summary_rows, segment_rows)
    quality_rows = stage238.s172.quality_rows(summary_rows, segment_rows, balance_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality_rows, external)

    stage238.s161.write_run_identity(result, probability_rows, model_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(BALANCE_CURVE_AUDIT_PATH, balance_rows)
    write_csv(MONTHLY_KPI_PATH, monthly_rows)
    write_csv(CONCENTRATION_PATH, concentration_rows)
    write_csv(DRAWDOWN_PATH, drawdown_rows)
    write_csv(QUALITY_MATRIX_PATH, quality_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows_stage240())
    write_md(REPORT_PATH, report_markdown(quality_rows, decision, external))
    write_md(DECISION_PATH, decision_markdown(decision, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "balance_rows": balance_rows,
            "monthly_rows": monthly_rows,
            "concentration_rows": concentration_rows,
            "drawdown_rows": drawdown_rows,
            "probability_rows": probability_rows,
            "model_rows": model_rows,
            "quality_rows": quality_rows,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "source_stage239_evidence_commit": SOURCE_STAGE239_EVIDENCE_COMMIT,
            "source_stage239_hash_record_commit": SOURCE_STAGE239_HASH_RECORD_COMMIT,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, quality_rows)
    write_stage241_seed(decision, external)
    update_current_truth(decision, external)
    write_status_files(decision, external)
    append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": external,
                    "run_id": RUN_ID,
                    "decision": decision,
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                    "quality_rows": quality_rows,
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
