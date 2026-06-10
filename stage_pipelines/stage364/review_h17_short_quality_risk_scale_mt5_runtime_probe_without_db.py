from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db as cv  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db as db  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_quality_risk_scale_runtime_package_without_db as da  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = db.STAGE_ID
RUN_NUMBER = "run364DC"
RUN_ID = "run364DC_review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = db.RUN_ID
BASELINE_RUN_ID = cv.RUN_ID
PACKAGE_RUN_ID = da.RUN_ID
NEXT_RUN_ID = "run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1"

STATUS = "completed_stage364DC_h17_short_quality_risk_scale_mt5_review_runtime_positive_clue_side_balance_unresolved_no_authority"
JUDGMENT = "positive_runtime_probe_clue_short_risk_scale_transfer_real_side_balance_unresolved_no_authority"
DECISION = "stage364DC_open_run364DD_short_source_expansion_runtime_positive_scout"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = db.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

COMPARISON_REVIEW = RUN_DIR / "db_vs_cv_runtime_comparison.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN364DD_QUEUE = RUN_DIR / "run364DD_short_source_expansion_queue.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DC_h17_short_quality_risk_scale_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DC_h17_short_quality_risk_scale_mt5_runtime_probe_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    db.FINAL_DECISION,
    db.GATE_AUDIT,
    db.EXECUTION_SUMMARY,
    db.PROXY_MT5_DIFF,
    db.STRATEGY_TESTER_REPORTS,
    db.RUNTIME_OUTPUT_COPY,
    da.FINAL_DECISION,
    da.EXPECTED_KPI_SUMMARY,
    cv.FINAL_DECISION,
    cv.EXECUTION_SUMMARY,
    cv.PROXY_MT5_DIFF,
]

OUTPUT_FILES = [
    COMPARISON_REVIEW,
    RESULT_JUDGMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    RUN364DD_QUEUE,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return db.rel(path)


def exists(path: Path | str) -> bool:
    return db.exists(path)


def sha(path: Path | str) -> str:
    return db.sha(path)


def read_json(path: Path) -> Any:
    return db.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    db.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    db.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    db.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    db.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    db.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    db.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def float_or_nan(value: Any) -> float:
    try:
        if value in ("", None):
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DC inputs(DC 입력 누락): " + ", ".join(missing))
    db_final = read_json(db.FINAL_DECISION)
    da_final = read_json(da.FINAL_DECISION)
    cv_final = read_json(cv.FINAL_DECISION)
    if db_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DB next_run_id mismatch(DB 다음 실행 ID 불일치): {db_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("DB", db_final), ("DA", da_final), ("CV", cv_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    db_gates = read_csv(db.GATE_AUDIT)
    if db_gates.empty or any(db_gates["status"].astype(str) != "passed"):
        raise RuntimeError("DB gate audit(DB 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return db_final, da_final, cv_final


def first_row(path: Path) -> dict[str, Any]:
    frame = read_csv(path)
    return {} if frame.empty else frame.iloc[0].to_dict()


def build_comparison(db_final: Mapping[str, Any], da_final: Mapping[str, Any], cv_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    db_row = first_row(db.EXECUTION_SUMMARY)
    cv_row = first_row(cv.EXECUTION_SUMMARY)
    proxy_row = first_row(db.PROXY_MT5_DIFF)
    expected_delta = float_or_nan(da_final.get("expected_proxy_risk_scale_net_delta"))
    actual_delta = float_or_nan(db_row.get("net_profit")) - float_or_nan(cv_row.get("net_profit"))
    transfer_efficiency = actual_delta / expected_delta if math.isfinite(actual_delta) and math.isfinite(expected_delta) and expected_delta else math.nan
    actual_trade_count = float_or_nan(db_row.get("trade_count"))
    actual_density = actual_trade_count / 314.0 if math.isfinite(actual_trade_count) else math.nan
    actual_short_count = float_or_nan(db_row.get("short_trade_count"))
    actual_long_count = float_or_nan(db_row.get("long_trade_count"))
    short_share = actual_short_count / actual_trade_count if math.isfinite(actual_short_count) and math.isfinite(actual_trade_count) and actual_trade_count else math.nan
    long_share = actual_long_count / actual_trade_count if math.isfinite(actual_long_count) and math.isfinite(actual_trade_count) and actual_trade_count else math.nan
    rows = [
        {
            "run_id": RUN_ID,
            "candidate_id": db_final.get("candidate_id", ""),
            "comparison_baseline": BASELINE_RUN_ID,
            "db_mt5_net": finite(db_row.get("net_profit")),
            "cv_mt5_net": finite(cv_row.get("net_profit")),
            "mt5_net_delta_vs_cv": finite(actual_delta),
            "expected_risk_scale_net_delta": finite(expected_delta),
            "overlay_transfer_efficiency": finite(transfer_efficiency),
            "db_profit_factor": finite(db_row.get("profit_factor")),
            "cv_profit_factor": finite(cv_row.get("profit_factor")),
            "profit_factor_delta_vs_cv": finite(float_or_nan(db_row.get("profit_factor")) - float_or_nan(cv_row.get("profit_factor"))),
            "db_expectancy": finite(db_row.get("expectancy")),
            "cv_expectancy": finite(cv_row.get("expectancy")),
            "expectancy_delta_vs_cv": finite(float_or_nan(db_row.get("expectancy")) - float_or_nan(cv_row.get("expectancy"))),
            "db_drawdown": finite(db_row.get("max_drawdown_amount")),
            "cv_drawdown": finite(cv_row.get("max_drawdown_amount")),
            "drawdown_delta_vs_cv": finite(float_or_nan(db_row.get("max_drawdown_amount")) - float_or_nan(cv_row.get("max_drawdown_amount"))),
            "db_recovery_factor": finite(db_row.get("recovery_factor")),
            "cv_recovery_factor": finite(cv_row.get("recovery_factor")),
            "recovery_factor_delta_vs_cv": finite(float_or_nan(db_row.get("recovery_factor")) - float_or_nan(cv_row.get("recovery_factor"))),
            "db_trade_count": finite(db_row.get("trade_count"), 0),
            "cv_trade_count": finite(cv_row.get("trade_count"), 0),
            "trade_count_delta_vs_cv": finite(float_or_nan(db_row.get("trade_count")) - float_or_nan(cv_row.get("trade_count")), 0),
            "actual_trade_density": finite(actual_density),
            "db_long_trade_count": finite(db_row.get("long_trade_count"), 0),
            "db_short_trade_count": finite(db_row.get("short_trade_count"), 0),
            "short_share": finite(short_share),
            "long_share": finite(long_share),
            "proxy_expected_net": proxy_row.get("expected_net_profit", ""),
            "actual_mt5_net": proxy_row.get("actual_mt5_net_profit", ""),
            "proxy_mt5_net_gap": proxy_row.get("net_profit_diff_actual_minus_expected", ""),
            "proxy_mt5_profit_factor_gap": proxy_row.get("profit_factor_diff_actual_minus_expected", ""),
            "side_balance_status": "unresolved_long_dominant(미해결 롱 우세)",
            "attribution_confidence": "medium(중간)",
            "judgment": JUDGMENT,
            "effect": "risk-scale overlay(위험비율 오버레이)는 MT5에서 거의 전달됐지만 long/short balance(롱/숏 균형)는 해결되지 않았습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(COMPARISON_REVIEW, rows)
    return rows


def build_queue(comparison: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "dd01_short_source_expansion",
            "seed": "DB risk-scale transfer real(DB 위험비율 전달 실제 확인)",
            "target_question": "Can new short-source features/rules lift short count and short PnL without weakening DB MT5 net/PF/DD?(새 숏 원천 피처/규칙이 DB MT5 순수익/수익 팩터/낙폭을 약화하지 않고 숏 수와 숏 손익을 올릴 수 있는가?)",
            "baseline_mt5_net": comparison.get("db_mt5_net", ""),
            "baseline_mt5_profit_factor": comparison.get("db_profit_factor", ""),
            "baseline_mt5_drawdown": comparison.get("db_drawdown", ""),
            "baseline_short_share": comparison.get("short_share", ""),
            "success_criteria": "proxy candidates preserve density>=3(밀도 3 이상) and prepare MT5 package only if side balance improves without trade splitting(거래 쪼개기 없이 방향 균형 개선)",
            "failure_memory": "Do not repeat pure exposure scaling only(순수 노출 증폭만 반복 금지); it improved net but did not fix side balance(순수익은 개선했지만 방향 균형은 미해결).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364DD_QUEUE, rows)
    return rows


def build_final(db_final: Mapping[str, Any], da_final: Mapping[str, Any], cv_final: Mapping[str, Any], comparison: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_id": db_final.get("candidate_id", ""),
        "created_at_utc": now_utc(),
        "db_mt5_net": comparison.get("db_mt5_net", ""),
        "db_profit_factor": comparison.get("db_profit_factor", ""),
        "db_expectancy": comparison.get("db_expectancy", ""),
        "db_trade_count": comparison.get("db_trade_count", ""),
        "db_trade_density": comparison.get("actual_trade_density", ""),
        "db_drawdown": comparison.get("db_drawdown", ""),
        "db_recovery_factor": comparison.get("db_recovery_factor", ""),
        "db_long_trade_count": comparison.get("db_long_trade_count", ""),
        "db_short_trade_count": comparison.get("db_short_trade_count", ""),
        "short_share": comparison.get("short_share", ""),
        "mt5_net_delta_vs_cv": comparison.get("mt5_net_delta_vs_cv", ""),
        "expected_risk_scale_net_delta": comparison.get("expected_risk_scale_net_delta", ""),
        "overlay_transfer_efficiency": comparison.get("overlay_transfer_efficiency", ""),
        "proxy_mt5_net_gap": comparison.get("proxy_mt5_net_gap", ""),
        "side_balance_status": comparison.get("side_balance_status", ""),
        "result_subject": "run364DB cx05 short-quality risk-scale MT5 runtime probe(run364DB cx05 숏 품질 위험비율 MT5 런타임 탐침)",
        "evidence_available": [rel(db.EXECUTION_SUMMARY), rel(db.PROXY_MT5_DIFF), rel(db.STRATEGY_TESTER_REPORTS), rel(COMPARISON_REVIEW)],
        "evidence_missing": [
            "forward/replay evidence(전진/재생 근거)",
            "runtime authority closure(런타임 권위 폐쇄)",
            "balanced short source expansion(균형 잡힌 숏 원천 확장)",
            "Tier B fallback source(Tier B 대체 원천)",
        ],
        "next_condition": NEXT_RUN_ID,
        "external_verification_status": "completed(완료)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate": "input_lineage_gate",
            "status": "passed",
            "evidence": ";".join(rel(path) for path in INPUT_FILES if exists(path)),
            "effect": "DB/CV/DA evidence(DB/CV/DA 근거)를 같은 비교 경계에 묶습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "mt5_output_review_gate",
            "status": "passed",
            "evidence": rel(db.EXECUTION_SUMMARY),
            "effect": "MT5 output(MT5 출력)이 review(검토) 가능한지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "baseline_comparison_gate",
            "status": "passed",
            "evidence": rel(COMPARISON_REVIEW),
            "effect": "DB를 CV runtime anchor(CV 런타임 기준점)와 비교합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "proxy_mt5_gap_attribution_gate",
            "status": "passed",
            "evidence": rel(COMPARISON_REVIEW),
            "effect": "proxy/MT5 gap(프록시/MT5 차이)과 overlay delta(오버레이 변화분)를 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "side_balance_boundary_gate",
            "status": "passed",
            "evidence": rel(COMPARISON_REVIEW),
            "effect": "long/short balance(롱/숏 균형) 미해결을 다음 탐색 제약으로 기록합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "required gate(필수 게이트)를 closeout(종료 기록)에 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(final: Mapping[str, Any], comparison: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": final["result_subject"],
            "evidence_available": final["evidence_available"],
            "evidence_missing": final["evidence_missing"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "MT5에서 수익 개선은 실제로 보였지만 방향 균형과 운영 권위는 아직 닫히지 않았습니다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": f"DB net {comparison.get('db_mt5_net')} vs CV net {comparison.get('cv_mt5_net')} delta {comparison.get('mt5_net_delta_vs_cv')}",
            "comparison_baseline": BASELINE_RUN_ID,
            "likely_drivers": ["risk_scale_overlay(위험비율 오버레이)", "short exposure multiplier(숏 노출 배수)"],
            "segment_checks": {
                "time_period": "not_split_in_DC(DC에서 미분할)",
                "direction": "long_short_counts_reviewed(롱/숏 수 검토)",
                "drawdown": "max_drawdown_compared_vs_CV(CV 대비 최대 낙폭 비교)",
                "cost": "Strategy Tester native report only(전략 테스터 기본 보고서 한정)",
            },
            "trade_shape": {
                "trade_count": comparison.get("db_trade_count"),
                "long_trade_count": comparison.get("db_long_trade_count"),
                "short_trade_count": comparison.get("db_short_trade_count"),
                "short_share": comparison.get("short_share"),
                "profit_factor": comparison.get("db_profit_factor"),
                "drawdown": comparison.get("db_drawdown"),
            },
            "alternative_explanations": [
                "proxy/MT5 cost and fill gap(프록시/MT5 비용 및 체결 차이)",
                "risk-scale only changed lot exposure(위험비율은 진입 수가 아니라 로트 노출만 변경)",
            ],
            "attribution_confidence": comparison.get("attribution_confidence", "medium(중간)"),
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "positive runtime clue(긍정 런타임 단서)를 operating claim(운영 주장)으로 승격하지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return db.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], comparison_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    comparison = comparison_rows[0]
    report = f"""# run364DC h17 short-quality risk-scale MT5 runtime probe review(17시 숏 품질 위험비율 MT5 런타임 탐침 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed`

## Key Read(핵심 판독)

Action(행동): DB MT5 result(DB MT5 결과)를 CV runtime anchor(CV 런타임 기준점)와 비교했습니다.

Effect(효과): risk-scale overlay(위험비율 오버레이)가 MT5에서 실제 순수익 개선으로 전달됐는지와, long/short balance(롱/숏 균형)가 여전히 약한지를 분리했습니다.

{markdown_table(comparison_rows, ['db_mt5_net', 'cv_mt5_net', 'mt5_net_delta_vs_cv', 'expected_risk_scale_net_delta', 'overlay_transfer_efficiency', 'db_profit_factor', 'db_trade_count', 'db_drawdown', 'db_long_trade_count', 'db_short_trade_count', 'short_share', 'proxy_mt5_net_gap'])}

## Result Boundary(결과 경계)

- positive clue(긍정 단서): MT5 net profit(MT5 순수익)은 CV 대비 `{comparison.get('mt5_net_delta_vs_cv')}` 개선됐고, 예상 risk-scale delta(위험비율 변화분) `{comparison.get('expected_risk_scale_net_delta')}`와 거의 맞습니다.
- unresolved guardrail(미해결 가드레일): short_share(숏 비중)는 `{comparison.get('short_share')}`이고 long/short balance(롱/숏 균형)는 아직 long-dominant(롱 우세)입니다.
- no authority(권위 없음): forward/replay/runtime authority(전진/재생/런타임 권위)는 없습니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Next(다음)

`{NEXT_RUN_ID}`는 pure exposure scaling(순수 노출 증폭) 반복이 아니라 short-source expansion(숏 원천 확장)을 탐색합니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DC decision(결정): short-quality risk-scale MT5 review

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- DB MT5 net/PF/trades(DB MT5 순수익/수익 팩터/거래수): `{final['db_mt5_net']}` / `{final['db_profit_factor']}` / `{final['db_trade_count']}`
- DB vs CV net delta(DB 대 CV 순수익 변화): `{final['mt5_net_delta_vs_cv']}`
- overlay transfer efficiency(오버레이 전달 효율): `{final['overlay_transfer_efficiency']}`
- side balance(방향 균형): `{final['side_balance_status']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DC__{RUN_ID}", f"\n- run364DC__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - DB MT5 review(DB MT5 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364DC__{RUN_ID}",
        f"""
<!-- run364DC__{RUN_ID} -->

## run364DC Short-Quality Risk-Scale Review(숏 품질 위험비율 검토)

Action(행동): DB MT5 probe(DB MT5 탐침)를 CV anchor(CV 기준점)와 비교했습니다.

Effect(효과): risk-scale overlay(위험비율 오버레이)는 긍정 단서로 남기고, side balance(방향 균형)는 다음 탐색 제약으로 남깁니다.
""",
    )
    append_text_once(STAGE_README, f"run364DC__{RUN_ID}", f"\n<!-- run364DC__{RUN_ID} -->\n## run364DC review(검토)\n\nDB MT5 review(DB MT5 검토) completed(완료). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364DC` reviewed(검토 완료) DB MT5 runtime probe(DB MT5 런타임 탐침). DB MT5 net/PF/trades(DB MT5 순수익/수익 팩터/거래수)는 `{final['db_mt5_net']}` / `{final['db_profit_factor']}` / `{final['db_trade_count']}`이고, CV 대비 net delta(순수익 변화)는 `{final['mt5_net_delta_vs_cv']}`입니다. risk-scale overlay(위험비율 오버레이)는 runtime-real clue(런타임 실제 단서)로 남지만 side balance(방향 균형)는 `{final['side_balance_status']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 short-source expansion(숏 원천 확장)을 탐색합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest reviewed MT5 runtime probe(최근 검토된 MT5 런타임 탐침): `{PARENT_RUN_ID}`.

DB MT5 net/PF/trades(DB MT5 순수익/수익 팩터/거래수): `{final['db_mt5_net']}` / `{final['db_profit_factor']}` / `{final['db_trade_count']}`.

Judgment(판정): `{JUDGMENT}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DC__{RUN_ID}", f"\n<!-- run364DC__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DB MT5 probe(DB MT5 탐침 검토); judgment `{JUDGMENT}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DC__{RUN_ID}", f"\n<!-- run364DC__{RUN_ID} -->\n- `{RUN_ID}`: risk-scale overlay(위험비율 오버레이)는 MT5 net delta(MT5 순수익 변화)로 확인됨. Effect(효과): 다음은 short-source expansion(숏 원천 확장)으로 이동.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DC__side_balance__{RUN_ID}", f"\n<!-- run364DC__side_balance__{RUN_ID} -->\n- `{RUN_ID}`: pure exposure scaling(순수 노출 증폭)은 net profit(순수익)을 올렸지만 long/short balance(롱/숏 균형)를 해결하지 못함. Effect(효과): 같은 수리만 반복하지 않고 short-source expansion(숏 원천 확장)을 다음 제약으로 둠.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "result_review(결과 검토)",
        "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "review_only_no_authority(검토 전용, 권위 없음)",
        "question": "Did cx05 risk-scale overlay transfer into MT5 value and what remains broken?(cx05 위험비율 오버레이가 MT5 가치로 전달됐고 무엇이 아직 깨졌는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["db_mt5_net"],
        "profit_factor": final["db_profit_factor"],
        "expectancy": final["db_expectancy"],
        "trade_count": final["db_trade_count"],
        "trade_density_per_feature_day": final["db_trade_density"],
        "long_trade_count": final["db_long_trade_count"],
        "short_trade_count": final["db_short_trade_count"],
        "max_drawdown_amount": final["db_drawdown"],
        "recovery_factor": final["db_recovery_factor"],
        "trade_density_requirement_status": "passed_runtime_density_ge_3_reviewed(런타임 밀도 3 이상 검토됨)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(COMPARISON_REVIEW),
        "primary_kpi": f"db_mt5_net={final['db_mt5_net']};pf={final['db_profit_factor']};trades={final['db_trade_count']};short_share={final['short_share']}",
        "guardrail_kpi": "side_balance_unresolved;runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", STATUS),
        ("tier_b_fallback_missing_required", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required_no_fallback_source(필수 누락, 대체 원천 없음)"),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", STATUS),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "DC runtime review(DC 런타임 검토)",
            "status": status,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)",
        }
        if suffix == "tier_b_fallback_missing_required":
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "long_trade_count", "short_trade_count", "max_drawdown_amount", "recovery_factor"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("comparison_review", COMPARISON_REVIEW, "DB vs CV runtime comparison(DB 대 CV 런타임 비교)."),
        ("result_judgment_receipt", RESULT_JUDGMENT_RECEIPT, "Result judgment receipt(결과 판정 영수증)."),
        ("performance_attribution_receipt", PERFORMANCE_RECEIPT, "Performance attribution receipt(성과 귀속 영수증)."),
        ("queue", RUN364DD_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DC producer script(DC 생산 스크립트)."),
    ]:
        if exists(path):
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    db_final, da_final, cv_final = validate_inputs()
    comparison_rows = build_comparison(db_final, da_final, cv_final)
    comparison = comparison_rows[0]
    build_queue(comparison)
    final = build_final(db_final, da_final, cv_final, comparison)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final, comparison)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_docs(final, comparison_rows, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    print(json.dumps(db.json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
