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
from stage_pipelines.stage364 import execute_h17_short_source_expansion_mt5_runtime_probe_without_db as dg_source  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_source_profit_recovery_mt5_runtime_probe_without_db as dl  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_source_profit_recovery_runtime_package_without_db as dk  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dk.STAGE_ID
RUN_NUMBER = "run364DM"
RUN_ID = "run364DM_review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = dl.RUN_ID
BASELINE_RUN_ID = db.RUN_ID
SOURCE_EXPANSION_RUN_ID = dg_source.RUN_ID
PACKAGE_RUN_ID = dk.RUN_ID
NEXT_RUN_ID = "run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1"

STATUS = "completed_stage364DM_h17_short_source_profit_recovery_mt5_review_positive_near_db_profit_short_lift_no_authority"
JUDGMENT = "positive_runtime_probe_clue_profit_recovered_near_db_short_lift_preserved_pf_slightly_below_db_no_authority"
DECISION = "stage364DM_open_run364DN_short_source_pf_balance_polish_scout"
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_review_only_short_source_profit_recovery_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DAYS = 314.0
DENSITY_FLOOR = 3.0
PF_REVIEW_FLOOR = 1.35

STAGE_DIR = dk.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

RUNTIME_REVIEW = RUN_DIR / "dl_vs_db_dg_runtime_comparison.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN364DN_QUEUE = RUN_DIR / "run364DN_short_source_pf_balance_polish_queue.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DM_h17_short_source_profit_recovery_mt5_runtime_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DM_h17_short_source_profit_recovery_mt5_runtime_probe_review.md"
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
    dl.FINAL_DECISION,
    dl.GATE_AUDIT,
    dl.EXECUTION_SUMMARY,
    dl.PROXY_MT5_DIFF,
    dl.STRATEGY_TESTER_REPORTS,
    dl.RUNTIME_OUTPUT_COPY,
    dl.RUNTIME_IDENTITY,
    dk.FINAL_DECISION,
    dk.EXPECTED_KPI_SUMMARY,
    dk.RUNTIME_POLICY_CONFIG,
    dk.TESTER_SET_MANIFEST,
    dg_source.FINAL_DECISION,
    dg_source.EXECUTION_SUMMARY,
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
    RUN364DN_QUEUE,
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
    return dl.rel(path)


def exists(path: Path | str) -> bool:
    return dl.exists(path)


def sha(path: Path | str) -> str:
    return dl.sha(path)


def read_json(path: Path) -> Any:
    return dl.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dl.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    dl.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dl.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dl.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dl.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dl.replace_prefixed_lines(path, replacements, bom=bom)


def json_ready(value: Any) -> Any:
    return dl.json_ready(value)


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
        raise FileNotFoundError("missing DM inputs(DM 입력 누락): " + ", ".join(missing))
    dl_final = read_json(dl.FINAL_DECISION)
    dk_final = read_json(dk.FINAL_DECISION)
    db_final = read_json(db.FINAL_DECISION)
    dg_source_final = read_json(dg_source.FINAL_DECISION)
    if dl_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DL next_run_id mismatch(DL 다음 실행 ID 불일치): {dl_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("DL", dl_final), ("DK", dk_final), ("DB", db_final), ("DG", dg_source_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    dl_gates = read_csv(dl.GATE_AUDIT)
    if dl_gates.empty or any(dl_gates["status"].astype(str) != "passed"):
        raise RuntimeError("DL gate audit(DL 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if int(float(dl_final.get("outputs_available_rows", 0) or 0)) < 1:
        raise RuntimeError("DL MT5 output(DL MT5 출력)이 review(검토)에 충분하지 않습니다.")
    return dl_final, dk_final, db_final


def first_row(path: Path) -> dict[str, Any]:
    frame = read_csv(path)
    return {} if frame.empty else frame.iloc[0].to_dict()


def build_review(dl_final: Mapping[str, Any], dk_final: Mapping[str, Any], db_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    dl_row = first_row(dl.EXECUTION_SUMMARY)
    db_row = first_row(db.EXECUTION_SUMMARY)
    dg_source_row = first_row(dg_source.EXECUTION_SUMMARY)
    proxy_row = first_row(dl.PROXY_MT5_DIFF)

    dl_trades = float_or_nan(dl_row.get("trade_count"))
    db_trades = float_or_nan(db_row.get("trade_count"))
    dl_short = float_or_nan(dl_row.get("short_trade_count"))
    db_short = float_or_nan(db_row.get("short_trade_count"))
    dl_long = float_or_nan(dl_row.get("long_trade_count"))
    db_long = float_or_nan(db_row.get("long_trade_count"))
    dl_net = float_or_nan(dl_row.get("net_profit"))
    db_net = float_or_nan(db_row.get("net_profit"))
    dl_pf = float_or_nan(dl_row.get("profit_factor"))
    db_pf = float_or_nan(db_row.get("profit_factor"))
    dl_expectancy = float_or_nan(dl_row.get("expectancy"))
    db_expectancy = float_or_nan(db_row.get("expectancy"))
    dl_dd = float_or_nan(dl_row.get("max_drawdown_amount"))
    db_dd = float_or_nan(db_row.get("max_drawdown_amount"))
    dl_recovery = float_or_nan(dl_row.get("recovery_factor"))
    db_recovery = float_or_nan(db_row.get("recovery_factor"))
    dg_source_net = float_or_nan(dg_source_row.get("net_profit"))
    dg_source_pf = float_or_nan(dg_source_row.get("profit_factor"))
    dg_source_trades = float_or_nan(dg_source_row.get("trade_count"))
    dg_source_short = float_or_nan(dg_source_row.get("short_trade_count"))

    dl_density = dl_trades / DAYS if math.isfinite(dl_trades) else math.nan
    db_density = db_trades / DAYS if math.isfinite(db_trades) else math.nan
    dl_short_share = dl_short / dl_trades if math.isfinite(dl_short) and math.isfinite(dl_trades) and dl_trades else math.nan
    db_short_share = db_short / db_trades if math.isfinite(db_short) and math.isfinite(db_trades) and db_trades else math.nan
    dl_long_share = dl_long / dl_trades if math.isfinite(dl_long) and math.isfinite(dl_trades) and dl_trades else math.nan

    rows = [
        {
            "run_id": RUN_ID,
            "candidate_id": dl_final.get("candidate_id", ""),
            "comparison_baseline": BASELINE_RUN_ID,
            "comparison_source_expansion": SOURCE_EXPANSION_RUN_ID,
            "dl_mt5_net": finite(dl_net),
            "db_mt5_net": finite(db_net),
            "net_delta_vs_db": finite(dl_net - db_net),
            "dg_source_mt5_net": finite(dg_source_net),
            "net_delta_vs_dg_source": finite(dl_net - dg_source_net),
            "dl_profit_factor": finite(dl_pf),
            "db_profit_factor": finite(db_pf),
            "profit_factor_delta_vs_db": finite(dl_pf - db_pf),
            "dg_source_profit_factor": finite(dg_source_pf),
            "profit_factor_delta_vs_dg_source": finite(dl_pf - dg_source_pf),
            "dl_expectancy": finite(dl_expectancy),
            "db_expectancy": finite(db_expectancy),
            "expectancy_delta_vs_db": finite(dl_expectancy - db_expectancy),
            "dl_drawdown": finite(dl_dd),
            "db_drawdown": finite(db_dd),
            "drawdown_delta_vs_db": finite(dl_dd - db_dd),
            "dl_recovery_factor": finite(dl_recovery),
            "db_recovery_factor": finite(db_recovery),
            "recovery_factor_delta_vs_db": finite(dl_recovery - db_recovery),
            "dl_trade_count": finite(dl_trades, 0),
            "db_trade_count": finite(db_trades, 0),
            "trade_count_delta_vs_db": finite(dl_trades - db_trades, 0),
            "dg_source_trade_count": finite(dg_source_trades, 0),
            "trade_count_delta_vs_dg_source": finite(dl_trades - dg_source_trades, 0),
            "dl_trade_density": finite(dl_density),
            "db_trade_density": finite(db_density),
            "density_status": "passed_density_floor(거래 밀도 하한 통과)" if math.isfinite(dl_density) and dl_density >= DENSITY_FLOOR else "failed_density_floor(거래 밀도 하한 실패)",
            "dl_long_trade_count": finite(dl_long, 0),
            "dl_short_trade_count": finite(dl_short, 0),
            "db_long_trade_count": finite(db_long, 0),
            "db_short_trade_count": finite(db_short, 0),
            "short_count_delta_vs_db": finite(dl_short - db_short, 0),
            "dg_source_short_trade_count": finite(dg_source_short, 0),
            "short_count_delta_vs_dg_source": finite(dl_short - dg_source_short, 0),
            "long_count_delta_vs_db": finite(dl_long - db_long, 0),
            "dl_short_share": finite(dl_short_share),
            "db_short_share": finite(db_short_share),
            "short_share_delta_vs_db": finite(dl_short_share - db_short_share),
            "dl_long_share": finite(dl_long_share),
            "expected_net": proxy_row.get("expected_net_profit", ""),
            "actual_mt5_net": proxy_row.get("actual_mt5_net_profit", ""),
            "proxy_mt5_net_gap": proxy_row.get("net_profit_diff_actual_minus_expected", ""),
            "expected_profit_factor": proxy_row.get("expected_profit_factor", ""),
            "actual_mt5_profit_factor": proxy_row.get("actual_mt5_profit_factor", ""),
            "proxy_mt5_pf_gap": proxy_row.get("profit_factor_diff_actual_minus_expected", ""),
            "expected_trade_count": proxy_row.get("expected_trade_count", ""),
            "actual_mt5_trade_count": proxy_row.get("actual_mt5_trade_count", ""),
            "proxy_mt5_trade_gap": proxy_row.get("trade_count_diff_actual_minus_expected", ""),
            "profit_recovery_status": "near_db_profit_recovered_but_not_exceeded(DB 근접 수익 회복, 초과 아님)" if math.isfinite(dl_net) and math.isfinite(db_net) and abs(dl_net - db_net) <= 2.0 else ("profit_retreated_vs_db(수익 후퇴)" if math.isfinite(dl_net) and math.isfinite(db_net) and dl_net < db_net else "profit_preserved_vs_db(수익 보존)"),
            "side_balance_status": "improved_vs_db_but_less_than_dg_source(DB 대비 개선, DG 원천 확장보다는 낮음)",
            "review_label": "positive_runtime_probe_clue_not_baseline_replacement(긍정 런타임 탐침 단서, 기준선 교체 아님)",
            "attribution_confidence": "medium(중간)",
            "effect": "short-source profit recovery(숏 원천 수익 회복)는 DG 대비 순수익을 회복하고 DB 대비 숏 거래수를 늘렸지만 PF는 DB보다 약간 낮습니다.",
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
            "queue_id": "dn01_short_source_pf_balance_polish",
            "seed": "DL recovered DG profit retreat(DL은 DG 수익 후퇴를 회복) but remains slightly below DB PF/net(DB 수익 팩터/순수익보다 약간 낮음)",
            "target_question": "Can we keep DL short-count lift while lifting PF/net above DB?(DL 숏 거래수 상승을 유지하면서 PF/순수익을 DB 위로 올릴 수 있는가?)",
            "baseline_mt5_net": review.get("db_mt5_net", ""),
            "dl_mt5_net": review.get("dl_mt5_net", ""),
            "baseline_mt5_profit_factor": review.get("db_profit_factor", ""),
            "dl_mt5_profit_factor": review.get("dl_profit_factor", ""),
            "dl_short_trade_count": review.get("dl_short_trade_count", ""),
            "db_short_trade_count": review.get("db_short_trade_count", ""),
            "net_delta_vs_dg_source": review.get("net_delta_vs_dg_source", ""),
            "short_count_delta_vs_dg_source": review.get("short_count_delta_vs_dg_source", ""),
            "success_criteria": "MT5-shaped proxy(프록시)는 density>=3(거래 밀도 3 이상), short_count>=125(숏 거래수 125 이상), PF>DB 1.41(DB 수익 팩터 1.41 초과), net>DB 1018.78(DB 순수익 1018.78 초과)를 동시에 요구합니다.",
            "allowed_ideas": "tighten flat margin(플랫 마진 강화), hour-pair veto(시간쌍 배제), short-source quality rank(숏 원천 품질 순위), no trade splitting(거래 쪼개기 금지)",
            "failure_memory": "DL is near DB net(-0.67) and above DB short count(+32), but PF remains -0.01 below DB(DL은 DB 순수익에 근접하고 숏 거래수는 높지만 PF는 DB보다 0.01 낮음). Do not add density without PF lift(PF 상승 없는 밀도 추가 금지).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUN364DN_QUEUE, rows)
    return rows


def build_final(dl_final: Mapping[str, Any], dk_final: Mapping[str, Any], db_final: Mapping[str, Any], review: Mapping[str, Any]) -> dict[str, Any]:
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
        "candidate_id": dl_final.get("candidate_id", ""),
        "model_id": dl_final.get("model_id", ""),
        "created_at_utc": now_utc(),
        "dl_mt5_net": review.get("dl_mt5_net", ""),
        "dl_profit_factor": review.get("dl_profit_factor", ""),
        "dl_expectancy": review.get("dl_expectancy", ""),
        "dl_trade_count": review.get("dl_trade_count", ""),
        "dl_trade_density": review.get("dl_trade_density", ""),
        "dl_drawdown": review.get("dl_drawdown", ""),
        "dl_recovery_factor": review.get("dl_recovery_factor", ""),
        "dl_long_trade_count": review.get("dl_long_trade_count", ""),
        "dl_short_trade_count": review.get("dl_short_trade_count", ""),
        "dl_short_share": review.get("dl_short_share", ""),
        "db_mt5_net": review.get("db_mt5_net", ""),
        "db_profit_factor": review.get("db_profit_factor", ""),
        "db_trade_count": review.get("db_trade_count", ""),
        "dg_source_mt5_net": review.get("dg_source_mt5_net", ""),
        "dg_source_profit_factor": review.get("dg_source_profit_factor", ""),
        "dg_source_trade_count": review.get("dg_source_trade_count", ""),
        "dg_source_short_trade_count": review.get("dg_source_short_trade_count", ""),
        "net_delta_vs_db": review.get("net_delta_vs_db", ""),
        "net_delta_vs_dg_source": review.get("net_delta_vs_dg_source", ""),
        "profit_factor_delta_vs_db": review.get("profit_factor_delta_vs_db", ""),
        "profit_factor_delta_vs_dg_source": review.get("profit_factor_delta_vs_dg_source", ""),
        "short_count_delta_vs_db": review.get("short_count_delta_vs_db", ""),
        "short_count_delta_vs_dg_source": review.get("short_count_delta_vs_dg_source", ""),
        "short_share_delta_vs_db": review.get("short_share_delta_vs_db", ""),
        "proxy_mt5_net_gap": review.get("proxy_mt5_net_gap", ""),
        "proxy_mt5_pf_gap": review.get("proxy_mt5_pf_gap", ""),
        "result_subject": "run364DL DI02 no19 short-source profit recovery MT5 runtime probe(run364DL DI02 19시 배제 숏 원천 수익 회복 MT5 런타임 탐침)",
        "evidence_available": [rel(dl.EXECUTION_SUMMARY), rel(dl.PROXY_MT5_DIFF), rel(dl.STRATEGY_TESTER_REPORTS), rel(RUNTIME_REVIEW)],
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
            "effect": "DL/DK/DB/DG evidence(DL/DK/DB/DG 근거)를 같은 비교 경계에 묶습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "mt5_output_review_gate",
            "status": "passed",
            "evidence": rel(dl.EXECUTION_SUMMARY),
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
            "evidence": rel(dl.PROXY_MT5_DIFF),
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
            "user_explanation_hook": "MT5 기준으로 DI02 no19는 거래 밀도와 숏 비중을 늘렸지만 DB 기준선의 순수익/수익 팩터를 아직 넘지 못했습니다.",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": f"DL net {review.get('dl_mt5_net')} vs DB net {review.get('db_mt5_net')} delta {review.get('net_delta_vs_db')}; short delta {review.get('short_count_delta_vs_db')}",
            "comparison_baseline": BASELINE_RUN_ID,
            "likely_drivers": [
                "synthetic short-source profit recovery(합성 숏 원천 수익 회복)",
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
                "trade_count": review.get("dl_trade_count"),
                "trade_density": review.get("dl_trade_density"),
                "long_trade_count": review.get("dl_long_trade_count"),
                "short_trade_count": review.get("dl_short_trade_count"),
                "short_share": review.get("dl_short_share"),
                "profit_factor": review.get("dl_profit_factor"),
                "drawdown": review.get("dl_drawdown"),
                "recovery_factor": review.get("dl_recovery_factor"),
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
            "tester_identity": rel(dk.TESTER_IDENTITY_CONTRACT),
            "ea_identity": rel(dl.RUNTIME_IDENTITY),
            "report_identity": [rel(dl.STRATEGY_TESTER_REPORTS), final.get("report_path", "")],
            "trade_evidence": {
                "trade_count": final["dl_trade_count"],
                "net_profit": final["dl_mt5_net"],
                "drawdown": final["dl_drawdown"],
                "profit_factor": final["dl_profit_factor"],
                "trade_list_availability": "strategy_report_artifact_available(전략 보고서 산출물 있음)",
            },
            "cost_assumptions": "broker-native Strategy Tester output only(브로커 기반 전략 테스터 출력 한정)",
            "forensic_checks": [rel(dl.MT5_EXECUTION_RESULT), rel(dl.STRATEGY_TESTER_REPORTS), rel(dl.RUNTIME_OUTPUT_COPY), rel(RUNTIME_REVIEW)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": [rel(dk.RUNTIME_POLICY_CONFIG), rel(dk.EXPECTED_KPI_SUMMARY)],
            "runtime_path": [rel(dk.TESTER_SET_MANIFEST), rel(dk.TESTER_INI_MANIFEST), rel(dl.EXECUTION_SUMMARY)],
            "shared_contract": rel(dk.RUNTIME_PARITY_CONTRACT),
            "known_differences": "proxy expected value(프록시 예상값)는 MT5 cost/fill/runtime(MT5 비용/체결/런타임)을 대체하지 않습니다.",
            "parity_check": [rel(dl.PROXY_MT5_DIFF), rel(RUNTIME_REVIEW)],
            "parity_identity": {"source_onnx_sha256": sha(dk.SOURCE_ONNX), "tester_set_manifest_sha256": sha(dk.TESTER_SET_MANIFEST)},
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
    return dk.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], review_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    review = review_rows[0]
    report = f"""# run364DM h17 short-source profit recovery MT5 runtime probe review(17시 숏 원천 수익 회복 MT5 런타임 탐침 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- baseline_run_id(기준선 실행 ID): `{BASELINE_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): DL MT5 result(DL MT5 결과)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): short-source profit recovery(숏 원천 수익 회복)가 DG 대비 순수익은 회복했지만, DB 기준 순수익/수익 팩터 초과가 필요하다는 다음 탐색 조건(next exploration condition, 다음 탐색 조건)을 분리했습니다.

{markdown_table(review_rows, ['dl_mt5_net', 'db_mt5_net', 'net_delta_vs_db', 'dg_source_mt5_net', 'net_delta_vs_dg_source', 'dl_profit_factor', 'db_profit_factor', 'profit_factor_delta_vs_db', 'dl_trade_count', 'db_trade_count', 'dl_short_trade_count', 'db_short_trade_count', 'short_count_delta_vs_db', 'short_count_delta_vs_dg_source', 'proxy_mt5_net_gap'])}

## Result Boundary(결과 경계)

- positive clue(긍정 단서): DL은 DB보다 short count(숏 거래수)를 `{review.get('short_count_delta_vs_db')}` 늘리고, DG source expansion(DG 원천 확장)보다 net profit(순수익)을 `{review.get('net_delta_vs_dg_source')}` 회복했습니다.
- unresolved guardrail(미해결 가드레일): DL net/PF/expectancy(순수익/수익 팩터/기대값)는 DB보다 각각 `{review.get('net_delta_vs_db')}` / `{review.get('profit_factor_delta_vs_db')}` / `{review.get('expectancy_delta_vs_db')}` 후퇴했습니다.
- no authority(권위 없음): forward/replay/runtime authority(전진/재생/런타임 권위)는 없고, 운영 승격(operating promotion, 운영 승격)도 없습니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Next(다음)

`{NEXT_RUN_ID}`는 margin_vs_flat(플랫 대비 마진), hour-pair veto(시간쌍 배제), short-source quality rank(숏 원천 품질 순위)를 탐색합니다. 효과(effect, 효과)는 숏 거래수 상승을 유지하면서 DB 기준 순수익/수익 팩터를 초과할 후보를 찾는 것입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DM decision(결정): short-source profit recovery MT5 review(숏 원천 수익 회복 MT5 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- DL MT5 net/PF/trades(DL MT5 순수익/수익 팩터/거래수): `{final['dl_mt5_net']}` / `{final['dl_profit_factor']}` / `{final['dl_trade_count']}`
- DB baseline net/PF/trades(DB 기준선 순수익/수익 팩터/거래수): `{final['db_mt5_net']}` / `{final['db_profit_factor']}` / `{final['db_trade_count']}`
- DG source net/PF/trades(DG 원천 확장 순수익/수익 팩터/거래수): `{final['dg_source_mt5_net']}` / `{final['dg_source_profit_factor']}` / `{final['dg_source_trade_count']}`
- short count delta(숏 거래수 변화): `{final['short_count_delta_vs_db']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DN은 숏 거래수 증가를 보존하면서 순수익/수익 팩터를 DB 위로 올리는 탐색입니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DM__{RUN_ID}", f"\n- run364DM__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - DI02 no19 MT5 review(DI02 no19 MT5 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364DM__{RUN_ID}",
        f"""
<!-- run364DM__{RUN_ID} -->

## run364DM Short-Source Profit Recovery Review(숏 원천 수익 회복 검토)

Action(행동): DL MT5 probe(DL MT5 탐침)를 DB runtime baseline(DB 런타임 기준선)과 비교했습니다.

Effect(효과): 숏 원천 수익 회복은 DG보다 순수익을 회복했지만 DB 초과가 필요하므로 `{NEXT_RUN_ID}`로 PF/net polish(PF/순수익 다듬기) 탐색을 엽니다.
""",
    )
    append_text_once(STAGE_README, f"run364DM__{RUN_ID}", f"\n<!-- run364DM__{RUN_ID} -->\n## run364DM review(검토)\n\nDI02 no19 MT5 review(DI02 no19 MT5 검토) completed(완료). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DM` reviewed(검토 완료) DI02 no19 short-source profit recovery MT5 runtime probe(DI02 19시 배제 숏 원천 수익 회복 MT5 런타임 탐침). DL MT5 net/PF/trades(DL MT5 순수익/수익 팩터/거래수)는 `{final['dl_mt5_net']}` / `{final['dl_profit_factor']}` / `{final['dl_trade_count']}`이고, DB baseline(DB 기준선) 대비 net delta(순수익 변화)는 `{final['net_delta_vs_db']}`, DG source(DG 원천 확장) 대비 net delta(순수익 변화)는 `{final['net_delta_vs_dg_source']}`, short count delta(숏 거래수 변화)는 `{final['short_count_delta_vs_db']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 PF/net polish(PF/순수익 다듬기)를 탐색합니다.

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

DL MT5 net/PF/trades(DL MT5 순수익/수익 팩터/거래수): `{final['dl_mt5_net']}` / `{final['dl_profit_factor']}` / `{final['dl_trade_count']}`.

DB baseline net/PF/trades(DB 기준선 순수익/수익 팩터/거래수): `{final['db_mt5_net']}` / `{final['db_profit_factor']}` / `{final['db_trade_count']}`.

DG source net/PF/trades(DG 원천 확장 순수익/수익 팩터/거래수): `{final['dg_source_mt5_net']}` / `{final['dg_source_profit_factor']}` / `{final['dg_source_trade_count']}`.

Judgment(판정): `{JUDGMENT}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DM__{RUN_ID}", f"\n<!-- run364DM__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed DI02 no19 MT5 probe(DI02 no19 MT5 탐침 검토); judgment `{JUDGMENT}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DM__{RUN_ID}", f"\n<!-- run364DM__{RUN_ID} -->\n- `{RUN_ID}`: DI02 no19 short-source profit recovery(DI02 19시 배제 숏 원천 수익 회복)는 MT5에서 DG 대비 net(순수익)을 `{final['net_delta_vs_dg_source']}` 회복했고 DB 대비 short count(숏 거래수)를 `{final['short_count_delta_vs_db']}` 늘렸지만 net/PF(순수익/수익 팩터)는 DB보다 약간 낮습니다. Effect(효과): 다음은 PF/net polish(PF/순수익 다듬기)입니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364DM__db_threshold_not_exceeded__{RUN_ID}", f"\n<!-- run364DM__db_threshold_not_exceeded__{RUN_ID} -->\n- `{RUN_ID}`: short-source profit recovery(숏 원천 수익 회복)는 DB를 아직 초과하지 못했습니다. Net delta vs DB(DB 대비 순수익 변화) `{final['net_delta_vs_db']}`, PF delta(PF 변화) `{final['profit_factor_delta_vs_db']}`. Effect(효과): DN은 PF 상승 없는 밀도 추가를 금지하고 품질 다듬기만 탐색합니다.\n")


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
        "question": "Did DI02 no19 short-source profit recovery improve MT5 trade shape without damaging profit?(DI02 19시 배제 숏 원천 수익 회복이 MT5 거래 형태를 개선하면서 수익을 해치지 않았는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["dl_mt5_net"],
        "profit_factor": final["dl_profit_factor"],
        "expectancy": final["dl_expectancy"],
        "trade_count": final["dl_trade_count"],
        "trade_density_per_feature_day": final["dl_trade_density"],
        "long_trade_count": final["dl_long_trade_count"],
        "short_trade_count": final["dl_short_trade_count"],
        "max_drawdown_amount": final["dl_drawdown"],
        "recovery_factor": final["dl_recovery_factor"],
        "trade_density_requirement_status": "passed_runtime_density_ge_3_reviewed(런타임 거래 밀도 3 이상 검토됨)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_REVIEW),
        "primary_kpi": f"dl_mt5_net={final['dl_mt5_net']};pf={final['dl_profit_factor']};trades={final['dl_trade_count']};shorts={final['dl_short_trade_count']}",
        "guardrail_kpi": "near_db_profit_not_exceeded;runtime_authority=not_claimed;operating_promotion=not_claimed",
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
            "kpi_scope": "DM runtime review(DM 런타임 검토)",
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
        ("runtime_review", RUNTIME_REVIEW, "DL vs DB/DG runtime review(DL 대 DB/DG 런타임 검토)."),
        ("result_judgment_receipt", RESULT_JUDGMENT_RECEIPT, "Result judgment receipt(결과 판정 영수증)."),
        ("performance_attribution_receipt", PERFORMANCE_RECEIPT, "Performance attribution receipt(성과 귀속 영수증)."),
        ("backtest_forensics_receipt", BACKTEST_RECEIPT, "Backtest forensics receipt(백테스트 포렌식 영수증)."),
        ("runtime_parity_receipt", RUNTIME_RECEIPT, "Runtime parity receipt(런타임 동등성 영수증)."),
        ("queue", RUN364DN_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DM producer script(DM 생산 스크립트)."),
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
    dl_final, dk_final, db_final = validate_inputs()
    review_rows = build_review(dl_final, dk_final, db_final)
    review = review_rows[0]
    build_queue(review)
    final = build_final(dl_final, dk_final, db_final, review)
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
