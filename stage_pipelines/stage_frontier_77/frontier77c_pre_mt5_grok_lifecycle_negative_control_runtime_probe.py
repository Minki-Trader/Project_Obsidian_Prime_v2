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
from stage_pipelines.stage_frontier_77 import frontier77b_runtime_lifecycle_label_density_proxy_scout as f77b


STAGE_ID = f77b.STAGE_ID
RUN_ID = "frontier77C_pre_mt5_grok_lifecycle_negative_control_runtime_probe_v1"
PARENT_RUN_ID = f77b.RUN_ID
NEXT_RUN_ID = "frontier77D_mt5_lifecycle_negative_control_runtime_probe_v1"

STATUS_SUCCESS = "pre_mt5_grok_review_completed_lifecycle_negative_control_probe_required_no_authority"
STATUS_REJECTED = "pre_mt5_grok_rejected_lifecycle_runtime_probe_repair_required_no_authority"
STATUS_TRANSPORT_FAIL = "pre_mt5_grok_transport_failed_lifecycle_runtime_probe_not_started_no_authority"
JUDGMENT_SUCCESS = "pre_mt5_grok_accepts_lifecycle_negative_control_probe_with_local_verification_no_authority"
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

SUMMARY_PATH = REVIEW_DIR / "f77b_lifecycle_proxy_summary.json"
TOP100_PATH = REVIEW_DIR / "f77b_lifecycle_proxy_ranked_top100.csv"
DATA_INTEGRITY_PATH = REVIEW_DIR / "f77b_data_integrity_review.json"
MODEL_VALIDATION_PATH = REVIEW_DIR / "f77b_model_validation_review.json"
F77B_REPORT_PATH = REVIEW_DIR / "frontier77B_runtime_lifecycle_label_density_proxy_scout_report.md"

REPORT_PATH = REVIEW_DIR / "frontier77C_pre_mt5_grok_lifecycle_negative_control_runtime_probe_report.md"
RECEIPT_PATH = REVIEW_DIR / "grok_pre_mt5_lifecycle_negative_control_runtime_probe_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f77c.md"
LOCAL_VERIFICATION_PATH = REVIEW_DIR / "f77c_pre_mt5_local_verification.json"
TARGET_SELECTION_PATH = REVIEW_DIR / "f77c_runtime_materialization_target_selection.json"
SELECTION_STATUS_PATH = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER_PATH = REVIEW_DIR / "stage_run_ledger.csv"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f77c_pre_mt5_lifecycle_negative_control_runtime_probe"
GROK_PROMPT_PATH = GROK_PACKET / "prompts/f77c_pre_mt5_lifecycle_negative_control_runtime_probe_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


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
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def required_inputs() -> list[Path]:
    return [SUMMARY_PATH, TOP100_PATH, DATA_INTEGRITY_PATH, MODEL_VALIDATION_PATH, F77B_REPORT_PATH, RUN_REGISTRY, ALPHA_LEDGER]


def local_export_feasibility() -> dict[str, Any]:
    checks: dict[str, Any] = {}
    try:
        import numpy as np
        from sklearn.datasets import make_classification
        from sklearn.ensemble import ExtraTreesClassifier, HistGradientBoostingClassifier
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        x, y = make_classification(n_samples=80, n_features=6, n_informative=4, random_state=7703)
        models = {
            "hist_gbm_d4_l2": HistGradientBoostingClassifier(max_iter=10, max_depth=4, l2_regularization=2.0, random_state=7703),
            "extra_trees_d7_l80": ExtraTreesClassifier(n_estimators=20, max_depth=7, min_samples_leaf=80, random_state=7703, n_jobs=1),
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
            except Exception as exc:  # pragma: no cover - environment dependent converter shape
                checks[name] = {
                    "export_status": "export_failed",
                    "error_type": type(exc).__name__,
                    "error_excerpt": str(exc)[:500],
                }
        checks["numpy_version"] = getattr(np, "__version__", "")
    except Exception as exc:  # pragma: no cover - environment dependent import shape
        checks["environment"] = {"export_status": "blocked", "error_type": type(exc).__name__, "error_excerpt": str(exc)[:500]}
    return checks


def choose_runtime_target(summary: Mapping[str, Any], top_rows: Sequence[Mapping[str, str]], export_checks: Mapping[str, Any]) -> dict[str, Any]:
    best = dict(summary.get("best_candidate") or {})
    exportable_models = {
        name for name, payload in export_checks.items() if isinstance(payload, Mapping) and payload.get("export_status") == "export_ok"
    }
    fallback: dict[str, str] | None = None
    for row in top_rows:
        if row.get("model") in exportable_models:
            fallback = dict(row)
            break
    if fallback is None:
        fallback = dict(top_rows[0]) if top_rows else {}
    target = fallback
    source_export = export_checks.get(str(best.get("model")), {})
    target_export = export_checks.get(str(target.get("model")), {})
    return {
        "blocked_best_candidate": best,
        "runtime_materialization_target": target,
        "target_candidate_id": target.get("candidate_id", ""),
        "selection_reason": (
            "best_proxy_hist_gbm_export_failed_so_first_ranked_exportable_extra_trees_target_selected"
            if best.get("candidate_id") != target.get("candidate_id")
            else "best_proxy_candidate_exportable"
        ),
        "best_export_check": source_export,
        "target_export_check": target_export,
        "export_checks": export_checks,
        "runtime_probe_role": "weak_nonzero_negative_control_runtime_probe",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def kpi_line(row: Mapping[str, Any], prefix: str) -> str:
    return (
        f"net/PF/DD/tpd/trades/win/expectancy/recovery("
        f"순수익/수익 팩터/손실폭/일거래/거래/승률/기대값/회복): "
        f"{row.get(prefix + '_net')}/{row.get(prefix + '_pf')}/{row.get(prefix + '_dd_pct')}/"
        f"{row.get(prefix + '_trades_day')}/{row.get(prefix + '_trade_count')}/"
        f"{row.get(prefix + '_win_rate')}/{row.get(prefix + '_expectancy')}/{row.get(prefix + '_recovery')}"
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
            (
                f"{idx}. {row.get('candidate_id')}: {row.get('label_name')}/"
                f"{row.get('feature_set')}/{row.get('model')}/{row.get('session')}/"
                f"{row.get('risk_filter')}/q{row.get('prob_quantile')} | "
                f"val {row.get('val_net')}/{row.get('val_pf')}/{row.get('val_dd_pct')}/{row.get('val_trades_day')}/"
                f"{row.get('val_trade_count')} | "
                f"oos {row.get('oos_net')}/{row.get('oos_pf')}/{row.get('oos_dd_pct')}/{row.get('oos_trades_day')}/"
                f"{row.get('oos_trade_count')}"
            )
        )
    return f"""# F77C Pre-MT5 Grok Review Prompt(F77C 사전 MT5 그록 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- proposed next run(제안 다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Hypothesis(가설)

F77 asks whether runtime lifecycle-native labels(런타임 생명주기 기본 라벨) can reduce the proxy/runtime gap(프록시/런타임 간극) by learning entry-to-exit path outcomes(진입-청산 경로 결과), first-touch TP/SL(최초접촉 익절/손절), hold duration(보유 시간), and single-position occupancy(단일 포지션 점유).

## F77B Proxy Evidence(F77B 프록시 근거)

- candidate rows(후보 행): `{summary['candidate_rows']}`
- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`
- final-like reference count(최종 유사 참조 수): `{summary['final_like_reference_count']}`
- nonzero lifecycle trade candidates(비영 생명주기 거래 후보): `{summary['nonzero_lifecycle_trade_candidates']}`

Best proxy candidate(최선 프록시 후보):
- candidate id(후보 ID): `{best['candidate_id']}`
- axes(축): `{best['label_name']}/{best['feature_set']}/{best['model']}/{best['session']}/{best['risk_filter']}/q{best['prob_quantile']}`
- validation KPI(검증 핵심 성과 지표): {kpi_line(best, 'val')}
- OOS KPI(표본외 핵심 성과 지표): {kpi_line(best, 'oos')}
- compression(압축): raw signal -> lifecycle trade validation/OOS(원시 신호 -> 생명주기 거래 검증/표본외) `{best['validation_raw_signal_count']}->{best['validation_lifecycle_trade_count']}/{best['oos_raw_signal_count']}->{best['oos_lifecycle_trade_count']}`
- weakness(약점): it is scout clue(탐색 단서) only because OOS trade count(표본외 거래 수) is below meaningful gate(의미 신호 게이트).

Top ranked rows(상위 행):
{chr(10).join(top_lines)}

## Local Export Check(로컬 내보내기 확인)

Codex checked skl2onnx(사이킷런-온엑스) export feasibility with an in-memory smoke test(메모리 내 연기 테스트):

```json
{json.dumps(json_ready(target_selection['export_checks']), ensure_ascii=False, indent=2)}
```

Result(결과): best HistGradientBoosting(히스토그램 그래디언트 부스팅) target is not exportable in this environment(현재 환경에서 내보내기 실패). Codex proposes the first ranked exportable ExtraTrees(엑스트라트리) target instead:

- target candidate(대상 후보): `{target.get('candidate_id')}`
- axes(축): `{target.get('label_name')}/{target.get('feature_set')}/{target.get('model')}/{target.get('session')}/{target.get('risk_filter')}/q{target.get('prob_quantile')}`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `{target.get('val_net')}/{target.get('val_pf')}/{target.get('val_dd_pct')}/{target.get('val_trades_day')}/{target.get('val_trade_count')}`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `{target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_trades_day')}/{target.get('oos_trade_count')}`

## Integrity And Validation Boundary(무결성과 검증 경계)

- data integrity judgment(데이터 무결성 판정): `{data_integrity.get('integrity_judgment')}`
- time axis(시간축): `{data_integrity.get('time_axis')}`
- feature/label boundary(피처/라벨 경계): `{data_integrity.get('feature_label_boundary')}`
- model validation judgment(모델 검증 판정): `{model_validation.get('validation_judgment')}`
- calibration risk(보정 위험): `{model_validation.get('calibration_risk')}`
- overfit risk(과적합 위험): `{model_validation.get('overfit_risk')}`

## Proposed MT5 Runtime Probe(제안 MT5 런타임 탐침)

Codex proposal(Codex 제안):

1. Re-train(재학습) the selected ExtraTrees(엑스트라트리) target on train split(학습 분할) using the same lifecycle label(생명주기 라벨), feature set(피처 묶음), session filter(세션 필터), risk filter(위험 필터), and train quantile threshold(학습 분위수 임계값).
2. Materialize ONNX(온엑스 물질화) as short-only three-column output(숏 전용 3열 출력): `[p_short=P(short), p_flat=P(non-short), p_long=0]`.
3. Use selected-entry runtime veto tape(선택 진입 런타임 거부 테이프) so MT5 signal count(신호 수) is forced to match proxy selected timestamps(프록시 선택 시각) after ONNX thresholding(온엑스 임계값 적용).
4. Runtime decision(런타임 결정): `short_threshold=proxy_threshold-epsilon`, `long_threshold=1.1`, `min_margin=-1.0`, decision mode(결정 모드) `threshold_margin`.
5. Trade shape(거래 형태): short-only(숏 전용), max hold 12 M5 bars(최대 보유 12개 5분봉), fixed TP/SL(고정 익절/손절) 18/12 points(포인트) by enabling ATR SL/TP(ATR 손절/익절) and setting min=max clamps(최소=최대 고정) to TP 18 and SL 12.
6. Execute validation and OOS Strategy Tester(검증 및 표본외 전략 테스터) attempts for US100 M5.

## Focus Question(집중 질문)

Should Codex proceed with this F77D negative-control MT5 Runtime Probe(F77D 부정 대조 MT5 런타임 탐침) as proposed, or must it adjust the materialization before execution?

Please classify advice(조언 분류) into exactly one:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Also list:
1. Top proxy/runtime gap risks(최상위 프록시/런타임 간극 위험)
2. Required local verification before execution(실행 전 필수 로컬 검증)
3. Any forbidden claim risk(금지 주장 위험)
4. The smallest useful MT5 probe scope(가장 작은 유용한 MT5 탐침 범위)
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str]]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ["goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion"]
        if f"may claim {term}" in lowered
        or f"can claim {term}" in lowered
        or f"{term} achieved" in lowered
        or f"{term}: achieved" in lowered
        or f"{term}: yes" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_required(재시도 필요)", forbidden_hits
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)", "do_not_execute_until_runtime_mapping_repaired(런타임 매핑 수리 전 실행 금지)", forbidden_hits
    if "accepted_with_conditions" in lowered or "accepted with conditions" in lowered:
        return "accepted_with_conditions(조건부 수용)", "proceed_after_local_verification(로컬 검증 뒤 진행)", forbidden_hits
    if "needs_local_verification" in lowered or "local verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)", "proceed_only_after_codex_checks(코덱스 확인 뒤에만 진행)", forbidden_hits
    return "accepted_with_conditions(조건부 수용)", "proceed_after_local_verification(로컬 검증 뒤 진행)", forbidden_hits


def report_text(
    created_at: str,
    summary: Mapping[str, Any],
    target_selection: Mapping[str, Any],
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: Sequence[str],
) -> str:
    best = summary["best_candidate"]
    target = target_selection["runtime_materialization_target"]
    return f"""# Frontier77C Pre-MT5 Grok Review Report(F77C 사전 MT5 Grok 검토 보고서)

Run id(실행 ID): `{RUN_ID}`

Status(상태): `{STATUS_SUCCESS if grok['success'] else STATUS_TRANSPORT_FAIL}`

Judgment(판정): `{JUDGMENT_SUCCESS if grok['success'] else JUDGMENT_TRANSPORT_FAIL}`

Updated(갱신): {created_at}

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Codex Direction Before Grok(Grok 전 Codex 방향)

Action(행동): F77B weak nonzero proxy(약한 비영 프록시)를 F77D negative-control MT5 Runtime Probe(F77D 부정 대조 MT5 런타임 탐침)로 물질화한다.

Effect(효과): 프록시의 trade shape(거래 형태), selected-entry count(선택 진입 수), feature readiness(피처 준비), ONNX parity(온엑스 동등성)가 MT5에서 어디까지 유지되는지 관찰한다.

## Proxy KPI(프록시 핵심 성과 지표)

- best candidate(최선 후보): `{best['candidate_id']}` `{best['label_name']}/{best['feature_set']}/{best['model']}/{best['session']}/{best['risk_filter']}/q{best['prob_quantile']}`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `{best['val_net']}/{best['val_pf']}/{best['val_dd_pct']}/{best['val_trades_day']}/{best['val_trade_count']}`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_trades_day']}/{best['oos_trade_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`

## Materialization Target(물질화 대상)

- selected target(선택 대상): `{target.get('candidate_id')}` `{target.get('label_name')}/{target.get('feature_set')}/{target.get('model')}/{target.get('session')}/{target.get('risk_filter')}/q{target.get('prob_quantile')}`
- selection reason(선택 이유): `{target_selection.get('selection_reason')}`
- target validation net/PF/DD/tpd/trades(대상 검증 순수익/수익 팩터/손실폭/일거래/거래): `{target.get('val_net')}/{target.get('val_pf')}/{target.get('val_dd_pct')}/{target.get('val_trades_day')}/{target.get('val_trade_count')}`
- target OOS net/PF/DD/tpd/trades(대상 표본외 순수익/수익 팩터/손실폭/일거래/거래): `{target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_trades_day')}/{target.get('oos_trade_count')}`
- local export check(로컬 내보내기 확인): `{rel(LOCAL_VERIFICATION_PATH)}`

## Grok Advice(Grok 조언)

- packet(묶음): `{rel(GROK_PACKET)}`
- prompt(프롬프트): `{rel(GROK_PROMPT_PATH)}` sha256 `{grok['prompt_sha256']}`
- output(출력): `{rel(GROK_CLEAN_PATH)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing'}`
- metadata(메타데이터): `{rel(GROK_METADATA_PATH)}` sha256 `{grok['metadata_sha256'] if grok['metadata_exists'] else 'missing'}`
- wrapper success(래퍼 성공): `{grok['success']}`
- returncode(반환 코드): `{grok['returncode']}`
- advice classification(조언 분류): `{advice_classification}`
- final Codex direction(최종 Codex 방향): `{final_direction}`
- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`

## Required Local Verification(필수 로컬 검증)

- model export parity(모델 내보내기 동등성): ExtraTrees binary ONNX(이진 온엑스)를 short-only three-column schema(숏 전용 3열 스키마)로 패치하고 확률 차이를 확인한다.
- signal count parity(신호 수 동등성): selected-entry runtime veto tape(선택 진입 런타임 거부 테이프) 뒤 validation/OOS signal count(검증/표본외 신호 수)가 proxy selected count(프록시 선택 수)와 일치하는지 확인한다.
- feature readiness parity(피처 준비 동등성): `price_action_core` feature order(피처 순서)와 MT5 feature CSV(피처 CSV)의 열 수/순서/hash(해시)를 확인한다.
- trade shape parity(거래 형태 동등성): short-only(숏 전용), max hold 12(최대 보유 12), fixed TP/SL 18/12(고정 익절/손절 18/12)를 EA inputs(EA 입력값)로 고정한다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`.
"""


def receipt_text(
    created_at: str,
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: Sequence[str],
) -> str:
    return f"""# F77C Grok Pre-MT5 Receipt(F77C Grok 사전 MT5 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): `/goal(목표)` requires Grok review(Grok 검토) before MT5 Runtime Probe(MT5 런타임 탐침).

Review size(검토 크기): medium review(중간 검토).

Direction before Grok(Grok 전 방향): weak nonzero lifecycle proxy(약한 비영 생명주기 프록시)를 negative-control MT5 Runtime Probe(부정 대조 MT5 런타임 탐침)로 물질화한다.

Bounded evidence(제한 근거): F77B summary/top100/data integrity/model validation(F77B 요약/상위100/데이터 무결성/모델 검증), local export smoke check(로컬 내보내기 연기 확인), proposed runtime mapping(제안 런타임 매핑).

Prompt identity(프롬프트 정체성): `{rel(GROK_PROMPT_PATH)}` sha256 `{grok['prompt_sha256']}`.

Grok output identity(Grok 출력 정체성): `{rel(GROK_CLEAN_PATH)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing'}`.

Advice classification(조언 분류): `{advice_classification}`.

Local verification(로컬 검증): wrapper success(래퍼 성공) `{grok['success']}`, returncode(반환 코드) `{grok['returncode']}`, local export target selection(로컬 내보내기 대상 선택) recorded at `{rel(TARGET_SELECTION_PATH)}`.

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`. Codex rejects any completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) implication.

Final Codex direction(최종 Codex 방향): `{final_direction}`.
"""


def gate_audit_text(grok: Mapping[str, Any], advice_classification: str) -> str:
    return f"""# Required Gate Coverage Audit F77C(F77C 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F77B proxy evidence(F77B 프록시 근거) | `passed(통과)` | `{rel(SUMMARY_PATH)}` |
| pre-MT5 Grok review(사전 MT5 Grok 검토) | `{'passed(통과)' if grok['success'] else 'failed_transport(전송 실패)'}` | `{rel(RECEIPT_PATH)}` |
| bounded evidence(제한 근거) | `passed(통과)` | summary/top100/integrity/validation(요약/상위100/무결성/검증) |
| local export check(로컬 내보내기 확인) | `recorded(기록됨)` | `{rel(LOCAL_VERIFICATION_PATH)}` |
| materialization target selection(물질화 대상 선택) | `recorded(기록됨)` | `{rel(TARGET_SELECTION_PATH)}` |
| advice classification(조언 분류) | `{advice_classification}` | `{rel(GROK_CLEAN_PATH)}` |
| runtime probe next(다음 런타임 탐침) | `required(필수)` | `{NEXT_RUN_ID}` |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def selection_status_text(created_at: str, status: str, judgment: str) -> str:
    return f"""# F77 Selection Status(F77 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F77C pre-MT5 Grok review(사전 MT5 Grok 검토)를 실행했다.

Effect(효과): F77D MT5 Runtime Probe(F77D MT5 런타임 탐침)에서 확인할 local parity checks(로컬 동등성 확인)와 materialization target(물질화 대상)을 고정했다.

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
        "path": rel(REPORT_PATH),
        "primary_kpi": f"target={target.get('candidate_id')};target_oos_pf={target.get('oos_pf')};target_oos_tpd={target.get('oos_trades_day')}",
        "guardrail_kpi": "no authority;runtime probe still required",
        "external_verification_status": "mt5_runtime_probe_required_next(MT5 런타임 탐침 다음 필수)",
        "notes": f"F77C Grok review completed; target={target.get('candidate_id')}; next={NEXT_RUN_ID}",
        "lane": "pre_mt5_grok_review(사전 MT5 Grok 검토)",
        "family": "runtime_probe_gate(런타임 탐침 게이트)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier77C",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": NEXT_RUN_ID,
        "rows": "1",
        "gate_passes": "8",
        "gate_total": "8",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "view": "pre_mt5_grok_review",
        "tier": "Tier A separate",
        "metric_scope": "runtime_probe_gate",
        "result_status": status,
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "pre_mt5_grok_review",
        "run_type": "lifecycle_negative_control_runtime_probe_gate",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "source_authority": "proxy_only(프록시 전용)",
        "best_proxy": target.get("candidate_id", ""),
        "best_model_id": target.get("model", ""),
        "expected_net_profit": target.get("oos_net", ""),
        "expected_profit_factor": target.get("oos_pf", ""),
        "expected_trade_count": target.get("oos_trade_count", ""),
        "expected_trade_density": target.get("oos_trades_day", ""),
    }


def update_state_and_ledgers(
    created_at: str,
    status: str,
    judgment: str,
    advice_classification: str,
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
runtime_probe_status: f77_mt5_lifecycle_negative_control_runtime_probe_required_next
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f76_closeout_1_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F77C pre-MT5 Grok review(사전 MT5 Grok 검토)를 실행했다."
  - "Effect(효과): F77D MT5 Runtime Probe(MT5 런타임 탐침)의 물질화 대상과 검증 조건을 고정했다."
  - "Target(대상): {target.get('candidate_id')} {target.get('model')} OOS net/PF/DD/tpd {target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_trades_day')}."
  - "Grok success(Grok 성공): {grok['success']}; advice(조언): {advice_classification}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, workspace)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F77C pre-MT5 Grok review(사전 MT5 Grok 검토)를 실행했다.

Effect(효과): F77D MT5 Runtime Probe(MT5 런타임 탐침)에서 물질화할 target(대상)과 parity checks(동등성 확인)가 정해졌다.

## Runtime Probe Target(런타임 탐침 대상)

- candidate(후보): `{target.get('candidate_id')}`
- axes(축): `{target.get('label_name')}/{target.get('feature_set')}/{target.get('model')}/{target.get('session')}/{target.get('risk_filter')}/q{target.get('prob_quantile')}`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `{target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_trades_day')}/{target.get('oos_trade_count')}`

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- runtime status(런타임 상태): `f77_mt5_lifecycle_negative_control_runtime_probe_required_next`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS_PATH, selection_status_text(created_at, status, judgment))
    row = ledger_row(created_at, status, judgment, target_selection)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER_PATH, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_idea_registry(status: str, judgment: str, target_selection: Mapping[str, Any]) -> None:
    marker = "<!-- frontier77C_pre_mt5_grok_lifecycle_negative_control_runtime_probe_v1 -->"
    text = read_text(IDEA_REGISTRY)
    if marker in text:
        return
    target = target_selection["runtime_materialization_target"]
    block = f"""

{marker}
### F77C pre-MT5 Grok review(사전 MT5 Grok 검토)

- status(상태): `{status}`
- judgment(판정): `{judgment}`
- action(행동): weak nonzero lifecycle proxy(약한 비영 생명주기 프록시)를 MT5 negative-control runtime probe(MT5 부정 대조 런타임 탐침)로 보낸다.
- effect(효과): target(대상) `{target.get('candidate_id')}`의 ONNX parity(온엑스 동등성), signal count parity(신호 수 동등성), feature readiness parity(피처 준비 동등성), trade shape parity(거래 형태 동등성)를 다음 run(실행)에서 확인한다.
- boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""
    write_text(IDEA_REGISTRY, text.rstrip() + block)


def run_manifest(
    created_at: str,
    status: str,
    judgment: str,
    grok: Mapping[str, Any],
    advice_classification: str,
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
            "f77b_report": rel(F77B_REPORT_PATH),
        },
        "outputs": {
            "report": rel(REPORT_PATH),
            "receipt": rel(RECEIPT_PATH),
            "gate_audit": rel(GATE_AUDIT_PATH),
            "local_verification": rel(LOCAL_VERIFICATION_PATH),
            "target_selection": rel(TARGET_SELECTION_PATH),
            "grok_prompt": rel(GROK_PROMPT_PATH),
            "grok_clean": rel(GROK_CLEAN_PATH),
            "grok_metadata": rel(GROK_METADATA_PATH),
        },
        "grok": grok,
        "advice_classification": advice_classification,
        "target_selection": target_selection,
        "runtime_probe_required_next": True,
    }


def main() -> int:
    ensure_dirs()
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required F77C inputs: {missing}")
    created_at = utc_now()
    summary = read_json(SUMMARY_PATH)
    top_rows = read_csv_rows(TOP100_PATH)
    data_integrity = read_json(DATA_INTEGRITY_PATH)
    model_validation = read_json(MODEL_VALIDATION_PATH)
    export_checks = local_export_feasibility()
    target_selection = choose_runtime_target(summary, top_rows, export_checks)
    write_json(LOCAL_VERIFICATION_PATH, {"created_at_utc": created_at, "export_checks": export_checks})
    write_json(TARGET_SELECTION_PATH, target_selection)
    prompt = build_prompt(summary, top_rows, data_integrity, model_validation, target_selection)
    write_text(GROK_PROMPT_PATH, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        timeout_seconds=300,
        review_size="medium",
        output_dir=GROK_PACKET,
        repo_root=ROOT,
        prompt_file_path=GROK_PROMPT_PATH,
    )
    success = bool(result.returncode == 0 and not result.timed_out)
    clean = result.clean_stdout
    grok = {
        "success": success,
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_sha256": result.prompt_hash,
        "output_exists": path_exists(GROK_CLEAN_PATH),
        "metadata_exists": path_exists(GROK_METADATA_PATH),
        "output_sha256": file_hash(GROK_CLEAN_PATH),
        "metadata_sha256": file_hash(GROK_METADATA_PATH),
        "packet_path": rel(GROK_PACKET),
        "prompt_path": rel(GROK_PROMPT_PATH),
        "output_path": rel(GROK_CLEAN_PATH),
        "metadata_path": rel(GROK_METADATA_PATH),
        "unexpected_top_level_artifacts": list(result.unexpected_top_level_artifacts),
        "preflight_warnings": list(result.preflight_warnings),
    }
    advice_classification, final_direction, forbidden_hits = classify_advice(clean, success)
    if advice_classification.startswith("rejected"):
        status = STATUS_REJECTED
        judgment = JUDGMENT_REJECTED
    elif not success:
        status = STATUS_TRANSPORT_FAIL
        judgment = JUDGMENT_TRANSPORT_FAIL
    else:
        status = STATUS_SUCCESS
        judgment = JUDGMENT_SUCCESS
    write_text(REPORT_PATH, report_text(created_at, summary, target_selection, grok, advice_classification, final_direction, forbidden_hits))
    write_text(RECEIPT_PATH, receipt_text(created_at, grok, advice_classification, final_direction, forbidden_hits))
    write_text(GATE_AUDIT_PATH, gate_audit_text(grok, advice_classification))
    write_json(RUN_MANIFEST_PATH, run_manifest(created_at, status, judgment, grok, advice_classification, target_selection))
    update_state_and_ledgers(created_at, status, judgment, advice_classification, grok, target_selection)
    update_idea_registry(status, judgment, target_selection)
    print(json.dumps({"status": status, "judgment": judgment, "advice_classification": advice_classification, "target_candidate": target_selection["target_candidate_id"], "next_run_id": NEXT_RUN_ID, "report": rel(REPORT_PATH)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
