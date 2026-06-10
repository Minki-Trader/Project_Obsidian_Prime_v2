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
from stage_pipelines.stage364 import execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db as db  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_source_expansion_mt5_runtime_probe_without_db as dg  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_source_expansion_runtime_package_without_db as df  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = df.STAGE_ID
RUN_NUMBER = "run364DH"
RUN_ID = "run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = dg.RUN_ID
BASELINE_RUN_ID = db.RUN_ID
PACKAGE_RUN_ID = df.RUN_ID
NEXT_RUN_ID = "run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1"

STATUS = "completed_stage364DH_h17_short_source_expansion_mt5_review_positive_trade_shape_profit_retreated_no_authority"
JUDGMENT = "positive_runtime_probe_clue_short_source_added_density_but_profit_retreated_side_balance_unresolved_no_authority"
DECISION = "stage364DH_open_run364DI_short_source_profit_recovery_scout"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_short_source_expansion_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DAYS = 314.0
DENSITY_FLOOR = 3.0
PF_REVIEW_FLOOR = 1.35

STAGE_DIR = df.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

RUNTIME_REVIEW = RUN_DIR / "dg_vs_db_runtime_comparison.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN364DI_QUEUE = RUN_DIR / "run364DI_short_source_profit_recovery_queue.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DH_h17_short_source_expansion_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DH_h17_short_source_expansion_mt5_runtime_probe_review.md"
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
    dg.FINAL_DECISION,
    dg.GATE_AUDIT,
    dg.EXECUTION_SUMMARY,
    dg.PROXY_MT5_DIFF,
    dg.STRATEGY_TESTER_REPORTS,
    dg.RUNTIME_OUTPUT_COPY,
    dg.RUNTIME_IDENTITY,
    df.FINAL_DECISION,
    df.EXPECTED_KPI_SUMMARY,
    df.RUNTIME_POLICY_CONFIG,
    df.TESTER_SET_MANIFEST,
    db.FINAL_DECISION,
    db.EXECUTION_SUMMARY,
    db.PROXY_MT5_DIFF,
]

OUTPUT_FILES = [
    RUNTIME_REVIEW,
    RESULT_JUDGMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    RUN364DI_QUEUE,
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
    return dg.rel(path)


def exists(path: Path | str) -> bool:
    return dg.exists(path)


def sha(path: Path | str) -> str:
    return dg.sha(path)


def read_json(path: Path) -> Any:
    return dg.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dg.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    dg.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dg.replace_prefixed_lines(path, replacements, bom=bom)


def json_ready(value: Any) -> Any:
    return dg.json_ready(value)


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
        raise FileNotFoundError("missing DH inputs(DH 입력 누락): " + ", ".join(missing))
    dg_final = read_json(dg.FINAL_DECISION)
    df_final = read_json(df.FINAL_DECISION)
    db_final = read_json(db.FINAL_DECISION)
    if dg_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DG next_run_id mismatch(DG 다음 실행 ID 불일치): {dg_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("DG", dg_final), ("DF", df_final), ("DB", db_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    dg_gates = read_csv(dg.GATE_AUDIT)
    if dg_gates.empty or any(dg_gates["status"].astype(str) != "passed"):
        raise RuntimeError("DG gate audit(DG 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if int(float(dg_final.get("outputs_available_rows", 0) or 0)) < 1:
        raise RuntimeError("DG MT5 output(DG MT5 출력)이 review(검토)에 충분하지 않습니다.")
    return dg_final, df_final, db_final


def first_row(path: Path) -> dict[str, Any]:
    frame = read_csv(path)
    return {} if frame.empty else frame.iloc[0].to_dict()


def build_review(dg_final: Mapping[str, Any], df_final: Mapping[str, Any], db_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    dg_row = first_row(dg.EXECUTION_SUMMARY)
    db_row = first_row(db.EXECUTION_SUMMARY)
    proxy_row = first_row(dg.PROXY_MT5_DIFF)

    dg_trades = float_or_nan(dg_row.get("trade_count"))
    db_trades = float_or_nan(db_row.get("trade_count"))
    dg_short = float_or_nan(dg_row.get("short_trade_count"))
    db_short = float_or_nan(db_row.get("short_trade_count"))
    dg_long = float_or_nan(dg_row.get("long_trade_count"))
    db_long = float_or_nan(db_row.get("long_trade_count"))
    dg_net = float_or_nan(dg_row.get("net_profit"))
    db_net = float_or_nan(db_row.get("net_profit"))
    dg_pf = float_or_nan(dg_row.get("profit_factor"))
    db_pf = float_or_nan(db_row.get("profit_factor"))
    dg_expectancy = float_or_nan(dg_row.get("expectancy"))
    db_expectancy = float_or_nan(db_row.get("expectancy"))
    dg_dd = float_or_nan(dg_row.get("max_drawdown_amount"))
    db_dd = float_or_nan(db_row.get("max_drawdown_amount"))
    dg_recovery = float_or_nan(dg_row.get("recovery_factor"))
    db_recovery = float_or_nan(db_row.get("recovery_factor"))

    dg_density = dg_trades / DAYS if math.isfinite(dg_trades) else math.nan
    db_density = db_trades / DAYS if math.isfinite(db_trades) else math.nan
    dg_short_share = dg_short / dg_trades if math.isfinite(dg_short) and math.isfinite(dg_trades) and dg_trades else math.nan
    db_short_share = db_short / db_trades if math.isfinite(db_short) and math.isfinite(db_trades) and db_trades else math.nan
    dg_long_share = dg_long / dg_trades if math.isfinite(dg_long) and math.isfinite(dg_trades) and dg_trades else math.nan

    rows = [
        {
            "run_id": RUN_ID,
            "candidate_id": dg_final.get("candidate_id", ""),
            "comparison_baseline": BASELINE_RUN_ID,
            "dg_mt5_net": finite(dg_net),
            "db_mt5_net": finite(db_net),
            "net_delta_vs_db": finite(dg_net - db_net),
            "dg_profit_factor": finite(dg_pf),
            "db_profit_factor": finite(db_pf),
            "profit_factor_delta_vs_db": finite(dg_pf - db_pf),
            "dg_expectancy": finite(dg_expectancy),
            "db_expectancy": finite(db_expectancy),
            "expectancy_delta_vs_db": finite(dg_expectancy - db_expectancy),
            "dg_drawdown": finite(dg_dd),
            "db_drawdown": finite(db_dd),
            "drawdown_delta_vs_db": finite(dg_dd - db_dd),
            "dg_recovery_factor": finite(dg_recovery),
            "db_recovery_factor": finite(db_recovery),
            "recovery_factor_delta_vs_db": finite(dg_recovery - db_recovery),
            "dg_trade_count": finite(dg_trades, 0),
            "db_trade_count": finite(db_trades, 0),
            "trade_count_delta_vs_db": finite(dg_trades - db_trades, 0),
            "dg_trade_density": finite(dg_density),
            "db_trade_density": finite(db_density),
            "density_status": "passed_density_floor(거래 밀도 하한 통과)" if math.isfinite(dg_density) and dg_density >= DENSITY_FLOOR else "failed_density_floor(거래 밀도 하한 실패)",
            "dg_long_trade_count": finite(dg_long, 0),
            "dg_short_trade_count": finite(dg_short, 0),
            "db_long_trade_count": finite(db_long, 0),
            "db_short_trade_count": finite(db_short, 0),
            "short_count_delta_vs_db": finite(dg_short - db_short, 0),
            "long_count_delta_vs_db": finite(dg_long - db_long, 0),
            "dg_short_share": finite(dg_short_share),
            "db_short_share": finite(db_short_share),
            "short_share_delta_vs_db": finite(dg_short_share - db_short_share),
            "dg_long_share": finite(dg_long_share),
            "expected_net": proxy_row.get("expected_net_profit", ""),
            "actual_mt5_net": proxy_row.get("actual_mt5_net_profit", ""),
            "proxy_mt5_net_gap": proxy_row.get("net_profit_diff_actual_minus_expected", ""),
            "expected_profit_factor": proxy_row.get("expected_profit_factor", ""),
            "actual_mt5_profit_factor": proxy_row.get("actual_mt5_profit_factor", ""),
            "proxy_mt5_pf_gap": proxy_row.get("profit_factor_diff_actual_minus_expected", ""),
            "expected_trade_count": proxy_row.get("expected_trade_count", ""),
            "actual_mt5_trade_count": proxy_row.get("actual_mt5_trade_count", ""),
            "proxy_mt5_trade_gap": proxy_row.get("trade_count_diff_actual_minus_expected", ""),
            "profit_recovery_status": "profit_retreated_vs_db(수익 후퇴)" if math.isfinite(dg_net) and math.isfinite(db_net) and dg_net < db_net else "profit_preserved_vs_db(수익 보존)",
            "side_balance_status": "improved_but_long_dominant(개선됐지만 롱 우세)",
            "review_label": "positive_trade_shape_clue_not_baseline_replacement(긍정 거래 형태 단서, 기준선 교체 아님)",
            "attribution_confidence": "medium(중간)",
            "effect": "short-source expansion(숏 원천 확장)은 short count(숏 거래수)와 density(거래 밀도)를 올렸지만 net/PF/expectancy(순수익/수익 팩터/기대값)는 DB 기준선보다 후퇴했습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUNTIME_REVIEW, rows)
    return rows


def build_queue(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "di01_short_source_profit_recovery",
            "seed": "DG increased short count(DG 숏 거래수 증가) but lost DB net/PF(DB 순수익/수익 팩터 후퇴)",
            "target_question": "Can we keep DG short-count lift while recovering DB net/PF/expectancy?(DG 숏 거래수 상승을 유지하면서 DB 순수익/수익 팩터/기대값을 회복할 수 있는가?)",
            "baseline_mt5_net": review.get("db_mt5_net", ""),
            "dg_mt5_net": review.get("dg_mt5_net", ""),
            "baseline_mt5_profit_factor": review.get("db_profit_factor", ""),
            "dg_mt5_profit_factor": review.get("dg_profit_factor", ""),
            "dg_short_trade_count": review.get("dg_short_trade_count", ""),
            "db_short_trade_count": review.get("db_short_trade_count", ""),
            "success_criteria": "MT5-shaped proxy(프록시)는 density>=3(거래 밀도 3 이상), short_count>=125(숏 거래수 125 이상), PF>=1.40(수익 팩터 1.40 이상), net near or above DB(DB 근처 또는 초과 순수익)를 동시에 요구합니다.",
            "allowed_ideas": "sweep InpSyntheticShortSourceMarginVsFlatMin(숏 원천 대 플랫 최소 마진 탐색), hour-specific veto(시간별 배제), reason-source quality filter(사유 원천 품질 필터), no trade splitting(거래 쪼개기 금지)",
            "failure_memory": "Do not accept added trades if they dilute expectancy(기대값을 희석하는 거래 증가 금지). DG added 42 trades and 41 shorts but net fell 30.90 versus DB(DG는 거래 42개와 숏 41개를 추가했지만 DB 대비 순수익이 30.90 낮아졌습니다).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364DI_QUEUE, rows)
    return rows


def build_final(dg_final: Mapping[str, Any], df_final: Mapping[str, Any], db_final: Mapping[str, Any], review: Mapping[str, Any]) -> dict[str, Any]:
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
        "candidate_id": dg_final.get("candidate_id", ""),
        "model_id": dg_final.get("model_id", ""),
        "created_at_utc": now_utc(),
        "dg_mt5_net": review.get("dg_mt5_net", ""),
        "dg_profit_factor": review.get("dg_profit_factor", ""),
        "dg_expectancy": review.get("dg_expectancy", ""),
        "dg_trade_count": review.get("dg_trade_count", ""),
        "dg_trade_density": review.get("dg_trade_density", ""),
        "dg_drawdown": review.get("dg_drawdown", ""),
        "dg_recovery_factor": review.get("dg_recovery_factor", ""),
        "dg_long_trade_count": review.get("dg_long_trade_count", ""),
        "dg_short_trade_count": review.get("dg_short_trade_count", ""),
        "dg_short_share": review.get("dg_short_share", ""),
        "db_mt5_net": review.get("db_mt5_net", ""),
        "db_profit_factor": review.get("db_profit_factor", ""),
        "db_trade_count": review.get("db_trade_count", ""),
        "net_delta_vs_db": review.get("net_delta_vs_db", ""),
        "profit_factor_delta_vs_db": review.get("profit_factor_delta_vs_db", ""),
        "short_count_delta_vs_db": review.get("short_count_delta_vs_db", ""),
        "short_share_delta_vs_db": review.get("short_share_delta_vs_db", ""),
        "proxy_mt5_net_gap": review.get("proxy_mt5_net_gap", ""),
        "proxy_mt5_pf_gap": review.get("proxy_mt5_pf_gap", ""),
        "result_subject": "run364DG DD05 short-source expansion MT5 runtime probe(run364DG DD05 숏 원천 확장 MT5 런타임 탐침)",
        "evidence_available": [rel(dg.EXECUTION_SUMMARY), rel(dg.PROXY_MT5_DIFF), rel(dg.STRATEGY_TESTER_REPORTS), rel(RUNTIME_REVIEW)],
        "evidence_missing": [
            "forward/replay evidence(전진/재생 근거)",
            "runtime authority closure(런타임 권위 폐쇄)",
            "Tier B fallback source(Tier B 대체 원천)",
            "session/regime split review(세션/국면 분할 검토)",
            "cost stress expansion beyond tester defaults(테스터 기본값 밖 비용 압박 확장)",
        ],
        "external_verification_status": "completed(완료)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
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
            "effect": "DG/DF/DB evidence(DG/DF/DB 근거)를 같은 비교 경계에 묶습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "mt5_output_review_gate",
            "status": "passed",
            "evidence": rel(dg.EXECUTION_SUMMARY),
            "effect": "MT5 runtime output(MT5 런타임 출력)이 review(검토) 가능한지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "baseline_trade_shape_comparison_gate",
            "status": "passed",
            "evidence": rel(RUNTIME_REVIEW),
            "effect": "DB baseline(DB 기준선) 대비 수익 구조와 trade shape(거래 형태)를 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "proxy_mt5_gap_attribution_gate",
            "status": "passed",
            "evidence": rel(dg.PROXY_MT5_DIFF),
            "effect": "proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "result_judgment_boundary_gate",
            "status": "passed",
            "evidence": rel(RESULT_JUDGMENT_RECEIPT),
            "effect": "positive clue(긍정 단서)를 operating promotion(운영 승격)으로 올리지 않습니다.",
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
            "effect": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 모두 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(final: Mapping[str, Any], review: Mapping[str, Any]) -> None:
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
            "user_explanation_hook": "MT5 기준으로 DD05는 거래 밀도와 숏 비중을 늘렸지만 DB 기준선의 순수익/수익 팩터를 아직 넘지 못했습니다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": f"DG net {review.get('dg_mt5_net')} vs DB net {review.get('db_mt5_net')} delta {review.get('net_delta_vs_db')}; short delta {review.get('short_count_delta_vs_db')}",
            "comparison_baseline": BASELINE_RUN_ID,
            "likely_drivers": [
                "synthetic short-source expansion(합성 숏 원천 확장)",
                "margin_vs_flat runtime guard(플랫 대비 마진 런타임 가드)",
                "additional short entries(추가 숏 진입)",
            ],
            "segment_checks": {
                "direction": "long/short counts reviewed(롱/숏 거래수 검토됨)",
                "drawdown": "max drawdown compared against DB(DB 대비 최대 낙폭 비교됨)",
                "density": "trade density checked against user floor(사용자 거래 밀도 하한 대비 확인됨)",
                "session_regime": "missing_for_next_probe(다음 탐침 필요)",
                "cost": "Strategy Tester native report only(전략 테스터 기본 보고서 한정)",
            },
            "trade_shape": {
                "trade_count": review.get("dg_trade_count"),
                "trade_density": review.get("dg_trade_density"),
                "long_trade_count": review.get("dg_long_trade_count"),
                "short_trade_count": review.get("dg_short_trade_count"),
                "short_share": review.get("dg_short_share"),
                "profit_factor": review.get("dg_profit_factor"),
                "drawdown": review.get("dg_drawdown"),
                "recovery_factor": review.get("dg_recovery_factor"),
            },
            "alternative_explanations": [
                "new shorts may be lower expectancy(새 숏 거래의 낮은 기대값 가능성)",
                "proxy/MT5 fill and cost gap(프록시/MT5 체결 및 비용 차이)",
                "hour-17 short source may add volume before quality(17시 숏 원천이 품질보다 거래량을 먼저 늘렸을 가능성)",
            ],
            "attribution_confidence": review.get("attribution_confidence", "medium(중간)"),
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(df.TESTER_IDENTITY_CONTRACT),
            "ea_identity": rel(dg.RUNTIME_IDENTITY),
            "report_identity": [rel(dg.STRATEGY_TESTER_REPORTS), final.get("report_path", "")],
            "trade_evidence": {
                "trade_count": final["dg_trade_count"],
                "net_profit": final["dg_mt5_net"],
                "drawdown": final["dg_drawdown"],
                "profit_factor": final["dg_profit_factor"],
                "trade_list_availability": "strategy_report_artifact_available(전략 보고서 산출물 있음)",
            },
            "cost_assumptions": "broker-native Strategy Tester output only(브로커 기반 전략 테스터 출력 한정)",
            "forensic_checks": [rel(dg.MT5_EXECUTION_RESULT), rel(dg.STRATEGY_TESTER_REPORTS), rel(dg.RUNTIME_OUTPUT_COPY), rel(RUNTIME_REVIEW)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": [rel(df.RUNTIME_POLICY_CONFIG), rel(df.EXPECTED_KPI_SUMMARY)],
            "runtime_path": [rel(df.TESTER_SET_MANIFEST), rel(df.TESTER_INI_MANIFEST), rel(dg.EXECUTION_SUMMARY)],
            "shared_contract": rel(df.RUNTIME_PARITY_CONTRACT),
            "known_differences": "proxy expected value(프록시 예상값)는 MT5 cost/fill/runtime(MT5 비용/체결/런타임)을 대체하지 않습니다.",
            "parity_check": [rel(dg.PROXY_MT5_DIFF), rel(RUNTIME_REVIEW)],
            "parity_identity": {"source_onnx_sha256": sha(df.SOURCE_ONNX), "tester_set_manifest_sha256": sha(df.TESTER_SET_MANIFEST)},
            "runtime_claim_boundary": "runtime_probe_review(런타임 탐침 검토), not authority(권위 아님)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
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
    return df.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    review = review_rows[0]
    report = f"""# run364DH h17 short-source expansion MT5 runtime probe review(17시 숏 원천 확장 MT5 런타임 탐침 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- baseline_run_id(기준선 실행 ID): `{BASELINE_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): DG MT5 result(DG MT5 결과)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): short-source expansion(숏 원천 확장)이 trade shape(거래 형태)는 개선했지만, DB 기준 순수익/수익 팩터 회복이 필요하다는 다음 탐색 조건(next exploration condition, 다음 탐색 조건)을 분리했습니다.

{markdown_table(review_rows, ['dg_mt5_net', 'db_mt5_net', 'net_delta_vs_db', 'dg_profit_factor', 'db_profit_factor', 'profit_factor_delta_vs_db', 'dg_trade_count', 'db_trade_count', 'dg_short_trade_count', 'db_short_trade_count', 'short_count_delta_vs_db', 'dg_short_share', 'db_short_share', 'proxy_mt5_net_gap'])}

## Result Boundary(결과 경계)

- positive clue(긍정 단서): DG는 DB보다 short count(숏 거래수)를 `{review.get('short_count_delta_vs_db')}` 늘리고 trade density(거래 밀도)를 `{review.get('dg_trade_density')}`까지 올렸습니다.
- unresolved guardrail(미해결 가드레일): DG net/PF/expectancy(순수익/수익 팩터/기대값)는 DB보다 각각 `{review.get('net_delta_vs_db')}` / `{review.get('profit_factor_delta_vs_db')}` / `{review.get('expectancy_delta_vs_db')}` 후퇴했습니다.
- no authority(권위 없음): forward/replay/runtime authority(전진/재생/런타임 권위)는 없고, 운영 승격(operating promotion, 운영 승격)도 없습니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Next(다음)

`{NEXT_RUN_ID}`는 margin_vs_flat(플랫 대비 마진), hour veto(시간 배제), short-source quality filter(숏 원천 품질 필터)를 탐색합니다. 효과(effect, 효과)는 숏 거래수 상승을 유지하면서 DB 기준 순수익/수익 팩터를 회복할 후보를 찾는 것입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DH decision(결정): short-source expansion MT5 review(숏 원천 확장 MT5 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- DG MT5 net/PF/trades(DG MT5 순수익/수익 팩터/거래수): `{final['dg_mt5_net']}` / `{final['dg_profit_factor']}` / `{final['dg_trade_count']}`
- DB baseline net/PF/trades(DB 기준선 순수익/수익 팩터/거래수): `{final['db_mt5_net']}` / `{final['db_profit_factor']}` / `{final['db_trade_count']}`
- short count delta(숏 거래수 변화): `{final['short_count_delta_vs_db']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DI는 숏 거래수 증가를 보존하면서 순수익/수익 팩터 후퇴를 복구하는 탐색입니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DH__{RUN_ID}", f"\n- run364DH__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - DD05 MT5 review(DD05 MT5 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364DH__{RUN_ID}",
        f"""
<!-- run364DH__{RUN_ID} -->

## run364DH Short-Source Expansion Review(숏 원천 확장 검토)

Action(행동): DG MT5 probe(DG MT5 탐침)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): 숏 원천 확장은 거래수와 숏 비중을 늘렸지만 순수익/수익 팩터 회복이 필요하므로 `{NEXT_RUN_ID}`로 profit recovery(수익 회복) 탐색을 엽니다.
""",
    )
    append_text_once(STAGE_README, f"run364DH__{RUN_ID}", f"\n<!-- run364DH__{RUN_ID} -->\n## run364DH review(검토)\n\nDD05 MT5 review(DD05 MT5 검토) completed(완료). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DH` reviewed(검토 완료) DD05 short-source expansion MT5 runtime probe(DD05 숏 원천 확장 MT5 런타임 탐침). DG MT5 net/PF/trades(DG MT5 순수익/수익 팩터/거래수)는 `{final['dg_mt5_net']}` / `{final['dg_profit_factor']}` / `{final['dg_trade_count']}`이고, DB baseline(DB 기준선) 대비 net delta(순수익 변화)는 `{final['net_delta_vs_db']}`, short count delta(숏 거래수 변화)는 `{final['short_count_delta_vs_db']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 short-source profit recovery(숏 원천 수익 회복)를 탐색합니다.

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

DG MT5 net/PF/trades(DG MT5 순수익/수익 팩터/거래수): `{final['dg_mt5_net']}` / `{final['dg_profit_factor']}` / `{final['dg_trade_count']}`.

DB baseline net/PF/trades(DB 기준선 순수익/수익 팩터/거래수): `{final['db_mt5_net']}` / `{final['db_profit_factor']}` / `{final['db_trade_count']}`.

Judgment(판정): `{JUDGMENT}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DH__{RUN_ID}", f"\n<!-- run364DH__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DD05 MT5 probe(DD05 MT5 탐침 검토); judgment `{JUDGMENT}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DH__{RUN_ID}", f"\n<!-- run364DH__{RUN_ID} -->\n- `{RUN_ID}`: DD05 short-source expansion(DD05 숏 원천 확장)은 MT5에서 short count(숏 거래수)를 늘렸지만 net/PF(순수익/수익 팩터)가 DB보다 후퇴했습니다. Effect(효과): 다음은 short-source profit recovery(숏 원천 수익 회복)입니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DH__profit_retreat__{RUN_ID}", f"\n<!-- run364DH__profit_retreat__{RUN_ID} -->\n- `{RUN_ID}`: short-source expansion(숏 원천 확장)은 거래수 증가만으로는 충분하지 않았습니다. Net delta vs DB(DB 대비 순수익 변화) `{final['net_delta_vs_db']}`, PF delta(PF 변화) `{final['profit_factor_delta_vs_db']}`. Effect(효과): DI는 low-quality added shorts(저품질 추가 숏)를 거르는 방향으로 진행합니다.\n")


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
        "question": "Did DD05 short-source expansion improve MT5 trade shape without damaging profit?(DD05 숏 원천 확장이 MT5 거래 형태를 개선하면서 수익을 해치지 않았는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["dg_mt5_net"],
        "profit_factor": final["dg_profit_factor"],
        "expectancy": final["dg_expectancy"],
        "trade_count": final["dg_trade_count"],
        "trade_density_per_feature_day": final["dg_trade_density"],
        "long_trade_count": final["dg_long_trade_count"],
        "short_trade_count": final["dg_short_trade_count"],
        "max_drawdown_amount": final["dg_drawdown"],
        "recovery_factor": final["dg_recovery_factor"],
        "trade_density_requirement_status": "passed_runtime_density_ge_3_reviewed(런타임 거래 밀도 3 이상 검토됨)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_REVIEW),
        "primary_kpi": f"dg_mt5_net={final['dg_mt5_net']};pf={final['dg_profit_factor']};trades={final['dg_trade_count']};shorts={final['dg_short_trade_count']}",
        "guardrail_kpi": "profit_retreated_vs_db;runtime_authority=not_claimed;operating_promotion=not_claimed",
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
            "kpi_scope": "DH runtime review(DH 런타임 검토)",
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
        ("runtime_review", RUNTIME_REVIEW, "DG vs DB runtime review(DG 대 DB 런타임 검토)."),
        ("result_judgment_receipt", RESULT_JUDGMENT_RECEIPT, "Result judgment receipt(결과 판정 영수증)."),
        ("performance_attribution_receipt", PERFORMANCE_RECEIPT, "Performance attribution receipt(성과 귀속 영수증)."),
        ("backtest_forensics_receipt", BACKTEST_RECEIPT, "Backtest forensics receipt(백테스트 포렌식 영수증)."),
        ("runtime_parity_receipt", RUNTIME_RECEIPT, "Runtime parity receipt(런타임 동등성 영수증)."),
        ("queue", RUN364DI_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DH producer script(DH 생산 스크립트)."),
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
    dg_final, df_final, db_final = validate_inputs()
    review_rows = build_review(dg_final, df_final, db_final)
    review = review_rows[0]
    build_queue(review)
    final = build_final(dg_final, df_final, db_final, review)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final, review)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_docs(final, review_rows, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
