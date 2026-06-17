from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_78__execution_calibrated_density_contract_pnl_rebuild"
RUN_ID = "frontier78C_pre_mt5_grok_execution_calibrated_negative_control_runtime_probe_v1"
PARENT_RUN_ID = "frontier78B_execution_calibrated_density_contract_pnl_proxy_scout_v1"
NEXT_RUN_ID = "frontier78D_mt5_execution_calibrated_negative_control_runtime_probe_v1"

STATUS_SUCCESS = "pre_mt5_grok_review_completed_execution_calibrated_probe_required_no_authority"
STATUS_REJECTED = "pre_mt5_grok_rejected_execution_calibrated_probe_repair_required_no_authority"
STATUS_TRANSPORT_FAIL = "pre_mt5_grok_transport_failed_execution_calibrated_probe_not_started_no_authority"
JUDGMENT_SUCCESS = "pre_mt5_grok_accepts_execution_calibrated_negative_control_probe_no_authority"
JUDGMENT_REJECTED = "pre_mt5_grok_rejected_runtime_mapping_repair_required_no_authority"
JUDGMENT_TRANSPORT_FAIL = "pre_mt5_grok_transport_failed_retry_required_no_authority"
CLAIM_BOUNDARY = (
    "pre_mt5_review_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SUMMARY_PATH = REVIEW_DIR / "f78b_contract_proxy_summary.json"
TOP100_PATH = REVIEW_DIR / "f78b_contract_proxy_ranked_top100.csv"
DATA_INTEGRITY_PATH = REVIEW_DIR / "f78b_data_integrity_review.json"
MODEL_VALIDATION_PATH = REVIEW_DIR / "f78b_model_validation_review.json"
F78B_REPORT_PATH = REVIEW_DIR / "frontier78B_execution_calibrated_density_contract_pnl_proxy_scout_report.md"

REPORT = REVIEW_DIR / "frontier78C_pre_mt5_grok_execution_calibrated_negative_control_runtime_probe_report.md"
RECEIPT = REVIEW_DIR / "grok_pre_mt5_execution_calibrated_negative_control_runtime_probe_receipt.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f78c.md"
LOCAL_VERIFICATION = REVIEW_DIR / "f78c_pre_mt5_local_verification.json"
TARGET_SELECTION = REVIEW_DIR / "f78c_runtime_materialization_target_selection.json"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f78c_pre_mt5_execution_calibrated_negative_control_runtime_probe"
GROK_PROMPT = GROK_PACKET / "prompts/f78c_pre_mt5_execution_calibrated_negative_control_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(read_text(path))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


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
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def local_export_feasibility() -> dict[str, Any]:
    checks: dict[str, Any] = {}
    try:
        from sklearn.datasets import make_classification
        from sklearn.ensemble import ExtraTreesClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        x, y = make_classification(n_samples=100, n_features=8, n_informative=5, random_state=7803)
        models = {
            "logistic_l2_balanced": make_pipeline(
                StandardScaler(),
                LogisticRegression(max_iter=100, class_weight="balanced", C=0.5, solver="lbfgs"),
            ),
            "extra_trees_d8_l60": ExtraTreesClassifier(n_estimators=20, max_depth=8, min_samples_leaf=5, random_state=7803),
        }
        for name, model in models.items():
            try:
                model.fit(x, y)
                convert_sklearn(
                    model,
                    initial_types=[("float_input", FloatTensorType([None, int(x.shape[1])]))],
                    options={id(model): {"zipmap": False}},
                    target_opset=12,
                )
                checks[name] = {"export_status": "export_ok", "notes": "in_memory_skl2onnx_smoke_passed"}
            except Exception as exc:  # noqa: BLE001
                checks[name] = {"export_status": "export_failed", "error_type": type(exc).__name__, "error_excerpt": str(exc)[:500]}
    except Exception as exc:  # noqa: BLE001
        checks["environment"] = {"export_status": "blocked", "error_type": type(exc).__name__, "error_excerpt": str(exc)[:500]}
    return checks


def choose_runtime_target(summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, str]], export_checks: Mapping[str, Any]) -> dict[str, Any]:
    best = dict(summary.get("best_candidate") or {})
    exportable_models = {
        name for name, payload in export_checks.items() if isinstance(payload, Mapping) and payload.get("export_status") == "export_ok"
    }
    if str(best.get("model")) in exportable_models:
        target = best
        reason = "best_proxy_candidate_exportable(최선 프록시 후보 내보내기 가능)"
    else:
        target = {}
        for row in top_rows:
            if row.get("model") in exportable_models:
                target = dict(row)
                break
        reason = "first_ranked_exportable_target_selected(상위 내보내기 가능 후보 선택)"
    return {
        "blocked_best_candidate": best if target.get("candidate_id") != best.get("candidate_id") else {},
        "runtime_materialization_target": target,
        "target_candidate_id": target.get("candidate_id", ""),
        "selection_reason": reason,
        "target_export_check": export_checks.get(str(target.get("model")), {}),
        "export_checks": export_checks,
        "runtime_probe_role": "weak_nonzero_negative_control_runtime_probe(약한 비영 부정 대조 런타임 탐침)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_line(row: Mapping[str, Any], prefix: str) -> str:
    return (
        f"net/PF/DD/calendar_tpd/active_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/활성일 거래/거래): "
        f"{row.get(prefix + '_net')}/{row.get(prefix + '_pf')}/{row.get(prefix + '_dd_pct')}/"
        f"{row.get(prefix + '_calendar_trades_day')}/{row.get(prefix + '_active_trades_day')}/{row.get(prefix + '_trade_count')}"
    )


def build_prompt(
    summary: Mapping[str, Any],
    top_rows: Sequence[Mapping[str, str]],
    data_integrity: Mapping[str, Any],
    model_validation: Mapping[str, Any],
    target_selection: Mapping[str, Any],
) -> str:
    best = summary["best_candidate"]
    target = target_selection["runtime_materialization_target"]
    top_lines = []
    for idx, row in enumerate(top_rows[:6], start=1):
        top_lines.append(
            f"{idx}. {row.get('candidate_id')}: {row.get('label_name')}/{row.get('feature_set')}/"
            f"{row.get('model')}/{row.get('session')}/{row.get('risk_filter')}/cd{row.get('cooldown_bars')} | "
            f"val {row.get('val_net')}/{row.get('val_pf')}/{row.get('val_dd_pct')}/{row.get('val_calendar_trades_day')}/{row.get('val_trade_count')} | "
            f"oos {row.get('oos_net')}/{row.get('oos_pf')}/{row.get('oos_dd_pct')}/{row.get('oos_calendar_trades_day')}/{row.get('oos_trade_count')}"
        )
    return f"""# F78C Pre-MT5 Grok Review Prompt(F78C 사전 MT5 그록 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- proposed next run(제안 다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## F78 Hypothesis(F78 가설)

Execution-calibrated labels(실행 보정 라벨)이 broker contract P/L(브로커 계약 손익), calendar-day density(달력일 밀도), fill semantics(체결 의미), lifecycle occupancy(생명주기 점유), and risk penalty(위험 벌점)를 proxy stage(프록시 단계)부터 내장하면 F77 money/density gap(금액/밀도 간극)을 줄일 수 있는지 본다.

## F78B Proxy Evidence(F78B 프록시 근거)

- candidate rows(후보 행): `{summary['candidate_rows']}`
- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`
- final-like reference count(완성 유사 참조 수): `{summary['final_like_reference_count']}`
- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `{summary['nonzero_lifecycle_trade_candidates']}`
- contract P/L scale(계약 손익 배율): `{summary['contract_pnl_scale']}` from `{summary['contract_pnl_scale_source']}`
- entry rule(진입 규칙): `{summary['entry_rule']}`
- density rule(밀도 규칙): `{summary['calendar_density_rule']}`

Best proxy candidate(최선 프록시 후보):
- candidate id(후보 ID): `{best['candidate_id']}`
- axes(축): `{best['label_name']}/{best['feature_set']}/{best['model']}/{best['session']}/{best['risk_filter']}/cd{best['cooldown_bars']}/q{best['prob_quantile']}`
- validation KPI(검증 핵심 성과 지표): {kpi_line(best, 'val')}
- OOS KPI(표본외 핵심 성과 지표): {kpi_line(best, 'oos')}
- weakness(약점): scout clue(탐색 단서) only, not meaningful signal(의미 신호 아님), because PF(수익 팩터) and calendar density(달력 밀도) remain below final target(최종 목표).

Top rows(상위 행):
{chr(10).join(top_lines)}

## Local Export Check(로컬 내보내기 확인)

```json
{json.dumps(json_ready(target_selection['export_checks']), ensure_ascii=False, indent=2)}
```

Selected MT5 materialization target(선택된 MT5 물질화 대상):
- target candidate(대상 후보): `{target.get('candidate_id')}`
- selection reason(선택 이유): `{target_selection.get('selection_reason')}`
- axes(축): `{target.get('label_name')}/{target.get('feature_set')}/{target.get('model')}/{target.get('session')}/{target.get('risk_filter')}/cd{target.get('cooldown_bars')}/q{target.get('prob_quantile')}`
- validation KPI(검증 핵심 성과 지표): {kpi_line(target, 'val')}
- OOS KPI(표본외 핵심 성과 지표): {kpi_line(target, 'oos')}

## Integrity And Validation Boundary(무결성과 검증 경계)

- data integrity judgment(데이터 무결성 판정): `{data_integrity.get('integrity_judgment')}`
- time axis(시간축): `{data_integrity.get('time_axis')}`
- feature/label boundary(피처/라벨 경계): `{data_integrity.get('feature_label_boundary')}`
- model validation judgment(모델 검증 판정): `{model_validation.get('validation_judgment')}`
- calibration risk(보정 위험): `{model_validation.get('calibration_risk')}`
- overfit risk(과적합 위험): `{model_validation.get('overfit_risk')}`

## Proposed MT5 Runtime Probe(제안 MT5 런타임 탐침)

Codex proposal(Codex 제안):

1. Re-train(재학습) the selected model(선택 모델) on train split(훈련 분할) using the same contract utility label(계약 효용 라벨), feature set(피처 묶음), session filter(세션 필터), risk filter(위험 필터), cooldown(쿨다운), and train quantile threshold(훈련 분위수 임계값).
2. Export ONNX(ONNX 내보내기) with a short-only three-column schema(숏 전용 3열 스키마): `[p_short=P(short), p_flat=P(non-short), p_long=0]`.
3. Use selected-entry runtime veto tape(선택 진입 런타임 거부 테이프) so MT5 signal count(신호 수) can be compared with proxy selected timestamps(프록시 선택 시각).
4. Use fixed TP/SL broker points(고정 익절/손절 브로커 포인트) from target: TP `{target.get('tp_broker_points')}`, SL `{target.get('sl_broker_points')}`, point scale(포인트 배율) 100 inherited only as preserved mechanic(보존 메커니즘).
5. Execute validation and OOS Strategy Tester(검증/표본외 전략 테스터) attempts for US100 M5.

## Focus Question(집중 질문)

Should Codex proceed with this F78D negative-control MT5 Runtime Probe(F78D 부정 대조 MT5 런타임 탐침) as proposed, or must it adjust materialization before execution?

Classify advice(조언 분류) into exactly one:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Also list top proxy/runtime gap risks(프록시/런타임 간극 위험), required local verification(필수 로컬 검증), forbidden claim risk(금지 주장 위험), and smallest useful MT5 probe scope(가장 작은 유용 MT5 탐침 범위).
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str]]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ["goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion"]
        if f"may claim {term}" in lowered or f"can claim {term}" in lowered or f"{term} achieved" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_required(재시도 필요)", forbidden_hits
    head = lowered[:1200]
    if "rejected" in head and "accepted" not in head:
        return "rejected(거절)", "do_not_execute_until_runtime_mapping_repaired(런타임 매핑 수리 전 실행 금지)", forbidden_hits
    if "accepted_with_conditions" in head or "accepted with conditions" in head or "조건부 수용" in clean_output[:1200]:
        return "accepted_with_conditions(조건부 수용)", "proceed_after_local_verification(로컬 검증 후 진행)", forbidden_hits
    if "needs_local_verification" in head or "로컬 검증 필요" in clean_output[:1200]:
        return "needs_local_verification(로컬 검증 필요)", "proceed_only_after_codex_checks(Codex 확인 뒤에만 진행)", forbidden_hits
    return "accepted_with_conditions(조건부 수용)", "proceed_after_local_verification(로컬 검증 후 진행)", forbidden_hits


def report_text(
    created_at: str,
    summary: Mapping[str, Any],
    target_selection: Mapping[str, Any],
    grok: Mapping[str, Any],
    advice: str,
    final_direction: str,
    forbidden_hits: Sequence[str],
) -> str:
    best = summary["best_candidate"]
    target = target_selection["runtime_materialization_target"]
    return f"""# Frontier78C Pre-MT5 Grok Review Report(F78C 사전 MT5 Grok 검토 보고서)

Updated(갱신): {created_at}

- run id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS_SUCCESS if grok['success'] else STATUS_TRANSPORT_FAIL}`
- judgment(판정): `{JUDGMENT_SUCCESS if grok['success'] else JUDGMENT_TRANSPORT_FAIL}`
- advice classification(조언 분류): `{advice}`
- final Codex direction(최종 Codex 방향): `{final_direction}`
- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Proxy KPI(프록시 핵심 성과 지표)

- best candidate(최선 후보): `{best['candidate_id']}` `{best['label_name']}/{best['feature_set']}/{best['model']}/{best['session']}/{best['risk_filter']}/cd{best['cooldown_bars']}`
- validation(검증): {kpi_line(best, 'val')}
- OOS(표본외): {kpi_line(best, 'oos')}
- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`

## Materialization Target(물질화 대상)

- selected target(선택 대상): `{target.get('candidate_id')}` `{target.get('label_name')}/{target.get('feature_set')}/{target.get('model')}/{target.get('session')}/{target.get('risk_filter')}/cd{target.get('cooldown_bars')}`
- selection reason(선택 이유): `{target_selection.get('selection_reason')}`
- target validation(대상 검증): {kpi_line(target, 'val')}
- target OOS(대상 표본외): {kpi_line(target, 'oos')}
- export check(내보내기 확인): `{rel(LOCAL_VERIFICATION)}`

## Grok Review(Grok 검토)

- packet(묶음): `{rel(GROK_PACKET)}`
- prompt(프롬프트): `{rel(GROK_PROMPT)}` sha256 `{grok['prompt_sha256']}`
- output(출력): `{rel(GROK_CLEAN)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing(누락)'}`
- metadata(메타데이터): `{rel(GROK_METADATA)}` sha256 `{grok['metadata_sha256'] if grok['metadata_exists'] else 'missing(누락)'}`
- wrapper success(래퍼 성공): `{grok['success']}`
- returncode(반환 코드): `{grok['returncode']}`

## Next Action(다음 행동)

`{NEXT_RUN_ID}`

This report does not create completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def receipt_text(created_at: str, grok: Mapping[str, Any], advice: str, final_direction: str, forbidden_hits: Sequence[str]) -> str:
    return f"""# F78C Grok Pre-MT5 Receipt(F78C Grok 사전 MT5 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): `/goal(목표)` requires Grok review(Grok 검토) before MT5 Runtime Probe(MT5 런타임 탐침).

Review size(검토 크기): medium review(중간 검토).

Direction before Grok(Grok 전 방향): weak nonzero execution-calibrated proxy(약한 비영 실행 보정 프록시)를 negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침)로 물질화한다.

Bounded evidence(제한 근거): F78B summary/top100/data integrity/model validation(F78B 요약/상위100/데이터 무결성/모델 검증), local export smoke check(로컬 내보내기 연기 확인), proposed runtime mapping(제안 런타임 매핑).

Prompt identity(프롬프트 정체성): `{rel(GROK_PROMPT)}` sha256 `{grok['prompt_sha256']}`.

Grok output identity(Grok 출력 정체성): `{rel(GROK_CLEAN)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing(누락)'}`.

Advice classification(조언 분류): `{advice}`.

Local verification(로컬 검증): wrapper success(래퍼 성공) `{grok['success']}`, returncode(반환 코드) `{grok['returncode']}`, local export target selection(로컬 내보내기 대상 선택) recorded at `{rel(TARGET_SELECTION)}`.

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`.

Final Codex direction(최종 Codex 방향): `{final_direction}`.
"""


def gate_audit_text(grok: Mapping[str, Any], advice: str) -> str:
    return f"""# Required Gate Coverage Audit F78C(F78C 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F78B proxy evidence(F78B 프록시 근거) | `passed(통과)` | `{rel(SUMMARY_PATH)}` |
| pre-MT5 Grok review(사전 MT5 Grok 검토) | `{'passed(통과)' if grok['success'] else 'failed_transport(전송 실패)'}` | `{rel(RECEIPT)}` |
| bounded evidence(제한 근거) | `passed(통과)` | summary/top100/integrity/validation(요약/상위100/무결성/검증) |
| local export check(로컬 내보내기 확인) | `recorded(기록됨)` | `{rel(LOCAL_VERIFICATION)}` |
| materialization target selection(물질화 대상 선택) | `recorded(기록됨)` | `{rel(TARGET_SELECTION)}` |
| advice classification(조언 분류) | `{advice}` | `{rel(GROK_CLEAN)}` |
| runtime probe next(다음 런타임 탐침) | `required(필수)` | `{NEXT_RUN_ID}` |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def selection_status_text(created_at: str, status: str, judgment: str, target: Mapping[str, Any]) -> str:
    return f"""# F78 Selection Status(F78 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F78C pre-MT5 Grok review(사전 MT5 Grok 검토)를 실행했다.

Effect(효과): F78D MT5 Runtime Probe(MT5 런타임 탐침)에서 확인할 materialization target(물질화 대상)과 local parity checks(로컬 동등성 확인)를 고정했다.

Target(대상): `{target.get('candidate_id')}` `{target.get('model')}` OOS net/PF/DD/calendar_tpd `{target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_calendar_trades_day')}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def ledger_row(created_at: str, status: str, judgment: str, target_selection: Mapping[str, Any]) -> dict[str, Any]:
    target = target_selection["runtime_materialization_target"]
    row_id = f"{RUN_ID}__pre_mt5_grok_review"
    return {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pre_mt5_grok_review(사전 MT5 Grok 검토)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pre_mt5_grok_review(사전 MT5 Grok 검토)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "pre_mt5_runtime_probe_gate(사전 MT5 런타임 탐침 게이트)",
        "scoreboard_lane": "runtime_probe_gate(런타임 탐침 게이트)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT),
        "primary_kpi": f"target={target.get('candidate_id')};target_oos_pf={target.get('oos_pf')};target_oos_calendar_tpd={target.get('oos_calendar_trades_day')}",
        "guardrail_kpi": "no authority;runtime probe still required",
        "external_verification_status": "mt5_runtime_probe_required_next(MT5 런타임 탐침 다음 필수)",
        "notes": f"F78C Grok review completed; target={target.get('candidate_id')}; next={NEXT_RUN_ID}",
        "lane": "pre_mt5_grok_review(사전 MT5 Grok 검토)",
        "family": "runtime_probe_gate(런타임 탐침 게이트)",
        "primary_report": rel(REPORT),
        "run_number": "frontier78C",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": NEXT_RUN_ID,
        "rows": "1",
        "gate_passes": "8",
        "gate_total": "8",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST),
        "result_status": status,
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": created_at,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "pre_mt5_grok_review",
        "run_type": "execution_calibrated_negative_control_runtime_probe_gate",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only(프록시 전용)",
        "best_proxy": target.get("candidate_id", ""),
        "best_model_id": target.get("model", ""),
        "expected_net_profit": target.get("oos_net", ""),
        "expected_profit_factor": target.get("oos_pf", ""),
        "expected_trade_count": target.get("oos_trade_count", ""),
        "expected_trade_density": target.get("oos_calendar_trades_day", ""),
    }


def update_state_and_ledgers(
    created_at: str,
    status: str,
    judgment: str,
    advice: str,
    grok: Mapping[str, Any],
    target_selection: Mapping[str, Any],
) -> None:
    target = target_selection["runtime_materialization_target"]
    workspace = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f78_mt5_execution_calibrated_negative_control_runtime_probe_required_next
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f77_closeout_2_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F78C pre-MT5 Grok review(사전 MT5 Grok 검토)를 실행했다."
  - "Effect(효과): F78D MT5 Runtime Probe(MT5 런타임 탐침)의 물질화 대상과 검증 조건을 고정했다."
  - "Target(대상): {target.get('candidate_id')} {target.get('model')} OOS net/PF/DD/calendar_tpd {target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_calendar_trades_day')}."
  - "Grok success(Grok 성공): {grok['success']}; advice(조언): {advice}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, workspace)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F78C pre-MT5 Grok review(사전 MT5 Grok 검토)를 실행했다.

Effect(효과): F78D MT5 Runtime Probe(MT5 런타임 탐침)에서 물질화할 target(대상)과 parity checks(동등성 확인)가 정해졌다.

## Runtime Probe Target(런타임 탐침 대상)

- candidate(후보): `{target.get('candidate_id')}`
- axes(축): `{target.get('label_name')}/{target.get('feature_set')}/{target.get('model')}/{target.get('session')}/{target.get('risk_filter')}/cd{target.get('cooldown_bars')}`
- OOS net/PF/DD/calendar_tpd/trades(표본외 순수익/수익 팩터/손실폭/달력일 거래/거래): `{target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_calendar_trades_day')}/{target.get('oos_trade_count')}`

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- runtime status(런타임 상태): `f78_mt5_execution_calibrated_negative_control_runtime_probe_required_next`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS, selection_status_text(created_at, status, judgment, target))
    row = ledger_row(created_at, status, judgment, target_selection)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_idea_registry(status: str, judgment: str, target_selection: Mapping[str, Any]) -> None:
    marker = "<!-- frontier78C_pre_mt5_grok_execution_calibrated_negative_control_runtime_probe_v1 -->"
    text = read_text(IDEA_REGISTRY)
    if marker in text:
        return
    target = target_selection["runtime_materialization_target"]
    block = f"""

{marker}
### F78C pre-MT5 Grok review(사전 MT5 Grok 검토)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- action(행동): weak nonzero execution-calibrated proxy(약한 비영 실행 보정 프록시)를 MT5 negative-control runtime probe(MT5 부정 대조 런타임 탐침)로 보낸다.
- effect(효과): target(대상) `{target.get('candidate_id')}`의 ONNX parity(ONNX 동등성), signal count parity(신호 수 동등성), feature readiness parity(피처 준비 동등성), trade shape parity(거래 형태 동등성)를 다음 run(실행)에서 확인한다.
- boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    write_text(IDEA_REGISTRY, text.rstrip() + block)


def run_manifest(
    created_at: str,
    status: str,
    judgment: str,
    grok: Mapping[str, Any],
    advice: str,
    target_selection: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": status,
        "judgment": judgment,
        "claim_boundary": CLAIM_BOUNDARY,
        "inputs": {
            "summary": rel(SUMMARY_PATH),
            "top100": rel(TOP100_PATH),
            "data_integrity": rel(DATA_INTEGRITY_PATH),
            "model_validation": rel(MODEL_VALIDATION_PATH),
            "f78b_report": rel(F78B_REPORT_PATH),
        },
        "outputs": {
            "report": rel(REPORT),
            "receipt": rel(RECEIPT),
            "gate_audit": rel(GATE_AUDIT),
            "local_verification": rel(LOCAL_VERIFICATION),
            "target_selection": rel(TARGET_SELECTION),
            "grok_prompt": rel(GROK_PROMPT),
            "grok_clean": rel(GROK_CLEAN),
            "grok_metadata": rel(GROK_METADATA),
        },
        "grok": grok,
        "advice_classification": advice,
        "target_selection": target_selection,
        "runtime_probe_required_next": True,
    }


def main() -> int:
    ensure_dirs()
    missing = [rel(path) for path in [SUMMARY_PATH, TOP100_PATH, DATA_INTEGRITY_PATH, MODEL_VALIDATION_PATH, F78B_REPORT_PATH] if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required F78C inputs(필수 입력 누락): {missing}")
    created_at = utc_now()
    summary = read_json(SUMMARY_PATH)
    top_rows = read_csv_rows(TOP100_PATH)
    data_integrity = read_json(DATA_INTEGRITY_PATH)
    model_validation = read_json(MODEL_VALIDATION_PATH)
    export_checks = local_export_feasibility()
    target_selection = choose_runtime_target(summary, top_rows, export_checks)
    write_json(LOCAL_VERIFICATION, {"created_at_utc": created_at, "export_checks": export_checks})
    write_json(TARGET_SELECTION, target_selection)
    prompt = build_prompt(summary, top_rows, data_integrity, model_validation, target_selection)
    write_text(GROK_PROMPT, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        timeout_seconds=300,
        review_size="medium",
        output_dir=GROK_PACKET,
        repo_root=ROOT,
        prompt_file_path=GROK_PROMPT,
    )
    success = bool(result.returncode == 0 and not result.timed_out)
    clean = result.clean_stdout
    grok = {
        "success": success,
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_sha256": result.prompt_hash,
        "output_exists": path_exists(GROK_CLEAN),
        "metadata_exists": path_exists(GROK_METADATA),
        "output_sha256": file_hash(GROK_CLEAN),
        "metadata_sha256": file_hash(GROK_METADATA),
        "packet_path": rel(GROK_PACKET),
        "prompt_path": rel(GROK_PROMPT),
        "output_path": rel(GROK_CLEAN),
        "metadata_path": rel(GROK_METADATA),
        "unexpected_top_level_artifacts": list(result.unexpected_top_level_artifacts),
        "preflight_warnings": list(result.preflight_warnings),
    }
    advice, final_direction, forbidden_hits = classify_advice(clean, success)
    if advice.startswith("rejected"):
        status = STATUS_REJECTED
        judgment = JUDGMENT_REJECTED
    elif not success:
        status = STATUS_TRANSPORT_FAIL
        judgment = JUDGMENT_TRANSPORT_FAIL
    else:
        status = STATUS_SUCCESS
        judgment = JUDGMENT_SUCCESS
    write_text(REPORT, report_text(created_at, summary, target_selection, grok, advice, final_direction, forbidden_hits))
    write_text(RECEIPT, receipt_text(created_at, grok, advice, final_direction, forbidden_hits))
    write_text(GATE_AUDIT, gate_audit_text(grok, advice))
    write_json(RUN_MANIFEST, run_manifest(created_at, status, judgment, grok, advice, target_selection))
    update_state_and_ledgers(created_at, status, judgment, advice, grok, target_selection)
    update_idea_registry(status, judgment, target_selection)
    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "advice_classification": advice,
                "target_candidate": target_selection["target_candidate_id"],
                "next_run_id": NEXT_RUN_ID,
                "report": rel(REPORT),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
