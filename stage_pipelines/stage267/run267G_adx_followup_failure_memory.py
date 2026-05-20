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
RUN_ID = "run267G_stage267_adx_followup_failure_memory_v1"
RUN_NUMBER = "run267G"
STATUS = "run267G_adx_followup_failure_memory_completed"
NEXT_ACTION = "run267H_design_soft_noncalendar_adapter_feature_engineering_matrix"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_"
    "no_operating_reference_no_production_baseline_no_deployment_no_onnx_until_goal_gate"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "adx_followup_failure_memory"

RUN267F_ROOT = STAGE_ROOT / "02_runs" / "run267F" / "atrcomp_guard_robustness"
GUARD_COMPARISON_PATH = RUN267F_ROOT / "guard_comparison.csv"
NEGATIVE_SLICE_PATH = RUN267F_ROOT / "negative_slice_summary.csv"
RUN267F_REPORT_PATH = REVIEWS_ROOT / "stage267_run267F_guard_robustness_review.md"

FAILURE_MEMORY_PATH = DESIGN_ROOT / "failure_memory.csv"
FOLLOWUP_DESIGN_PATH = DESIGN_ROOT / "followup_design.csv"
STOP_RULES_PATH = DESIGN_ROOT / "stop_rules.csv"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267G_adx_followup_failure_memory.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267G_adx_followup_failure_memory.py")

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


def negative_by_candidate_guard(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str], list[Mapping[str, str]]]:
    grouped: dict[tuple[str, str], list[Mapping[str, str]]] = {}
    for row in rows:
        key = (str(row.get("candidate_alias", "")), str(row.get("guard_variant", "")))
        grouped.setdefault(key, []).append(row)
    for key, values in grouped.items():
        grouped[key] = sorted(values, key=lambda item: fnum(item.get("net_profit")))
    return grouped


def classify_guard(row: Mapping[str, str]) -> tuple[str, str, str]:
    guard = str(row.get("guard_variant", ""))
    if guard == "adx2025":
        return (
            "partial_support_keep_as_soft_context_seed",
            "ADX 20-25 hard guard(ADX 20-25 강한 방어)는 run267D(267D 실행) 대비 일부 개선이 있지만 run267E(267E 실행) Monday guard(월요일 방어)보다 약하고 Monday/July(월요일/7월)가 계속 깨졌다.",
            "정확한 hard prune(강한 절단)을 반복하지 말고 soft context feature(부드러운 문맥 피처), risk scaling(위험 배율), 또는 interaction term(상호작용 항)으로만 재사용한다.",
        )
    return (
        "negative_failure_memory_block_exact_repeat",
        "DI-low q33(DI 낮은 33%) replacement(대체)는 모든 후보에서 net/PF(순수익/수익 팩터)를 악화했고 DD(drawdown, 손실폭)를 키웠다.",
        "standalone q33 hard filter(단독 33% 강한 필터)는 반복 금지한다. DI spread(방향성 차이)는 ADX/ATR(추세 강도/ATR)와 결합된 연속 feature(피처)로만 재검토한다.",
    )


def build_failure_memory(
    comparisons: Sequence[Mapping[str, str]],
    negative_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    grouped_negatives = negative_by_candidate_guard(negative_rows)
    rows: list[dict[str, Any]] = []
    for row in comparisons:
        classification, evidence_read, reuse_rule = classify_guard(row)
        negatives = grouped_negatives.get((str(row.get("candidate_alias")), str(row.get("guard_variant"))), [])
        worst = negatives[0] if negatives else {}
        rows.append(
            {
                "run_id": RUN_ID,
                "source_run_id": "run267F_stage267_atrcomp_guard_robustness_non_calendar_v1",
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "guard_variant": row.get("guard_variant"),
                "guard_family": row.get("guard_family"),
                "classification": classification,
                "net_delta_vs_run267d_atrcomp": row.get("net_delta_vs_run267d_atrcomp"),
                "net_delta_vs_run267e_atrmon": row.get("net_delta_vs_run267e_atrmon"),
                "pf_delta_vs_run267d_atrcomp": row.get("pf_delta_vs_run267d_atrcomp"),
                "trade_delta_vs_run267d_atrcomp": row.get("trade_delta_vs_run267d_atrcomp"),
                "dd_delta_vs_run267d_atrcomp": row.get("dd_delta_vs_run267d_atrcomp"),
                "weakest_month": row.get("weakest_month"),
                "weakest_month_net": row.get("weakest_month_net"),
                "weakest_weekday": row.get("weakest_weekday"),
                "weakest_weekday_net": row.get("weakest_weekday_net"),
                "worst_negative_axis": worst.get("axis", ""),
                "worst_negative_bucket": worst.get("bucket", ""),
                "worst_negative_net": worst.get("net_profit", ""),
                "evidence_read": evidence_read,
                "reuse_rule": reuse_rule,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_followup_design(failure_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    aliases = sorted({str(row.get("candidate_alias")) for row in failure_rows})
    rows: list[dict[str, Any]] = []
    for alias in aliases:
        adx = next((row for row in failure_rows if row.get("candidate_alias") == alias and row.get("guard_variant") == "adx2025"), {})
        di = next((row for row in failure_rows if row.get("candidate_alias") == alias and row.get("guard_variant") == "dilowq33"), {})
        rows.append(
            {
                "design_id": f"run267H_soft_context_{alias}",
                "candidate_alias": alias,
                "candidate_role": adx.get("candidate_role") or di.get("candidate_role"),
                "source_evidence": "run267F adx2025 partial support; run267F dilowq33 exact replacement failure",
                "hypothesis": "ADX/ATR compression(추세 강도/ATR 압축) 정보는 hard prune(강한 절단)보다 soft feature/risk scale(부드러운 피처/위험 배율)로 쓰면 약한 월과 월요일 손상을 덜 만들 수 있다.",
                "decision_use": "run267H에서 실제 materialization(물질화) 후보를 만들지, 또는 이 guard branch(방어 분기)를 닫을지 결정한다.",
                "comparison_baseline": "run267D atrcomp, run267E Monday guard, run267F adx2025/dilowq33",
                "changed_variables": "hard guard(강한 방어)를 soft score(부드러운 점수), risk multiplier(위험 배율), interaction feature(상호작용 피처) 후보로 바꾼다.",
                "control_variables": "baseline candidate pool(기준 후보군), 2024 historical window(2024 과거 구간), MT5(MetaTrader 5, 메타트레이더5) execution settings(실행 설정), model identity(모델 정체성)",
                "success_criteria": "run267E 대비 손상 폭을 줄이면서 run267D 대비 net/PF(순수익/수익 팩터) 개선을 유지하고, Monday/July/chron_mid(월요일/7월/중간 구간) 약점이 커지지 않는다.",
                "failure_criteria": "trade count(거래 수)만 줄이고 약한 구간이 그대로면 실패다. DI q33 hard filter(33% 강한 필터) 재사용은 자동 실패다.",
                "invalid_conditions": "feature order(피처 순서), set/ini(설정/초기화), MT5 report(보고서), parser(파서), source hash(원천 해시) 중 하나라도 끊기면 무효다.",
                "stop_condition": "ADX/DI guard branch(방어 분기)는 run267H까지 materialize/execute/review(물질화/실행/검토) 중 하나로 결론을 낸다. 같은 hard guard(강한 방어)는 반복하지 않는다.",
                "status": "designed_not_materialized",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_stop_rules() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "run267G_stop_exact_dilowq33",
            "scope": "DI spread(방향성 차이) similar replacement(유사 대체)",
            "rule": "dilowq33 standalone hard filter(DI 낮은 33% 단독 강한 필터)는 반복 금지한다.",
            "effect": "run267F에서 모든 후보가 악화된 조건을 다시 실행해 시간을 쓰지 않는다.",
            "reopen_condition": "ADX/ATR/risk(추세 강도/ATR/위험)와 결합된 continuous feature(연속 피처)로 설계가 바뀔 때만 재개한다.",
        },
        {
            "rule_id": "run267G_stop_adx_hard_equivalence_claim",
            "scope": "ADX 20-25 hard guard(ADX 20-25 강한 방어)",
            "rule": "adx2025를 run267E Monday guard(월요일 방어)와 동급이라고 말하지 않는다.",
            "effect": "부분 지지 evidence(근거)를 후보 선택이나 ONNX(ONNX) 준비로 과장하지 않는다.",
            "reopen_condition": "soft feature/risk-scale(부드러운 피처/위험 배율) 형태로 materialize(물질화)하고 MT5(MetaTrader 5, 메타트레이더5) 검토까지 끝났을 때만 재평가한다.",
        },
        {
            "rule_id": "run267G_stop_monday_only_bottleneck",
            "scope": "weak-slice repair(약한 구간 수리)",
            "rule": "Monday(월요일) 손실만 줄이는 미세 조정으로 3 stage(단계) 이상 끌지 않는다.",
            "effect": "월요일 한 구간에 갇히지 않고 feature engineering(피처 엔지니어링)과 Adapter(어댑터) 구조로 넓힌다.",
            "reopen_condition": "월요일, 2024-07, chron_mid(중간 구간)를 동시에 설명하는 넓은 구조 가설이 있을 때만 재개한다.",
        },
    ]


def report_markdown(
    failure_rows: Sequence[Mapping[str, Any]],
    design_rows: Sequence[Mapping[str, Any]],
    stop_rows: Sequence[Mapping[str, Any]],
    result: Mapping[str, Any],
) -> str:
    adx_rows = [row for row in failure_rows if row.get("guard_variant") == "adx2025"]
    di_rows = [row for row in failure_rows if row.get("guard_variant") == "dilowq33"]
    best_adx = max(adx_rows, key=lambda row: fnum(row.get("net_delta_vs_run267d_atrcomp")), default={})
    worst_di = min(di_rows, key=lambda row: fnum(row.get("net_delta_vs_run267d_atrcomp")), default={})

    lines = [
        "# Stage267 Run267G ADX Follow-up and DI Failure Memory(267단계 267G ADX 후속과 DI 실패 기억)",
        "",
        "- action(행동): run267F(267F 실행)의 guard comparison(방어 비교)과 weak slices(약한 구간)를 failure memory(실패 기억), follow-up design(후속 설계), stop rules(중단 규칙)로 정리했다.",
        "- effect(효과): `adx2025`는 soft context seed(부드러운 문맥 씨앗)로만 남기고, `dilowq33` exact repeat(정확 반복)는 막아 다음 Adapter(어댑터) 연구가 좁은 미세조정에 갇히지 않게 한다.",
        f"- source_evidence(원천 근거): `{rel(GUARD_COMPARISON_PATH)}`, `{rel(NEGATIVE_SLICE_PATH)}`",
        f"- failure_rows(실패 기억 행): `{len(failure_rows)}`",
        f"- followup_design_rows(후속 설계 행): `{len(design_rows)}`",
        f"- stop_rule_rows(중단 규칙 행): `{len(stop_rows)}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "이전 단계 연구는 버려진 것이 아니라, 이제 실제 R&D racing(연구개발 경주) 문법으로 재사용되기 시작했다.",
        "run267F(267F 실행)는 ADX(추세 강도)가 약간의 구조 신호일 수 있음을 보여줬지만, 월요일과 7월 약점까지 해결하지는 못했다.",
        "DI spread(방향성 차이) q33 대체는 강하게 나빠졌으므로 같은 형태는 실패 기억으로 묶는다.",
        "",
        "## Key Reads(핵심 판독)",
        "",
        f"- best_adx_partial(가장 나은 ADX 부분 지지): `{best_adx.get('candidate_alias', '')}` net_delta_vs_run267D(267D 대비 순수익 변화) `{best_adx.get('net_delta_vs_run267d_atrcomp', '')}`, weakest_weekday(약한 요일) `{best_adx.get('weakest_weekday', '')}` `{best_adx.get('weakest_weekday_net', '')}`.",
        f"- worst_di_failure(가장 나쁜 DI 실패): `{worst_di.get('candidate_alias', '')}` net_delta_vs_run267D(267D 대비 순수익 변화) `{worst_di.get('net_delta_vs_run267d_atrcomp', '')}`, dd_delta_vs_run267D(267D 대비 손실폭 변화) `{worst_di.get('dd_delta_vs_run267d_atrcomp', '')}`.",
        "- selected_candidate(선택 후보): `none`.",
        "- ONNX readiness(ONNX 준비): `not_claimed`.",
        "",
        "## Failure Memory(실패 기억)",
        "",
        "| candidate(후보) | guard(방어) | classification(분류) | net vs D(267D 대비) | net vs E(267E 대비) | weakest(약점) | reuse rule(재사용 규칙) |",
        "| --- | --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in failure_rows:
        lines.append(
            f"| `{row['candidate_alias']}` | `{row['guard_variant']}` | `{row['classification']}` | {row['net_delta_vs_run267d_atrcomp']} | {row['net_delta_vs_run267e_atrmon']} | `{row['weakest_weekday']}` {row['weakest_weekday_net']}; `{row['weakest_month']}` {row['weakest_month_net']} | {row['reuse_rule']} |"
        )
    lines.extend(
        [
            "",
            "## Follow-up Design(후속 설계)",
            "",
            "- hypothesis(가설): ADX/ATR compression(추세 강도/ATR 압축)은 hard prune(강한 절단)보다 soft score/risk scale(부드러운 점수/위험 배율)로 구조화해야 덜 깨질 수 있다.",
            "- comparison_baseline(비교 기준): run267D(267D 실행), run267E(267E 실행), run267F(267F 실행).",
            "- success_criteria(성공 기준): net/PF(순수익/수익 팩터) 개선만이 아니라 Monday/July/chron_mid(월요일/7월/중간 구간)가 덜 깨져야 한다.",
            "- failure_criteria(실패 기준): 거래 수만 줄이거나 특정 약한 구간이 그대로면 실패다.",
            "- stop_condition(중단 조건): 같은 hard guard(강한 방어)는 반복하지 않고, run267H(267H 실행)에서 soft feature/risk-scale(부드러운 피처/위험 배율) 물질화 여부를 결정한다.",
            "",
            "## Stop Rules(중단 규칙)",
            "",
        ]
    )
    for row in stop_rows:
        lines.append(f"- `{row['rule_id']}`: {row['rule']} Effect(효과): {row['effect']}")
    lines.extend(
        [
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267G_adx_followup_failure_memory`.",
            "- evidence_available(사용 가능 근거): run267F MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표), guard comparison(방어 비교), weak slices(약한 구간), generated failure/design/stop files(생성 실패/설계/중단 파일).",
            "- evidence_missing(빠진 근거): run267H materialization/execution(물질화/실행), new balance/equity curve(잔액/평가금 곡선), expanded period(확장 기간) 재검증.",
            "- judgment_label(판정 라벨): `design_review_completed_no_candidate_selection`.",
            "- claim_boundary(주장 경계): design/failure-memory only(설계/실패 기억 전용). 후보 선택, ONNX(ONNX), 운영 의미를 주장하지 않는다.",
            f"- next_action(다음 행동): `{result['next_action']}`.",
        ]
    )
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        {
            "row_id": "stage267_run267G_adx_followup_failure_memory",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "adx_followup_failure_memory",
            "tier_scope": "Tier A and Tier A+B historical 2024 design review",
            "scoreboard": "structural_scout",
            "status": STATUS,
            "judgment": "design_review_completed_no_candidate_selection",
            "evidence_boundary": "failure_memory_and_followup_design_only_no_mt5_execution",
            "report_path": rel(REPORT_PATH),
            "notes": f"failure_rows={result['failure_rows']};followup_design_rows={result['followup_design_rows']};next_action={NEXT_ACTION}.",
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
            "lane": "baseline_candidate_racing_failure_memory_design",
            "status": STATUS,
            "judgment": "design_review_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"ADX partial support kept as soft context seed; DI q33 hard replacement blocked; next_action={NEXT_ACTION}.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__adx_followup_failure_memory",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adx_followup_failure_memory",
            "parent_run_id": RUN_ID,
            "record_view": "adx_followup_failure_memory",
            "tier_scope": "Tier A and Tier A+B historical 2024",
            "kpi_scope": "failure_memory_followup_design_stop_rules",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": "design_review_completed_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"failure_rows={result['failure_rows']};followup_design_rows={result['followup_design_rows']};stop_rules={result['stop_rule_rows']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;no_exact_dilowq33_repeat;no_adx_equivalence_claim",
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
        ("stage267_run267G_adx_followup_failure_memory_script", "producer_script", PRODUCER_PATH, "Builds run267G failure memory and follow-up design."),
        ("stage267_run267G_failure_memory", "failure_memory", FAILURE_MEMORY_PATH, "Run267G candidate/guard failure memory rows."),
        ("stage267_run267G_followup_design", "followup_design", FOLLOWUP_DESIGN_PATH, "Run267G ADX/DI follow-up design rows."),
        ("stage267_run267G_stop_rules", "stop_rules", STOP_RULES_PATH, "Run267G guard branch stop rules."),
        ("stage267_run267G_result", "result", RESULT_PATH, "Run267G result payload."),
        ("stage267_run267G_report", "review_report", REPORT_PATH, "User-facing run267G report."),
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
        "- Stage267(267단계) run267G ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억): "
        f"`{rel(REPORT_PATH)}`"
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_if_present(current, "- current_run(현재 실행): `run267F_stage267_atrcomp_guard_robustness_non_calendar_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_if_present(current, "- status(상태): `run267F_non_calendar_guard_mt5_review_completed`", f"- status(상태): `{STATUS}`")
    current = append_after(
        current,
        "- Stage267(267단계) run267F non-calendar guard MT5 review(비달력 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md`",
        evidence_line,
    )
    current = replace_if_present(
        current,
        "- next_run(다음 실행): `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`",
        f"- next_run(다음 실행): `{NEXT_ACTION}`",
    )
    current = replace_if_present(
        current,
        "- action(행동): run267F(267F 실행)의 비달력 guard(방어) 2종을 MT5(MetaTrader 5, 메타트레이더5)에서 실행하고 trade/time-slice/curve review(거래/시간 구간/곡선 검토)까지 완료했다.",
        "- action(행동): run267G(267G 실행)에서 run267F(267F 실행)의 ADX/DI guard(추세 강도/방향성 차이 방어)를 failure memory(실패 기억), follow-up design(후속 설계), stop rules(중단 규칙)로 정리했다.",
    )
    current = replace_if_present(
        current,
        "- effect(효과): `adx2025`는 부분 지지만 남기고, `dilowq33`는 유사 대체 악화로 실패 기억(failure memory, 실패 기억)에 남겨 다음 Adapter(어댑터) 설계를 좁힌다.",
        "- effect(효과): `adx2025`는 soft context seed(부드러운 문맥 씨앗)로만 남기고, `dilowq33` exact repeat(정확 반복)는 차단해 다음 Adapter(어댑터) 연구가 넓은 feature engineering(피처 엔지니어링)으로 이동하게 한다.",
    )
    current = replace_if_present(
        current,
        "- next_action(다음 행동): `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`. Effect(효과): ADX(추세 강도) guard(방어)의 후속 설계 여부와 DI spread(방향성 차이) replacement(대체)의 반복 금지 또는 재구성 조건을 정한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): hard guard(강한 방어)가 아니라 soft feature/risk-scale(부드러운 피처/위험 배율) 후보를 설계해 Monday/July/chron_mid(월요일/7월/중간 구간)를 함께 본다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_if_present(selection, "- stage_status(단계 상태): `run267F_non_calendar_guard_mt5_review_completed`", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_if_present(selection, "- current_run(현재 실행): `run267F_stage267_atrcomp_guard_robustness_non_calendar_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_if_present(selection, "- last_completed_run(마지막 완료 실행): `run267F_stage267_atrcomp_guard_robustness_non_calendar_v1`", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after(
        selection,
        "- run267F_non_calendar_guard_mt5_review(267F 비달력 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md`",
        f"- run267G_adx_followup_failure_memory(267G ADX 후속과 DI 실패 기억): `{rel(REPORT_PATH)}`",
    )
    selection = replace_if_present(selection, "- next_action(다음 행동): `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_if_present(
        selection,
        "Run267F(267F 실행)는 non-calendar guard MT5 review(비달력 방어 MT5 검토)를 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, `adx2025`는 부분 지지, `dilowq33`는 유사 대체 악화로 기록해 다음은 run267G(267G 실행) 실패 기억과 후속 설계로 간다.",
        "Run267G(267G 실행)는 ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억)를 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, `adx2025`는 soft context seed(부드러운 문맥 씨앗), `dilowq33`는 exact repeat block(정확 반복 차단)으로 다음 run267H(267H 실행) 설계에 넘긴다.",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_if_present(review, "- status(상태): `run267F_non_calendar_guard_mt5_review_completed`", f"- status(상태): `{STATUS}`")
    review = replace_if_present(review, "- current_run(현재 실행): `run267F_stage267_atrcomp_guard_robustness_non_calendar_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_if_present(review, "- last_completed_run(마지막 완료 실행): `run267F_stage267_atrcomp_guard_robustness_non_calendar_v1`", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after(
        review,
        "- run267F_non_calendar_guard_mt5_review(267F 비달력 방어 MT5 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md`",
        f"- run267G_adx_followup_failure_memory(267G ADX 후속과 DI 실패 기억): `{rel(REPORT_PATH)}`",
    )
    review = replace_if_present(
        review,
        "Run267F(267F 실행)는 non-calendar guard MT5 review(비달력 방어 MT5 검토)를 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)를 주장하지 않고, `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`에서 ADX(추세 강도) 후속 설계와 DI spread(방향성 차이) 실패 기억을 정리한다.",
        f"Run267G(267G 실행)는 ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억)를 완료했다.\nEffect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)를 주장하지 않고, `{NEXT_ACTION}`에서 soft non-calendar Adapter(부드러운 비달력 어댑터) feature engineering(피처 엔지니어링) 설계를 진행한다.",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_if_present(workspace, "current_run_id: run267F_stage267_atrcomp_guard_robustness_non_calendar_v1", f"current_run_id: {RUN_ID}")
    workspace = replace_if_present(workspace, "  status: run267F_non_calendar_guard_mt5_review_completed", f"  status: {STATUS}")
    workspace = replace_if_present(workspace, "  current_run_id: run267F_stage267_atrcomp_guard_robustness_non_calendar_v1", f"  current_run_id: {RUN_ID}")
    workspace = replace_if_present(workspace, "  last_completed_run_id: run267F_stage267_atrcomp_guard_robustness_non_calendar_v1", f"  last_completed_run_id: {RUN_ID}")
    workspace = append_after(
        workspace,
        "  run267F_non_calendar_guard_mt5_review_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267F_guard_robustness_review.md",
        f"  run267G_adx_followup_failure_memory_path: {rel(REPORT_PATH)}",
    )
    workspace = replace_if_present(workspace, "  next_action: run267G_design_adx_guard_followup_and_di_replacement_failure_memory", f"  next_action: {NEXT_ACTION}")
    workspace = replace_if_present(
        workspace,
        "Stage267(267단계) run267F(267F 실행) non-calendar guard MT5 review(비달력 방어 MT5 검토) `run267F_non_calendar_guard_mt5_review_completed`. Effect(효과): 비달력 guard(방어)의 trade/time-slice/curve review(거래/시간 구간/곡선 검토)를 완료했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        f"Stage267(267단계) run267G(267G 실행) ADX follow-up and DI failure memory(ADX 후속과 DI 실패 기억) `{STATUS}`. Effect(효과): run267F(267F 실행)의 ADX(추세 강도) 부분 지지와 DI spread(방향성 차이) 악화를 failure memory(실패 기억)와 next design(다음 설계)으로 정리했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace = replace_if_present(
        workspace,
        "Next action(다음 행동)는 `run267G_design_adx_guard_followup_and_di_replacement_failure_memory`이다. Effect(효과): `adx2025`는 부분 지지만 남기고, `dilowq33`는 유사 대체 악화로 실패 기억(failure memory, 실패 기억)에 남겨 다음 Adapter(어댑터) 설계 방향을 좁힌다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): hard guard(강한 방어)를 반복하지 않고 soft feature/risk-scale(부드러운 피처/위험 배율) Adapter(어댑터) 설계로 확장한다.",
    )
    workspace = replace_if_present(
        workspace,
        "active_run267F_non_calendar_guard_mt5_review_completed(267F 비달력 방어 MT5 검토 완료 활성)",
        "active_run267G_adx_followup_failure_memory_completed(267G ADX 후속과 DI 실패 기억 완료 활성)",
    )
    write_md(WORKSPACE_STATE_PATH, workspace)


def build() -> dict[str, Any]:
    created_at = utc_now()
    comparisons = read_csv(GUARD_COMPARISON_PATH)
    negatives = read_csv(NEGATIVE_SLICE_PATH)
    if not comparisons:
        raise RuntimeError(f"missing comparison rows: {GUARD_COMPARISON_PATH}")

    failure_rows = build_failure_memory(comparisons, negatives)
    design_rows = build_followup_design(failure_rows)
    stop_rows = build_stop_rules()
    result = {
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "source_run_id": "run267F_stage267_atrcomp_guard_robustness_non_calendar_v1",
        "failure_rows": len(failure_rows),
        "followup_design_rows": len(design_rows),
        "stop_rule_rows": len(stop_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "followup_design": rel(FOLLOWUP_DESIGN_PATH),
            "stop_rules": rel(STOP_RULES_PATH),
            "report": rel(REPORT_PATH),
        },
    }

    write_csv(
        FAILURE_MEMORY_PATH,
        failure_rows,
        (
            "run_id",
            "source_run_id",
            "candidate_alias",
            "candidate_role",
            "guard_variant",
            "guard_family",
            "classification",
            "net_delta_vs_run267d_atrcomp",
            "net_delta_vs_run267e_atrmon",
            "pf_delta_vs_run267d_atrcomp",
            "trade_delta_vs_run267d_atrcomp",
            "dd_delta_vs_run267d_atrcomp",
            "weakest_month",
            "weakest_month_net",
            "weakest_weekday",
            "weakest_weekday_net",
            "worst_negative_axis",
            "worst_negative_bucket",
            "worst_negative_net",
            "evidence_read",
            "reuse_rule",
            "claim_boundary",
        ),
    )
    write_csv(
        FOLLOWUP_DESIGN_PATH,
        design_rows,
        (
            "design_id",
            "candidate_alias",
            "candidate_role",
            "source_evidence",
            "hypothesis",
            "decision_use",
            "comparison_baseline",
            "changed_variables",
            "control_variables",
            "success_criteria",
            "failure_criteria",
            "invalid_conditions",
            "stop_condition",
            "status",
            "claim_boundary",
        ),
    )
    write_csv(STOP_RULES_PATH, stop_rows, ("rule_id", "scope", "rule", "effect", "reopen_condition"))
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(failure_rows, design_rows, stop_rows, result))
    update_current_truth_docs()
    update_ledgers(created_at, result)
    return result


def main() -> int:
    result = build()
    print(
        json.dumps(
            {
                "status": result["status"],
                "failure_rows": result["failure_rows"],
                "followup_design_rows": result["followup_design_rows"],
                "stop_rule_rows": result["stop_rule_rows"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
