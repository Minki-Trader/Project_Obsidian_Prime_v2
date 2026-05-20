from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "267_adapter_research__baseline_candidate_racing_protocol"
RUN_ID = "run267H_stage267_soft_noncalendar_adapter_design_v1"
RUN_NUMBER = "run267H"
STATUS = "run267H_soft_noncalendar_adapter_design_completed"
NEXT_ACTION = "run267I_materialize_top_soft_noncalendar_adapter_candidates"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "soft_noncalendar_adapter_design"

RUN267G_ROOT = STAGE_ROOT / "02_runs" / "run267G" / "adx_followup_failure_memory"
RUN267F_ROOT = STAGE_ROOT / "02_runs" / "run267F" / "atrcomp_guard_robustness"
FOLLOWUP_DESIGN_PATH = RUN267G_ROOT / "followup_design.csv"
FAILURE_MEMORY_PATH = RUN267G_ROOT / "failure_memory.csv"
STOP_RULES_PATH = RUN267G_ROOT / "stop_rules.csv"
GUARD_COMPARISON_PATH = RUN267F_ROOT / "guard_comparison.csv"
NEGATIVE_SLICE_PATH = RUN267F_ROOT / "negative_slice_summary.csv"

FEATURE_MATRIX_PATH = DESIGN_ROOT / "soft_feature_engineering_matrix.csv"
ADAPTER_SURFACE_PATH = DESIGN_ROOT / "adapter_surface_matrix.csv"
EXPERIMENT_QUEUE_PATH = DESIGN_ROOT / "experiment_queue.csv"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267H_soft_noncalendar_adapter_design.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267H_soft_noncalendar_adapter_design.py")

STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


def fnum(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(dict(row))
    write_csv(path, merged, columns)


def append_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def replace_if_present(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    return text


def by_alias(rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, str]]:
    return {str(row.get("candidate_alias")): dict(row) for row in rows}


def guard_by_alias(rows: Sequence[Mapping[str, str]], guard: str) -> dict[str, dict[str, str]]:
    return {str(row.get("candidate_alias")): dict(row) for row in rows if row.get("guard_variant") == guard}


def candidate_priority(alias: str, adx: Mapping[str, str], di: Mapping[str, str]) -> tuple[int, str]:
    adx_delta = fnum(adx.get("net_delta_vs_run267d_atrcomp"))
    di_dd = fnum(di.get("dd_delta_vs_run267d_atrcomp"))
    if alias == "s264_aih":
        return (1, "core_challenger_first(핵심 도전자 우선)")
    if alias == "s264_lc":
        return (2, "defensive_control_pair(방어 기준 동반)")
    if adx_delta >= 55 and di_dd >= 5:
        return (3, "stress_challenger_high_information(압박 도전자 정보량 높음)")
    if alias == "s264_aia":
        return (4, "oos_anchor_check(표본외 앵커 확인)")
    return (5, "validation_heavy_sanity(검증 중심 정상성 확인)")


def feature_blueprints() -> tuple[dict[str, Any], ...]:
    return (
        {
            "feature_design": "adx_atr_soft_score",
            "feature_family": "trend_strength_atr_compression",
            "new_feature_candidates": "adx_20_25_soft_distance;atr_14_over_atr_50_z;adx_atr_compression_score",
            "formula_sketch": "score = smooth_band(adx_14, 20, 25) * z_low(atr_14_over_atr_50)",
            "adapter_mode": "feature_only_model_retrain",
            "runtime_surface": "existing model CSV can consume after retraining; no EA change if kept as model input",
            "why_from_run267G": "ADX hard guard(강한 방어)는 일부 지지지만 약한 구간을 해결하지 못해 soft score(부드러운 점수)로 바꾼다.",
        },
        {
            "feature_design": "di_adx_atr_continuous_interaction",
            "feature_family": "directional_imbalance_soft_replacement",
            "new_feature_candidates": "abs_di_spread_14_z;di_adx_alignment_score;di_atr_compression_interaction",
            "formula_sketch": "score = z(abs(di_spread_14)) * smooth_band(adx_14, 18, 28) * z_low(atr_14_over_atr_50)",
            "adapter_mode": "feature_only_model_retrain",
            "runtime_surface": "existing model CSV can consume after retraining; exact q33 hard filter is blocked",
            "why_from_run267G": "DI q33 hard replacement(강한 대체)은 실패했으므로 연속 interaction(상호작용)으로만 재검토한다.",
        },
        {
            "feature_design": "soft_exit_overlay_flag",
            "feature_family": "risk_exit_overlay_probe",
            "new_feature_candidates": "weak_context_exit_long_flag;weak_context_exit_short_flag;soft_max_hold_context",
            "formula_sketch": "flag = score_above(weak_context_score, q80); max_hold_context = bucket(score, 0..N)",
            "adapter_mode": "exit_overlay_existing_runtime_possible",
            "runtime_surface": "EA has ExitRiskOverlay(청산 위험 오버레이) feature index inputs; requires materialized feature index mapping",
            "why_from_run267G": "월요일/7월/chron_mid(중간 구간) 약점은 entry prune(진입 절단)보다 lifecycle/risk(수명주기/위험) 쪽으로도 봐야 한다.",
        },
        {
            "feature_design": "model_risk_sizing_confidence_gate",
            "feature_family": "risk_scale_runtime_probe",
            "new_feature_candidates": "confidence_floor_variant;risk_minmax_variant;weak_context_telemetry_slice",
            "formula_sketch": "use existing model-risk sizing parameters while slicing by weak_context_score",
            "adapter_mode": "set_level_runtime_probe_no_model_change",
            "runtime_surface": "EA has model risk sizing(모델 위험 크기 조절) inputs; not a feature replacement and not candidate selection",
            "why_from_run267G": "손실폭과 약한 월을 trade count(거래 수) 절단 없이 줄일 수 있는지 별도 risk probe(위험 탐침)로 본다.",
        },
    )


def build_feature_matrix(
    followups: Sequence[Mapping[str, str]],
    failures: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    adx_rows = guard_by_alias(failures, "adx2025")
    di_rows = guard_by_alias(failures, "dilowq33")
    rows: list[dict[str, Any]] = []
    for followup in followups:
        alias = str(followup.get("candidate_alias"))
        adx = adx_rows.get(alias, {})
        di = di_rows.get(alias, {})
        priority, priority_reason = candidate_priority(alias, adx, di)
        for blueprint in feature_blueprints():
            blocked = "false"
            if blueprint["feature_design"] == "di_adx_atr_continuous_interaction":
                blocked = "exact_dilowq33_blocked_continuous_only"
            rows.append(
                {
                    "design_id": f"{RUN_NUMBER}_{alias}_{blueprint['feature_design']}",
                    "candidate_alias": alias,
                    "candidate_role": followup.get("candidate_role"),
                    "priority_rank": priority,
                    "priority_reason": priority_reason,
                    "feature_design": blueprint["feature_design"],
                    "feature_family": blueprint["feature_family"],
                    "new_feature_candidates": blueprint["new_feature_candidates"],
                    "formula_sketch": blueprint["formula_sketch"],
                    "adapter_mode": blueprint["adapter_mode"],
                    "runtime_surface": blueprint["runtime_surface"],
                    "why_from_run267G": blueprint["why_from_run267G"],
                    "run267f_adx_net_delta_vs_d": adx.get("net_delta_vs_run267d_atrcomp", ""),
                    "run267f_adx_net_delta_vs_e": adx.get("net_delta_vs_run267e_atrmon", ""),
                    "run267f_adx_weakest_weekday_net": adx.get("weakest_weekday_net", ""),
                    "run267f_adx_weakest_month_net": adx.get("weakest_month_net", ""),
                    "run267f_di_net_delta_vs_d": di.get("net_delta_vs_run267d_atrcomp", ""),
                    "run267f_di_dd_delta_vs_d": di.get("dd_delta_vs_run267d_atrcomp", ""),
                    "blocked_exact_repeat": blocked,
                    "materialization_status": "designed_not_materialized",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return sorted(rows, key=lambda row: (int(row["priority_rank"]), str(row["feature_design"])))


def build_adapter_surface(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    surfaces = {
        "feature_only_model_retrain": {
            "adapter_surface": "feature_parser_and_model_training",
            "existing_support": "supported_after_feature_materialization",
            "implementation_scope": "create engineered feature columns; retrain or rematerialize model CSV; preserve feature order hash",
            "verification_need": "feature order audit(피처 순서 감사), model hash(모델 해시), MT5 parity smoke(MT5 동등성 스모크)",
        },
        "exit_overlay_existing_runtime_possible": {
            "adapter_surface": "runtime_set_feature_index_mapping",
            "existing_support": "partially_supported_by_exit_risk_overlay",
            "implementation_scope": "materialize overlay flags and set InpExitRisk* feature indexes; no EA logic change if existing inputs suffice",
            "verification_need": "set/ini hash(설정/초기화 해시), telemetry close reason(원격 측정 청산 사유), time-slice review(시간 구간 검토)",
        },
        "set_level_runtime_probe_no_model_change": {
            "adapter_surface": "runtime_risk_sizing_parameters",
            "existing_support": "supported_as_runtime_probe_only",
            "implementation_scope": "vary model risk sizing settings; compare against fixed lot without calling it model improvement",
            "verification_need": "risk telemetry(위험 원격 측정), min lot floor count(최소 랏 바닥 횟수), DD/trade count attribution(손실폭/거래 수 귀속)",
        },
    }
    rows: list[dict[str, Any]] = []
    for mode in sorted({str(row.get("adapter_mode")) for row in feature_rows}):
        surface = surfaces[mode]
        rows.append(
            {
                "adapter_mode": mode,
                "adapter_surface": surface["adapter_surface"],
                "existing_support": surface["existing_support"],
                "implementation_scope": surface["implementation_scope"],
                "verification_need": surface["verification_need"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_experiment_queue(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    selected_designs = {
        ("s264_aih", "adx_atr_soft_score"): "P0",
        ("s264_lc", "adx_atr_soft_score"): "P0_control",
        ("s264_aih", "di_adx_atr_continuous_interaction"): "P1",
        ("s264_lc", "di_adx_atr_continuous_interaction"): "P1_control",
        ("s258_stc", "model_risk_sizing_confidence_gate"): "P2_stress",
        ("s264_aih", "soft_exit_overlay_flag"): "P2_lifecycle",
    }
    rows: list[dict[str, Any]] = []
    for row in feature_rows:
        key = (str(row.get("candidate_alias")), str(row.get("feature_design")))
        lane = selected_designs.get(key)
        if not lane:
            continue
        rows.append(
            {
                "queue_id": f"{RUN_NUMBER}_{lane}_{row['candidate_alias']}_{row['feature_design']}",
                "priority_lane": lane,
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "feature_design": row.get("feature_design"),
                "adapter_mode": row.get("adapter_mode"),
                "materialization_decision": "materialize_next" if lane.startswith("P0") else "hold_until_p0_review",
                "comparison_baseline": "run267D atrcomp;run267E Monday guard;run267F adx2025;run267G failure memory",
                "success_criteria": "improve or preserve run267D net/PF while reducing run267E gap and not worsening Monday/July/chron_mid weak slices",
                "failure_criteria": "trade count collapse, exact dilowq33 repeat, DD increase without weak-slice repair, or feature order/runtime handoff mismatch",
                "next_action": "run267I materialize P0 candidate/control first",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    priority_order = {"P0": 0, "P0_control": 1, "P1": 2, "P1_control": 3, "P2_stress": 4, "P2_lifecycle": 5}
    return sorted(rows, key=lambda row: priority_order.get(str(row["priority_lane"]), 99))


def report_markdown(
    result: Mapping[str, Any],
    feature_rows: Sequence[Mapping[str, Any]],
    adapter_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> str:
    p0_rows = [row for row in queue_rows if str(row.get("priority_lane")).startswith("P0")]
    lines = [
        "# Stage267 Run267H Soft Non-Calendar Adapter Design(267단계 267H 부드러운 비달력 어댑터 설계)",
        "",
        "- action(행동): run267G(267G 실행)의 failure memory(실패 기억)를 받아 soft feature engineering matrix(부드러운 피처 엔지니어링 행렬), Adapter surface matrix(어댑터 표면 행렬), experiment queue(실험 대기열)를 만들었다.",
        "- effect(효과): hard guard(강한 방어) 반복을 막고, ADX/ATR/DI(추세 강도/ATR/방향성 차이)를 model feature(모델 피처), exit overlay(청산 오버레이), risk sizing probe(위험 크기 조절 탐침)로 나눠 다음 물질화 후보를 좁힌다.",
        f"- feature_rows(피처 행): `{result['feature_rows']}`",
        f"- adapter_surface_rows(어댑터 표면 행): `{result['adapter_surface_rows']}`",
        f"- experiment_queue_rows(실험 대기열 행): `{result['experiment_queue_rows']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "이번 단계는 숫자를 더 좋게 보이게 만드는 실행이 아니다. 어떤 구조를 다음에 실제로 물질화할지 정하는 설계다.",
        "`s264_aih`는 핵심 challenger(도전자)라 P0(우선순위 0)이고, `s264_lc`는 defensive control(방어 기준)로 같이 둔다.",
        "`dilowq33` 같은 hard filter(강한 필터)는 반복하지 않고, DI spread(방향성 차이)는 ADX/ATR(추세 강도/ATR)와 결합된 continuous feature(연속 피처)로만 다시 본다.",
        "",
        "## P0 Queue(P0 대기열)",
        "",
        "| lane(레인) | candidate(후보) | feature design(피처 설계) | adapter mode(어댑터 모드) | decision(결정) |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in p0_rows:
        lines.append(
            f"| `{row['priority_lane']}` | `{row['candidate_alias']}` | `{row['feature_design']}` | `{row['adapter_mode']}` | `{row['materialization_decision']}` |"
        )
    lines.extend(
        [
            "",
            "## Adapter Surfaces(어댑터 표면)",
            "",
            "| adapter mode(어댑터 모드) | support(지원 상태) | implementation(구현 범위) | verification(검증 필요) |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in adapter_rows:
        lines.append(
            f"| `{row['adapter_mode']}` | `{row['existing_support']}` | {row['implementation_scope']} | {row['verification_need']} |"
        )
    lines.extend(
        [
            "",
            "## Experiment Design Receipt(실험 설계 기록)",
            "",
            "- hypothesis(가설): ADX/ATR/DI(추세 강도/ATR/방향성 차이)는 hard prune(강한 절단)이 아니라 soft feature/risk-scale(부드러운 피처/위험 배율) 구조에서만 후보군 안정성을 높일 수 있다.",
            "- decision_use(결정 용도): run267I(267I 실행)에서 P0 candidate/control(후보/기준)을 물질화할지 결정한다.",
            "- comparison_baseline(비교 기준): run267D(267D 실행) atrcomp(ATR 압축), run267E(267E 실행) Monday guard(월요일 방어), run267F(267F 실행) adx2025/dilowq33, run267G(267G 실행) failure memory(실패 기억).",
            "- control_variables(고정 변수): baseline candidate pool(기준 후보군), 2024 historical window(2024 과거 구간), MT5(MetaTrader 5, 메타트레이더5) settings(설정), model identity(모델 정체성) 또는 명시된 model rematerialization(모델 재물질화).",
            "- changed_variables(변경 변수): engineered feature(설계 피처), feature order(피처 순서), optional exit overlay/risk sizing set surface(선택 청산 오버레이/위험 크기 설정 표면).",
            "- sample_scope(표본 범위): FPMarkets US100 M5, 2024 historical stress(2024 과거 압박), Tier A(티어 A)와 routed total(라우팅 전체) 비교.",
            "- success_criteria(성공 기준): net/PF(순수익/수익 팩터), trade count(거래 수), DD(drawdown, 손실폭), Monday/July/chron_mid(월요일/7월/중간 구간)가 함께 덜 깨져야 한다.",
            "- failure_criteria(실패 기준): 특정 feature(피처) 하나에만 붙거나, 거래 수만 줄거나, DI q33 hard repeat(강한 반복)로 돌아가면 실패다.",
            "- invalid_conditions(무효 조건): feature order mismatch(피처 순서 불일치), model hash missing(모델 해시 누락), set/ini path missing(설정/초기화 경로 누락), parser error(파서 오류), MT5 report missing(MT5 보고서 누락).",
            "- stop_conditions(중단 조건): P0 물질화와 MT5 review(MT5 검토) 후에도 약한 구간이 그대로면 ADX/DI branch(분기)를 닫거나 다른 구조 가설로 전환한다.",
            "- evidence_plan(근거 계획): feature matrix(피처 행렬), Adapter surface(어댑터 표면), experiment queue(실험 대기열), materialization manifest(물질화 목록), MT5 reports(MT5 보고서), trade/time-slice/curve review(거래/시간 구간/곡선 검토).",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(FOLLOWUP_DESIGN_PATH)}`, `{rel(FAILURE_MEMORY_PATH)}`, `{rel(STOP_RULES_PATH)}`, `{rel(GUARD_COMPARISON_PATH)}`, `{rel(NEGATIVE_SLICE_PATH)}`",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- consumer(소비자): `{NEXT_ACTION}`",
            f"- artifact_paths(산출물 경로): `{rel(FEATURE_MATRIX_PATH)}`, `{rel(ADAPTER_SURFACE_PATH)}`, `{rel(EXPERIMENT_QUEUE_PATH)}`, `{rel(LINEAGE_PATH)}`, `{rel(RESULT_PATH)}`",
            "- availability(가용성): tracked(추적됨) after commit; reproducible_from_command(명령으로 재생성 가능).",
            "- lineage_judgment(계보 판정): `connected_with_boundary`.",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267H_soft_noncalendar_adapter_design`.",
            "- evidence_available(사용 가능 근거): run267G design/failure memory(설계/실패 기억), run267F MT5 KPI(MT5 핵심 성과 지표), feature/adapter/queue matrices(피처/어댑터/대기열 행렬).",
            "- evidence_missing(빠진 근거): actual materialized features(실제 물질화 피처), model retraining(모델 재학습), MT5 execution(MT5 실행), balance/equity curve(잔액/평가금 곡선).",
            "- judgment_label(판정 라벨): `design_completed_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267H_soft_noncalendar_adapter_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "soft_noncalendar_adapter_design",
            "tier_scope": "Tier A and Tier A+B historical 2024 design",
            "scoreboard": "structural_scout",
            "status": STATUS,
            "judgment": "design_completed_no_candidate_selection",
            "evidence_boundary": "design_matrix_only_no_materialization_no_mt5_execution",
            "report_path": rel(REPORT_PATH),
            "notes": f"feature_rows={result['feature_rows']};queue_rows={result['experiment_queue_rows']};next_action={NEXT_ACTION}.",
        },
        (
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
        ),
    )
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_soft_adapter_design",
            "status": STATUS,
            "judgment": "design_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"Soft non-calendar feature/risk-scale design completed; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__soft_noncalendar_adapter_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "soft_noncalendar_adapter_design",
            "parent_run_id": RUN_ID,
            "record_view": "soft_noncalendar_adapter_design",
            "tier_scope": "Tier A and Tier A+B historical 2024",
            "kpi_scope": "feature_engineering_adapter_design_queue",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": "design_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"feature_rows={result['feature_rows']};adapter_rows={result['adapter_surface_rows']};queue_rows={result['experiment_queue_rows']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;exact_dilowq33_blocked;P0_core_and_control_only",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": f"Next action: {NEXT_ACTION}.",
        },
        (
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
        ),
    )
    entries = (
        ("stage267_run267H_soft_adapter_design_script", "producer_script", PRODUCER_PATH, "Builds run267H soft non-calendar Adapter design."),
        ("stage267_run267H_soft_feature_matrix", "feature_engineering_matrix", FEATURE_MATRIX_PATH, "Run267H soft feature engineering matrix."),
        ("stage267_run267H_adapter_surface_matrix", "adapter_surface_matrix", ADAPTER_SURFACE_PATH, "Run267H Adapter surface matrix."),
        ("stage267_run267H_experiment_queue", "experiment_queue", EXPERIMENT_QUEUE_PATH, "Run267H materialization queue."),
        ("stage267_run267H_lineage", "lineage", LINEAGE_PATH, "Run267H lineage payload."),
        ("stage267_run267H_result", "result", RESULT_PATH, "Run267H result payload."),
        ("stage267_run267H_report", "review_report", REPORT_PATH, "User-facing run267H design report."),
    )
    rows = read_csv(ARTIFACT_REGISTRY_PATH)
    replacement: dict[str, dict[str, Any]] = {}
    for artifact_id, artifact_type, path, notes in entries:
        replacement[artifact_id] = {
            "artifact_id": artifact_id,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": notes,
        }
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(replacement.values())
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_truth_docs() -> None:
    evidence_line = (
        "- Stage267(267단계) run267H soft non-calendar Adapter design(부드러운 비달력 어댑터 설계): "
        f"`{rel(REPORT_PATH)}`"
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_if_present(current, "- current_run(현재 실행): `run267G_stage267_adx_followup_failure_memory_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_if_present(current, "- status(상태): `run267G_adx_followup_failure_memory_completed`", f"- status(상태): `{STATUS}`")
    current = append_after(
        current,
        "- Stage267(267단계) run267G ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267G_adx_followup_failure_memory.md`",
        evidence_line,
    )
    current = replace_if_present(current, "- next_run(다음 실행): `run267H_design_soft_noncalendar_adapter_feature_engineering_matrix`", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_if_present(
        current,
        "- action(행동): run267G(267G 실행)에서 run267F(267F 실행)의 ADX/DI guard(추세 강도/방향성 차이 방어)를 failure memory(실패 기억), follow-up design(후속 설계), stop rules(중단 규칙)로 정리했다.",
        "- action(행동): run267H(267H 실행)에서 soft feature engineering matrix(부드러운 피처 엔지니어링 행렬), Adapter surface matrix(어댑터 표면 행렬), experiment queue(실험 대기열)를 만들었다.",
    )
    current = replace_if_present(
        current,
        "- effect(효과): `adx2025`는 soft context seed(부드러운 문맥 씨앗)로만 남기고, `dilowq33` exact repeat(정확 반복)는 차단해 다음 Adapter(어댑터) 연구가 넓은 feature engineering(피처 엔지니어링)으로 이동하게 한다.",
        "- effect(효과): hard guard(강한 방어)를 반복하지 않고 `s264_aih` 핵심 후보와 `s264_lc` 방어 기준을 P0 materialization(우선 물질화) 후보로 좁힌다.",
    )
    current = replace_if_present(
        current,
        "- next_action(다음 행동): `run267H_design_soft_noncalendar_adapter_feature_engineering_matrix`. Effect(효과): hard guard(강한 방어)가 아니라 soft feature/risk-scale(부드러운 피처/위험 배율) 후보를 설계해 Monday/July/chron_mid(월요일/7월/중간 구간)를 함께 본다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): P0 soft non-calendar Adapter(부드러운 비달력 어댑터) 후보를 실제 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 물질화할지 검증한다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_if_present(selection, "- stage_status(단계 상태): `run267G_adx_followup_failure_memory_completed`", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_if_present(selection, "- current_run(현재 실행): `run267G_stage267_adx_followup_failure_memory_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_if_present(selection, "- last_completed_run(마지막 완료 실행): `run267G_stage267_adx_followup_failure_memory_v1`", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after(
        selection,
        "- run267G_adx_followup_failure_memory(267G ADX 후속과 DI 실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267G_adx_followup_failure_memory.md`",
        f"- run267H_soft_noncalendar_adapter_design(267H 부드러운 비달력 어댑터 설계): `{rel(REPORT_PATH)}`",
    )
    selection = replace_if_present(selection, "- next_action(다음 행동): `run267H_design_soft_noncalendar_adapter_feature_engineering_matrix`", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_if_present(
        selection,
        "Run267G(267G 실행)는 ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억)를 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, `adx2025`는 soft context seed(부드러운 문맥 씨앗), `dilowq33`는 exact repeat block(정확 반복 차단)으로 다음 run267H(267H 실행) 설계에 넘긴다.",
        "Run267H(267H 실행)는 soft non-calendar Adapter design(부드러운 비달력 어댑터 설계)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, P0 물질화 후보는 `s264_aih` core(핵심)와 `s264_lc` control(기준)의 `adx_atr_soft_score`로 좁힌다.",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_if_present(review, "- status(상태): `run267G_adx_followup_failure_memory_completed`", f"- status(상태): `{STATUS}`")
    review = replace_if_present(review, "- current_run(현재 실행): `run267G_stage267_adx_followup_failure_memory_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_if_present(review, "- last_completed_run(마지막 완료 실행): `run267G_stage267_adx_followup_failure_memory_v1`", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after(
        review,
        "- run267G_adx_followup_failure_memory(267G ADX 후속과 DI 실패 기억): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267G_adx_followup_failure_memory.md`",
        f"- run267H_soft_noncalendar_adapter_design(267H 부드러운 비달력 어댑터 설계): `{rel(REPORT_PATH)}`",
    )
    review = replace_if_present(
        review,
        "Run267G(267G 실행)는 ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억)를 완료했다.",
        "Run267H(267H 실행)는 soft non-calendar Adapter design(부드러운 비달력 어댑터 설계)을 완료했다.",
    )
    review = replace_if_present(
        review,
        "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)를 주장하지 않고, `run267H_design_soft_noncalendar_adapter_feature_engineering_matrix`에서 soft non-calendar Adapter(부드러운 비달력 어댑터) feature engineering(피처 엔지니어링) 설계를 진행한다.",
        f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)를 주장하지 않고, `{NEXT_ACTION}`에서 P0 soft non-calendar Adapter(우선순위 0 부드러운 비달력 어댑터) 후보 물질화를 검토한다.",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_if_present(workspace, "current_run_id: run267G_stage267_adx_followup_failure_memory_v1", f"current_run_id: {RUN_ID}")
    workspace = replace_if_present(workspace, "  status: run267G_adx_followup_failure_memory_completed", f"  status: {STATUS}")
    workspace = replace_if_present(workspace, "  current_run_id: run267G_stage267_adx_followup_failure_memory_v1", f"  current_run_id: {RUN_ID}")
    workspace = replace_if_present(workspace, "  last_completed_run_id: run267G_stage267_adx_followup_failure_memory_v1", f"  last_completed_run_id: {RUN_ID}")
    workspace = append_after(
        workspace,
        "  run267G_adx_followup_failure_memory_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267G_adx_followup_failure_memory.md",
        f"  run267H_soft_noncalendar_adapter_design_path: {rel(REPORT_PATH)}",
    )
    workspace = replace_if_present(workspace, "  next_action: run267H_design_soft_noncalendar_adapter_feature_engineering_matrix", f"  next_action: {NEXT_ACTION}")
    workspace = replace_if_present(
        workspace,
        "Stage267(267단계) run267G(267G 실행) ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억) `run267G_adx_followup_failure_memory_completed`. Effect(효과): run267F(267F 실행)의 ADX(추세 강도) 부분 지지와 DI spread(방향성 차이) 악화를 failure memory(실패 기억)와 next design(다음 설계)으로 정리했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        f"Stage267(267단계) run267H(267H 실행) soft non-calendar Adapter design(부드러운 비달력 어댑터 설계) `{STATUS}`. Effect(효과): P0 materialization(우선 물질화) 후보를 `s264_aih`와 `s264_lc`의 `adx_atr_soft_score`로 좁혔지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace = replace_if_present(
        workspace,
        "Next action(다음 행동)는 `run267H_design_soft_noncalendar_adapter_feature_engineering_matrix`이다. Effect(효과): hard guard(강한 방어)를 반복하지 않고 soft feature/risk-scale(부드러운 피처/위험 배율) Adapter(어댑터) 설계로 확장한다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): P0 soft non-calendar Adapter(부드러운 비달력 어댑터) 후보를 실제 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 물질화할지 검증한다.",
    )
    workspace = replace_if_present(
        workspace,
        "active_run267G_adx_followup_failure_memory_completed(267G ADX 후속과 DI 실패 기억 완료 활성)",
        "active_run267H_soft_noncalendar_adapter_design_completed(267H 부드러운 비달력 어댑터 설계 완료 활성)",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def build() -> dict[str, Any]:
    created_at = utc_now()
    followups = read_csv(FOLLOWUP_DESIGN_PATH)
    failures = read_csv(FAILURE_MEMORY_PATH)
    guard_comparison = read_csv(GUARD_COMPARISON_PATH)
    negatives = read_csv(NEGATIVE_SLICE_PATH)
    if not followups or not failures:
        raise RuntimeError("run267G inputs are missing")
    feature_rows = build_feature_matrix(followups, failures)
    adapter_rows = build_adapter_surface(feature_rows)
    queue_rows = build_experiment_queue(feature_rows)
    result = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "source_run_ids": [
            "run267G_stage267_adx_followup_failure_memory_v1",
            "run267F_stage267_atrcomp_guard_robustness_non_calendar_v1",
        ],
        "feature_rows": len(feature_rows),
        "adapter_surface_rows": len(adapter_rows),
        "experiment_queue_rows": len(queue_rows),
        "source_guard_comparison_rows": len(guard_comparison),
        "source_negative_slice_rows": len(negatives),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "feature_matrix": rel(FEATURE_MATRIX_PATH),
            "adapter_surface": rel(ADAPTER_SURFACE_PATH),
            "experiment_queue": rel(EXPERIMENT_QUEUE_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
    }
    write_csv(
        FEATURE_MATRIX_PATH,
        feature_rows,
        (
            "design_id",
            "candidate_alias",
            "candidate_role",
            "priority_rank",
            "priority_reason",
            "feature_design",
            "feature_family",
            "new_feature_candidates",
            "formula_sketch",
            "adapter_mode",
            "runtime_surface",
            "why_from_run267G",
            "run267f_adx_net_delta_vs_d",
            "run267f_adx_net_delta_vs_e",
            "run267f_adx_weakest_weekday_net",
            "run267f_adx_weakest_month_net",
            "run267f_di_net_delta_vs_d",
            "run267f_di_dd_delta_vs_d",
            "blocked_exact_repeat",
            "materialization_status",
            "claim_boundary",
        ),
    )
    write_csv(
        ADAPTER_SURFACE_PATH,
        adapter_rows,
        (
            "adapter_mode",
            "adapter_surface",
            "existing_support",
            "implementation_scope",
            "verification_need",
            "claim_boundary",
        ),
    )
    write_csv(
        EXPERIMENT_QUEUE_PATH,
        queue_rows,
        (
            "queue_id",
            "priority_lane",
            "candidate_alias",
            "candidate_role",
            "feature_design",
            "adapter_mode",
            "materialization_decision",
            "comparison_baseline",
            "success_criteria",
            "failure_criteria",
            "next_action",
            "claim_boundary",
        ),
    )
    write_json(
        LINEAGE_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "source_inputs": {
                "followup_design": rel(FOLLOWUP_DESIGN_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "stop_rules": rel(STOP_RULES_PATH),
                "guard_comparison": rel(GUARD_COMPARISON_PATH),
                "negative_slices": rel(NEGATIVE_SLICE_PATH),
            },
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_ACTION,
            "artifact_paths": result["outputs"],
            "availability": "tracked_after_commit_reproducible_from_command",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result, feature_rows, adapter_rows, queue_rows))
    update_current_truth_docs()
    update_ledgers(created_at, result)
    return result


def main() -> int:
    result = build()
    print(
        json.dumps(
            {
                "status": result["status"],
                "feature_rows": result["feature_rows"],
                "adapter_surface_rows": result["adapter_surface_rows"],
                "experiment_queue_rows": result["experiment_queue_rows"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
