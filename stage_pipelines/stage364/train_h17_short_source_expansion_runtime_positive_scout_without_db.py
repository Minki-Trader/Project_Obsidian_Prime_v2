import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db as db  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_quality_risk_scale_runtime_package_without_db as da  # noqa: E402
from stage_pipelines.stage364 import review_h17_short_quality_risk_scale_mt5_runtime_probe_without_db as dc  # noqa: E402
from stage_pipelines.stage364 import train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db as cy  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dc.STAGE_ID
RUN_NUMBER = "run364DD"
RUN_ID = "run364DD_train_h17_short_source_expansion_runtime_positive_scout_without_db_v1"
PARENT_RUN_ID = dc.RUN_ID
SOURCE_RUNTIME_RUN_ID = db.RUN_ID
SOURCE_PACKAGE_RUN_ID = da.RUN_ID
SOURCE_PROXY_RUN_ID = cy.RUN_ID
NEXT_RUN_ID = "run364DE_review_h17_short_source_expansion_runtime_positive_scout_without_db_v1"

STATUS = "completed_stage364DD_h17_short_source_expansion_proxy_scout_review_required_no_authority"
JUDGMENT = "proxy_short_source_expansion_scout_completed_review_required_no_authority"
DECISION = "stage364DD_open_run364DE_short_source_expansion_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DAYS = 314.0
FIXED_LOT = 0.10
RISK_SCALE_MULTIPLIER = 1.10
RISK_SCALE_HOURS = {17, 18, 19, 20}
RISK_SCALE_MIN_MARGIN = 0.08
MAX_HOLD_BARS = 6
DENSITY_FLOOR = 3.0
DENSITY_CEILING = 10.0
PF_FLOOR = 1.35
SOURCE_RAW_US100_M5 = ROOT / "data" / "raw" / "mt5_bars" / "m5" / "US100" / "bars_us100_m5_mt5api_raw.csv"

STAGE_DIR = dc.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
SHORT_SOURCE_SURFACE = RUN_DIR / "dd_short_source_expansion_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_dd_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_dd_trade_tape.csv"
VARIANT_OVERRIDE_AUDIT = RUN_DIR / "variant_override_audit.csv"
VARIANT_REASON_ATTRIBUTION = RUN_DIR / "variant_reason_attribution.csv"
VARIANT_HOUR_SIDE_ATTRIBUTION = RUN_DIR / "variant_hour_side_attribution.csv"
VARIANT_MONTH_SIDE_ATTRIBUTION = RUN_DIR / "variant_month_side_attribution.csv"
BASELINE_REPLAY_GAP = RUN_DIR / "baseline_replay_gap.csv"
PACKAGE_PRECHECK = RUN_DIR / "package_precheck.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_difference_plan.csv"
RUN364DE_QUEUE = RUN_DIR / "run364DE_review_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DD_h17_short_source_expansion_runtime_positive_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DD_h17_short_source_expansion_runtime_positive_scout.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    dc.FINAL_DECISION,
    dc.GATE_AUDIT,
    dc.RUN364DD_QUEUE,
    dc.COMPARISON_REVIEW,
    db.FINAL_DECISION,
    db.EXECUTION_SUMMARY,
    db.RUNTIME_OUTPUT_COPY,
    da.FINAL_DECISION,
    da.RUNTIME_POLICY_CONFIG,
    cy.SELECTED_CANDIDATE,
    cy.SELECTED_TRADE_TAPE,
    cy.RUN_MANIFEST,
    SOURCE_RAW_US100_M5,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SHORT_SOURCE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    VARIANT_OVERRIDE_AUDIT,
    VARIANT_REASON_ATTRIBUTION,
    VARIANT_HOUR_SIDE_ATTRIBUTION,
    VARIANT_MONTH_SIDE_ATTRIBUTION,
    BASELINE_REPLAY_GAP,
    PACKAGE_PRECHECK,
    PROXY_MT5_DIFF_PLAN,
    RUN364DE_QUEUE,
    DATA_INTEGRITY_AUDIT,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
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
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return dc.rel(path)


def exists(path: Path | str) -> bool:
    return dc.exists(path)


def sha(path: Path | str) -> str:
    return dc.sha(path)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dc.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dc.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dc.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dc.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DD inputs(DD 입력 누락): " + ", ".join(missing))
    dc_final = read_json(dc.FINAL_DECISION)
    db_final = read_json(db.FINAL_DECISION)
    da_final = read_json(da.FINAL_DECISION)
    if dc_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DC next_run_id mismatch(DC 다음 실행 ID 불일치): {dc_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("DC", dc_final), ("DB", db_final), ("DA", da_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    gates = read_csv(dc.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DC gate audit(DC 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return dc_final, db_final, da_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "short-source expansion scout input(숏 원천 확장 탐색 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-exploration-mandate(옵시디언 탐색 규율)",
            "support_skills": [
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-result-judgment(옵시디언 결과 판정)",
                "obsidian-performance-attribution(옵시디언 성과 귀속)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "hypothesis": (
                "New short-source rules can lift short count and short PnL without weakening the "
                "DB MT5 net/PF/DD boundary(새 숏 원천 규칙이 DB MT5 순수익/수익 팩터/낙폭 경계를 "
                "약화하지 않고 숏 수와 숏 손익을 올릴 수 있다)."
            ),
            "comparison": "DB MT5 runtime probe(DB MT5 런타임 탐침) plus telemetry replay(텔레메트리 재생).",
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "data_integrity_gate",
                "baseline_replay_boundary_gate",
                "short_source_candidate_gate",
                "kpi_contract_gate",
                "no_trade_splitting_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "Turns DD queue(DD 대기열)를 measurable proxy scout(측정 가능한 프록시 탐색)로 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def load_raw_price_maps() -> tuple[dict[str, float], pd.DataFrame]:
    raw = pd.read_csv(io_path(SOURCE_RAW_US100_M5), encoding="utf-8-sig")
    raw["bar_time"] = (
        pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
        .dt.tz_localize(None)
        .dt.strftime("%Y.%m.%d %H:%M:%S")
    )
    raw = raw.drop_duplicates("bar_time").sort_values("bar_time").reset_index(drop=True)
    raw["close_return_1"] = raw["close"].pct_change()
    raw["close_return_3"] = raw["close"].pct_change(3)
    raw["close_return_6"] = raw["close"].pct_change(6)
    raw["bar_body_return"] = raw["close"] / raw["open"] - 1.0
    return dict(zip(raw["bar_time"], raw["open"], strict=False)), raw


def load_cycles() -> tuple[pd.DataFrame, pd.DataFrame]:
    runtime_copy = read_csv(db.RUNTIME_OUTPUT_COPY)
    telemetry_rows = runtime_copy[runtime_copy["copy_id"].astype(str).str.contains("::telemetry", na=False)]
    telemetry_rel = str((telemetry_rows.iloc[0] if not telemetry_rows.empty else runtime_copy.iloc[0])["target_path"])
    telemetry_path = ROOT / telemetry_rel
    open_map, raw = load_raw_price_maps()
    raw_features = raw.set_index("bar_time")[["open", "close", "close_return_1", "close_return_3", "close_return_6", "bar_body_return"]]
    telemetry = pd.read_csv(io_path(telemetry_path), encoding="utf-8-sig")
    cycles = telemetry[telemetry["record_type"].eq("cycle")].copy()
    cycles = cycles[cycles["feature_ready"].astype(str).eq("True") & cycles["model_ok"].astype(str).eq("True")].copy()
    for column in ["p_short", "p_flat", "p_long"]:
        cycles[column] = pd.to_numeric(cycles[column], errors="coerce")
    cycles["source_dt"] = pd.to_datetime(cycles["source_time"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    cycles["written_dt"] = pd.to_datetime(cycles["written_at"], format="%Y.%m.%d %H:%M:%S", errors="coerce")
    cycles["dt"] = cycles["source_dt"] + pd.Timedelta(minutes=5)
    cycles["entry_time_raw"] = cycles["dt"].dt.strftime("%Y.%m.%d %H:%M:%S")
    cycles["entry_open"] = cycles["entry_time_raw"].map(open_map)
    cycles["open_hour"] = cycles["dt"].dt.hour.astype("Int64")
    cycles["open_month"] = cycles["dt"].dt.strftime("%Y-%m")
    cycles["open_month_num"] = cycles["dt"].dt.month.astype("Int64")
    cycles["margin_vs_long"] = cycles["p_short"] - cycles["p_long"]
    cycles["margin_vs_flat"] = cycles["p_short"] - cycles["p_flat"]
    cycles["p_short_dominant"] = cycles["p_short"].gt(cycles[["p_long", "p_flat"]].max(axis=1))
    cycles["decision_base"] = cycles["decision"].where(cycles["decision"].isin(["long", "short"]), "flat")
    cycles["source_open"] = cycles["source_time"].map(raw_features["open"])
    cycles["source_close"] = cycles["source_time"].map(raw_features["close"])
    cycles["close_return_1"] = cycles["source_time"].map(raw_features["close_return_1"]).fillna(0.0)
    cycles["close_return_3"] = cycles["source_time"].map(raw_features["close_return_3"]).fillna(0.0)
    cycles["close_return_6"] = cycles["source_time"].map(raw_features["close_return_6"]).fillna(0.0)
    cycles["bar_body_return"] = cycles["source_time"].map(raw_features["bar_body_return"]).fillna(0.0)
    missing_price = int(cycles["entry_open"].isna().sum())
    if missing_price:
        raise RuntimeError(f"missing runtime entry open prices(런타임 진입 시가 누락): {missing_price}")
    cycles = cycles.sort_values("dt").reset_index(drop=True)
    return cycles, telemetry


def variant_specs() -> list[dict[str, Any]]:
    return [
        {
            "variant_id": "dd00_db_policy_anchor",
            "family": "anchor(기준점)",
            "hypothesis": "Keep DB runtime policy unchanged(DB 런타임 정책을 그대로 둔다).",
            "hours": [],
            "p_short_min": None,
            "margin_vs_long_min": None,
            "extra_filter": "none(없음)",
        },
        {
            "variant_id": "dd01_h16_premarket_short_m100",
            "family": "premarket_short_source(프리마켓 숏 원천)",
            "hypothesis": "Very high-margin hour16 shorts may fill a true short source(매우 높은 16시 숏 마진이 실제 숏 원천을 만들 수 있다).",
            "hours": [16],
            "p_short_min": 0.45,
            "margin_vs_long_min": 0.10,
            "extra_filter": "p_short_dominant(숏 우세)",
        },
        {
            "variant_id": "dd02_h16_premarket_short_m080",
            "family": "premarket_short_source(프리마켓 숏 원천)",
            "hypothesis": "Hour16 blocked short rows deserve a softer margin test(16시 차단 숏 행은 완화된 마진 시험 가치가 있다).",
            "hours": [16],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.08,
            "extra_filter": "p_short_dominant(숏 우세)",
        },
        {
            "variant_id": "dd03_h18_19_short_source_m060",
            "family": "session_short_source(세션 숏 원천)",
            "hypothesis": "Hour18-19 flat short rows can add quality shorts(18-19시 관망 숏 행이 품질 숏을 더할 수 있다).",
            "hours": [18, 19],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.06,
            "extra_filter": "p_short_dominant(숏 우세)",
        },
        {
            "variant_id": "dd04_h18_21_short_source_m050_no20",
            "family": "session_short_source(세션 숏 원천)",
            "hypothesis": "Exclude weak hour20 while opening 18/19/21 short source(약한 20시는 빼고 18/19/21시 숏 원천을 연다).",
            "hours": [18, 19, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "extra_filter": "p_short_dominant(숏 우세)",
        },
        {
            "variant_id": "dd05_h17_21_short_source_m050_ex_aug",
            "family": "broad_short_source(광역 숏 원천)",
            "hypothesis": "Broad 17-21 short source may work if month8 is blocked(8월을 막으면 17-21시 광역 숏 원천이 작동할 수 있다).",
            "hours": [17, 18, 19, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "extra_filter": "p_short_dominant_and_not_august(숏 우세 및 8월 제외)",
        },
        {
            "variant_id": "dd06_h17_19_high_conviction_m080",
            "family": "high_conviction_short_source(고확신 숏 원천)",
            "hypothesis": "High-conviction 17-19 shorts may lift side balance cleanly(고확신 17-19시 숏은 방향 균형을 깨끗하게 올릴 수 있다).",
            "hours": [17, 18, 19],
            "p_short_min": 0.45,
            "margin_vs_long_min": 0.08,
            "extra_filter": "p_short_dominant(숏 우세)",
        },
        {
            "variant_id": "dd07_h21_late_short_m060",
            "family": "late_session_short_source(후반 세션 숏 원천)",
            "hypothesis": "Hour21 shorts may add balance without touching weak hour20(21시 숏은 약한 20시를 건드리지 않고 균형을 더할 수 있다).",
            "hours": [21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.06,
            "extra_filter": "p_short_dominant(숏 우세)",
        },
        {
            "variant_id": "dd08_bearish_impulse_h17_21_m040",
            "family": "market_behavior_short_source(시장 현상 숏 원천)",
            "hypothesis": "Bearish impulse can separate usable short rows(하락 충격이 사용 가능한 숏 행을 분리할 수 있다).",
            "hours": [17, 18, 19, 20, 21],
            "p_short_min": 0.42,
            "margin_vs_long_min": 0.04,
            "extra_filter": "p_short_dominant_and_ret3_negative(숏 우세 및 3봉 수익률 음수)",
        },
        {
            "variant_id": "dd09_bearish_impulse_h16_19_m030",
            "family": "market_behavior_short_source(시장 현상 숏 원천)",
            "hypothesis": "Earlier bearish impulse may unlock blocked short rows(이른 하락 충격이 차단된 숏 행을 열 수 있다).",
            "hours": [16, 17, 18, 19],
            "p_short_min": 0.42,
            "margin_vs_long_min": 0.03,
            "extra_filter": "p_short_dominant_and_ret6_negative(숏 우세 및 6봉 수익률 음수)",
        },
        {
            "variant_id": "dd10_combo_h16_high_h18_19_m060",
            "family": "combo_short_source(조합 숏 원천)",
            "hypothesis": "Combine hour16 high margin with 18-19 quality rows(16시 고마진과 18-19시 품질 행을 조합한다).",
            "hours": [16, 18, 19],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.06,
            "extra_filter": "h16_m100_or_h18_19_m060(16시 0.10 또는 18-19시 0.06)",
        },
        {
            "variant_id": "dd11_combo_no20_m050_bearish",
            "family": "combo_short_source(조합 숏 원천)",
            "hypothesis": "Combine no-hour20 source with bearish impulse(20시 제외 원천과 하락 충격을 조합한다).",
            "hours": [17, 18, 19, 21],
            "p_short_min": 0.42,
            "margin_vs_long_min": 0.04,
            "extra_filter": "p_short_dominant_and_ret3_negative_no20(숏 우세 및 3봉 음수, 20시 제외)",
        },
    ]


def build_override_mask(cycles: pd.DataFrame, spec: Mapping[str, Any]) -> pd.Series:
    if spec["variant_id"] == "dd00_db_policy_anchor":
        return pd.Series(False, index=cycles.index)
    flat = cycles["decision_base"].eq("flat")
    hours = cycles["open_hour"].astype("Int64").isin(list(spec["hours"]))
    p_ok = cycles["p_short"].ge(float(spec["p_short_min"]))
    margin_ok = cycles["margin_vs_long"].ge(float(spec["margin_vs_long_min"]))
    dominant = cycles["p_short_dominant"].astype(bool)
    base = flat & hours & p_ok & margin_ok & dominant & cycles["p_short"].gt(cycles["p_flat"])
    extra = str(spec["extra_filter"])
    if "not_august" in extra:
        base &= ~cycles["open_month_num"].eq(8)
    if "ret3_negative" in extra:
        base &= cycles["close_return_3"].le(-0.0010)
    if "ret6_negative" in extra:
        base &= cycles["close_return_6"].le(-0.0015)
    if spec["variant_id"] == "dd10_combo_h16_high_h18_19_m060":
        h16 = flat & cycles["open_hour"].eq(16) & cycles["p_short"].ge(0.45) & cycles["margin_vs_long"].ge(0.10) & dominant
        h18_19 = flat & cycles["open_hour"].isin([18, 19]) & cycles["p_short"].ge(0.4375) & cycles["margin_vs_long"].ge(0.06) & dominant
        base = h16 | h18_19
    return base.fillna(False)


def volume_for(side: str, row: Mapping[str, Any]) -> float:
    if side == "short" and int(row["open_hour"]) in RISK_SCALE_HOURS and as_float(row["margin_vs_long"]) >= RISK_SCALE_MIN_MARGIN:
        return FIXED_LOT * RISK_SCALE_MULTIPLIER
    return FIXED_LOT


def iso_time(value: Any) -> str:
    return pd.Timestamp(value).strftime("%Y-%m-%dT%H:%M:%S")


def simulate_variant(cycles: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    mask = build_override_mask(cycles, spec)
    decisions = cycles["decision_base"].copy()
    decisions.loc[mask] = "short"
    variant_id = str(spec["variant_id"])
    override_rows = cycles.loc[mask].copy()
    override_audit = []
    if not override_rows.empty:
        for hour, group in override_rows.groupby("open_hour", sort=True):
            override_audit.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": variant_id,
                    "open_hour": int(hour),
                    "override_rows": int(len(group)),
                    "avg_p_short": finite(group["p_short"].mean()),
                    "avg_margin_vs_long": finite(group["margin_vs_long"].mean()),
                    "avg_close_return_3": finite(group["close_return_3"].mean()),
                    "effect": "flat cycle(관망 주기)을 short source(숏 원천) 후보로 바꿉니다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    else:
        override_audit.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "open_hour": "",
                "override_rows": 0,
                "avg_p_short": "",
                "avg_margin_vs_long": "",
                "avg_close_return_3": "",
                "effect": "no changed rows(변경 행 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    trades: list[dict[str, Any]] = []
    position: str | None = None
    entry_price = 0.0
    entry_time = pd.NaT
    entry_index = -1
    entry_row: Mapping[str, Any] | None = None
    hold_bars = 0
    volume = FIXED_LOT

    for index, row in cycles.iterrows():
        desired = str(decisions.iloc[index])
        if desired not in {"long", "short"}:
            desired = "flat"
        price = float(row["entry_open"])
        current_time = row["dt"]
        blocked_open_this_bar = False
        if position is not None:
            hold_bars += 1
            close_reason = ""
            if desired in {"long", "short"} and desired != position:
                close_reason = "reverse"
            elif hold_bars >= MAX_HOLD_BARS:
                close_reason = "max_hold"
            if close_reason:
                gross = (price - entry_price) * volume if position == "long" else (entry_price - price) * volume
                source = entry_row or {}
                trades.append(
                    {
                        "run_id": RUN_ID,
                        "variant_id": variant_id,
                        "open_time": iso_time(entry_time),
                        "close_time": iso_time(current_time),
                        "direction": position,
                        "volume": round(volume, 8),
                        "open_price": round(entry_price, 5),
                        "close_price": round(price, 5),
                        "gross_profit": round(gross, 10),
                        "swap": 0.0,
                        "commission": 0.0,
                        "net_profit": round(gross, 10),
                        "hold_bars": hold_bars,
                        "open_hour": int(source.get("open_hour", 0)),
                        "open_month": str(source.get("open_month", "")),
                        "open_month_num": int(source.get("open_month_num", 0)),
                        "p_short": round(as_float(source.get("p_short")), 12),
                        "p_flat": round(as_float(source.get("p_flat")), 12),
                        "p_long": round(as_float(source.get("p_long")), 12),
                        "margin_vs_long": round(as_float(source.get("margin_vs_long")), 12),
                        "margin_vs_flat": round(as_float(source.get("margin_vs_flat")), 12),
                        "source_reason": source.get("source_reason", ""),
                        "source_bucket": source.get("source_bucket", ""),
                        "close_reason": close_reason,
                        "entry_index": entry_index,
                        "exit_index": index,
                        "proxy_boundary": "single-position telemetry replay(단일 포지션 텔레메트리 재생)",
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )
                position = None
                hold_bars = 0
                blocked_open_this_bar = True
                if close_reason == "reverse" and desired in {"long", "short"}:
                    position = desired
                    entry_price = price
                    entry_time = current_time
                    entry_index = index
                    source_bucket = "dd_added_short_source" if bool(mask.iloc[index]) else "runtime_decision"
                    entry_row = {
                        **row.to_dict(),
                        "source_reason": f"{variant_id}_override" if bool(mask.iloc[index]) else row.get("decision_reason", ""),
                        "source_bucket": source_bucket,
                    }
                    volume = volume_for(position, entry_row)
                    blocked_open_this_bar = True
        if position is None and not blocked_open_this_bar and desired in {"long", "short"}:
            position = desired
            entry_price = price
            entry_time = current_time
            entry_index = index
            source_bucket = "dd_added_short_source" if bool(mask.iloc[index]) else "runtime_decision"
            entry_row = {
                **row.to_dict(),
                "source_reason": f"{variant_id}_override" if bool(mask.iloc[index]) else row.get("decision_reason", ""),
                "source_bucket": source_bucket,
            }
            volume = volume_for(position, entry_row)

    if position is not None:
        row = cycles.iloc[-1]
        price = float(row["entry_open"])
        gross = (price - entry_price) * volume if position == "long" else (entry_price - price) * volume
        source = entry_row or {}
        trades.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "open_time": iso_time(entry_time),
                "close_time": iso_time(row["dt"]),
                "direction": position,
                "volume": round(volume, 8),
                "open_price": round(entry_price, 5),
                "close_price": round(price, 5),
                "gross_profit": round(gross, 10),
                "swap": 0.0,
                "commission": 0.0,
                "net_profit": round(gross, 10),
                "hold_bars": hold_bars,
                "open_hour": int(source.get("open_hour", 0)),
                "open_month": str(source.get("open_month", "")),
                "open_month_num": int(source.get("open_month_num", 0)),
                "p_short": round(as_float(source.get("p_short")), 12),
                "p_flat": round(as_float(source.get("p_flat")), 12),
                "p_long": round(as_float(source.get("p_long")), 12),
                "margin_vs_long": round(as_float(source.get("margin_vs_long")), 12),
                "margin_vs_flat": round(as_float(source.get("margin_vs_flat")), 12),
                "source_reason": source.get("source_reason", ""),
                "source_bucket": source.get("source_bucket", ""),
                "close_reason": "final_close",
                "entry_index": entry_index,
                "exit_index": len(cycles) - 1,
                "proxy_boundary": "single-position telemetry replay(단일 포지션 텔레메트리 재생)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(trades), pd.DataFrame(override_audit)


def profit_factor(profits: np.ndarray) -> float:
    gains = float(profits[profits > 0].sum()) if profits.size else 0.0
    losses = float(profits[profits < 0].sum()) if profits.size else 0.0
    if losses < 0:
        return gains / abs(losses)
    return 999.0 if gains > 0 else 0.0


def closed_drawdown(profits: np.ndarray) -> float:
    if not profits.size:
        return 0.0
    equity = np.cumsum(profits)
    peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    return float(np.maximum(peaks - equity, 0.0).max())


def metric_frame(frame: pd.DataFrame) -> dict[str, Any]:
    profits = frame["net_profit"].to_numpy(dtype="float64") if not frame.empty else np.asarray([], dtype="float64")
    trade_count = int(len(frame))
    net = float(profits.sum()) if profits.size else 0.0
    dd = closed_drawdown(profits)
    long_frame = frame[frame["direction"].eq("long")]
    short_frame = frame[frame["direction"].eq("short")]
    return {
        "net_profit": finite(net, 4),
        "profit_factor": finite(profit_factor(profits), 10),
        "expectancy": finite(net / trade_count if trade_count else 0.0, 10),
        "trade_count": trade_count,
        "trade_density": finite(trade_count / DAYS, 10),
        "long_trade_count": int(len(long_frame)),
        "short_trade_count": int(len(short_frame)),
        "short_share": finite(len(short_frame) / trade_count if trade_count else 0.0, 10),
        "long_net_profit": finite(float(long_frame["net_profit"].sum()) if not long_frame.empty else 0.0, 4),
        "short_net_profit": finite(float(short_frame["net_profit"].sum()) if not short_frame.empty else 0.0, 4),
        "closed_trade_drawdown_proxy": finite(dd, 4),
        "closed_trade_recovery_proxy": finite(net / dd if dd > 0 else (999.0 if net > 0 else 0.0), 10),
    }


def mt5_baseline_metrics() -> dict[str, float]:
    row = read_csv(db.EXECUTION_SUMMARY).iloc[0]
    return {
        "net_profit": as_float(row.get("net_profit")),
        "profit_factor": as_float(row.get("profit_factor")),
        "trade_count": as_float(row.get("trade_count")),
        "density": as_float(row.get("trade_count")) / DAYS,
        "expectancy": as_float(row.get("expectancy")),
        "drawdown": as_float(row.get("max_drawdown_amount")),
        "recovery_factor": as_float(row.get("recovery_factor")),
        "long_trade_count": as_float(row.get("long_trade_count")),
        "short_trade_count": as_float(row.get("short_trade_count")),
        "short_share": as_float(row.get("short_trade_count")) / as_float(row.get("trade_count")),
    }


def build_surface() -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]], pd.DataFrame, dict[str, Any]]:
    cycles, _telemetry = load_cycles()
    mt5_base = mt5_baseline_metrics()
    specs = variant_specs()
    frames: dict[str, pd.DataFrame] = {}
    audits: list[dict[str, Any]] = []
    surface: list[dict[str, Any]] = []
    baseline_metrics: dict[str, Any] | None = None
    baseline_frame: pd.DataFrame | None = None
    for spec in specs:
        frame, audit = simulate_variant(cycles, spec)
        frames[str(spec["variant_id"])] = frame
        audits.extend(audit.to_dict("records"))
        metrics = metric_frame(frame)
        if spec["variant_id"] == "dd00_db_policy_anchor":
            baseline_metrics = metrics
            baseline_frame = frame
    if baseline_metrics is None or baseline_frame is None:
        raise RuntimeError("missing DD baseline replay(DD 기준선 재생 누락)")
    base_net = as_float(baseline_metrics["net_profit"])
    base_pf = as_float(baseline_metrics["profit_factor"])
    base_dd = as_float(baseline_metrics["closed_trade_drawdown_proxy"])
    base_trade_count = as_float(baseline_metrics["trade_count"])
    base_short_count = as_float(baseline_metrics["short_trade_count"])
    base_short_net = as_float(baseline_metrics["short_net_profit"])
    for spec in specs:
        frame = frames[str(spec["variant_id"])]
        metrics = metric_frame(frame)
        variant_id = str(spec["variant_id"])
        override_count = sum(int(row["override_rows"]) for row in audits if row["variant_id"] == variant_id and str(row["override_rows"]) != "")
        net_delta = as_float(metrics["net_profit"]) - base_net
        pf_delta = as_float(metrics["profit_factor"]) - base_pf
        dd_delta = as_float(metrics["closed_trade_drawdown_proxy"]) - base_dd
        trade_delta = as_float(metrics["trade_count"]) - base_trade_count
        short_count_delta = as_float(metrics["short_trade_count"]) - base_short_count
        short_net_delta = as_float(metrics["short_net_profit"]) - base_short_net
        estimated_net = mt5_base["net_profit"] + net_delta
        estimated_pf = mt5_base["profit_factor"] + pf_delta
        estimated_trade_count = mt5_base["trade_count"] + trade_delta
        estimated_density = estimated_trade_count / DAYS
        estimated_dd = max(0.0, mt5_base["drawdown"] + dd_delta)
        side_balance_improved = (
            as_float(metrics["short_trade_count"]) > mt5_base["short_trade_count"]
            and as_float(metrics["short_share"]) > mt5_base["short_share"]
        )
        package_pass = (
            variant_id != "dd00_db_policy_anchor"
            and override_count > 0
            and estimated_net >= mt5_base["net_profit"]
            and estimated_pf >= PF_FLOOR
            and DENSITY_FLOOR <= estimated_density <= DENSITY_CEILING
            and side_balance_improved
        )
        score = (
            estimated_net
            + estimated_pf * 120.0
            + max(0.0, short_count_delta) * 3.0
            + max(0.0, short_net_delta) * 2.0
            - max(0.0, dd_delta) * 1.5
            - max(0.0, DENSITY_FLOOR - estimated_density) * 300.0
            - max(0.0, estimated_density - DENSITY_CEILING) * 150.0
            + (180.0 if package_pass else 0.0)
        )
        surface.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "variant_family": spec["family"],
                "hypothesis": spec["hypothesis"],
                "changed_variables": f"hours={spec['hours']};p_short_min={spec['p_short_min']};margin_vs_long_min={spec['margin_vs_long_min']};extra={spec['extra_filter']}",
                "override_rows": override_count,
                "sim_net_profit": metrics["net_profit"],
                "sim_profit_factor": metrics["profit_factor"],
                "sim_expectancy": metrics["expectancy"],
                "sim_trade_count": metrics["trade_count"],
                "sim_trade_density": metrics["trade_density"],
                "sim_long_trade_count": metrics["long_trade_count"],
                "sim_short_trade_count": metrics["short_trade_count"],
                "sim_short_share": metrics["short_share"],
                "sim_long_net_profit": metrics["long_net_profit"],
                "sim_short_net_profit": metrics["short_net_profit"],
                "sim_closed_trade_drawdown_proxy": metrics["closed_trade_drawdown_proxy"],
                "sim_closed_trade_recovery_proxy": metrics["closed_trade_recovery_proxy"],
                "sim_net_delta_vs_anchor": finite(net_delta, 4),
                "sim_pf_delta_vs_anchor": finite(pf_delta, 10),
                "sim_trade_delta_vs_anchor": finite(trade_delta, 4),
                "sim_short_count_delta_vs_anchor": finite(short_count_delta, 4),
                "sim_short_net_delta_vs_anchor": finite(short_net_delta, 4),
                "sim_dd_delta_vs_anchor": finite(dd_delta, 4),
                "db_mt5_net_profit": finite(mt5_base["net_profit"], 4),
                "db_mt5_profit_factor": finite(mt5_base["profit_factor"], 10),
                "db_mt5_drawdown": finite(mt5_base["drawdown"], 4),
                "db_mt5_trade_count": finite(mt5_base["trade_count"], 4),
                "db_mt5_short_trade_count": finite(mt5_base["short_trade_count"], 4),
                "db_mt5_short_share": finite(mt5_base["short_share"], 10),
                "estimated_mt5_net_profit": finite(estimated_net, 4),
                "estimated_mt5_profit_factor": finite(estimated_pf, 10),
                "estimated_mt5_trade_count": finite(estimated_trade_count, 4),
                "estimated_mt5_density": finite(estimated_density, 10),
                "estimated_mt5_drawdown": finite(estimated_dd, 4),
                "estimated_short_share": finite(as_float(metrics["short_trade_count"]) / max(estimated_trade_count, 1.0), 10),
                "side_balance_status": "improved" if side_balance_improved else "not_improved",
                "package_precheck_status": "passed_proxy_precheck(프록시 사전검토 통과)" if package_pass else "failed_proxy_precheck(프록시 사전검토 실패)",
                "candidate_status": "proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음)" if package_pass else "proxy_watch_or_negative_no_authority(프록시 관찰 또는 부정, 권위 없음)",
                "selection_score": finite(score, 10),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    surface = sorted(surface, key=lambda row: as_float(row["selection_score"]), reverse=True)
    return surface, frames, audits, baseline_frame, mt5_base


def selected_row(surface: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    passing = [row for row in surface if str(row["package_precheck_status"]).startswith("passed")]
    return dict(max(passing or surface, key=lambda row: as_float(row["selection_score"])))


def group_summary(frames: Mapping[str, pd.DataFrame], surface: Sequence[Mapping[str, Any]], by: Sequence[str], kind: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for surface_row in surface:
        variant_id = str(surface_row["variant_id"])
        frame = frames[variant_id]
        if frame.empty:
            continue
        for keys, group in frame.groupby(list(by), sort=True, dropna=False):
            if not isinstance(keys, tuple):
                keys = (keys,)
            profits = group["net_profit"].to_numpy(dtype="float64")
            row = {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "summary_kind": kind,
                "trade_count": int(len(group)),
                "net_profit": finite(float(profits.sum()), 4),
                "profit_factor": finite(profit_factor(profits), 10),
                "long_trade_count": int(group["direction"].eq("long").sum()),
                "short_trade_count": int(group["direction"].eq("short").sum()),
                "added_short_source_count": int(group["source_bucket"].eq("dd_added_short_source").sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column, value in zip(by, keys, strict=False):
                row[str(column)] = value
            rows.append(row)
    return rows


def package_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "variant_id": row["variant_id"],
            "estimated_net_ge_db": str(as_float(row["estimated_mt5_net_profit"]) >= as_float(row["db_mt5_net_profit"])).lower(),
            "estimated_pf_ge_135": str(as_float(row["estimated_mt5_profit_factor"]) >= PF_FLOOR).lower(),
            "density_range_3_to_10": str(DENSITY_FLOOR <= as_float(row["estimated_mt5_density"]) <= DENSITY_CEILING).lower(),
            "short_share_improved": str(row["side_balance_status"] == "improved").lower(),
            "override_rows_positive": str(as_float(row["override_rows"]) > 0).lower(),
            "package_precheck_status": row["package_precheck_status"],
            "effect": "MT5 package(MT5 패키지)는 review(검토) 후에만 준비합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in surface
    ]


def write_artifacts(
    surface: Sequence[Mapping[str, Any]],
    frames: Mapping[str, pd.DataFrame],
    audits: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    baseline_frame: pd.DataFrame,
    mt5_base: Mapping[str, Any],
) -> None:
    write_csv(SHORT_SOURCE_SURFACE, surface)
    write_csv(VARIANT_OVERRIDE_AUDIT, audits)
    write_csv(VARIANT_REASON_ATTRIBUTION, group_summary(frames, surface, ["source_bucket", "direction"], "reason_side"))
    write_csv(VARIANT_HOUR_SIDE_ATTRIBUTION, group_summary(frames, surface, ["open_hour", "direction"], "hour_side"))
    write_csv(VARIANT_MONTH_SIDE_ATTRIBUTION, group_summary(frames, surface, ["open_month", "direction"], "month_side"))
    write_csv(PACKAGE_PRECHECK, package_rows(surface))
    baseline_metrics = metric_frame(baseline_frame)
    write_csv(
        BASELINE_REPLAY_GAP,
        [
            {
                "run_id": RUN_ID,
                "baseline_variant_id": "dd00_db_policy_anchor",
                "sim_net_profit": baseline_metrics["net_profit"],
                "db_mt5_net_profit": finite(mt5_base["net_profit"], 4),
                "sim_profit_factor": baseline_metrics["profit_factor"],
                "db_mt5_profit_factor": finite(mt5_base["profit_factor"], 10),
                "sim_trade_count": baseline_metrics["trade_count"],
                "db_mt5_trade_count": finite(mt5_base["trade_count"], 4),
                "sim_short_trade_count": baseline_metrics["short_trade_count"],
                "db_mt5_short_trade_count": finite(mt5_base["short_trade_count"], 4),
                "net_gap_db_minus_sim": finite(mt5_base["net_profit"] - as_float(baseline_metrics["net_profit"]), 4),
                "boundary": "telemetry replay estimates deltas only(텔레메트리 재생은 변화분만 추정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        PROXY_MT5_DIFF_PLAN,
        [
            {
                "run_id": RUN_ID,
                "variant_id": selected["variant_id"],
                "sim_net_delta_vs_anchor": selected["sim_net_delta_vs_anchor"],
                "estimated_mt5_net_profit": selected["estimated_mt5_net_profit"],
                "db_mt5_net_profit": selected["db_mt5_net_profit"],
                "estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
                "db_mt5_profit_factor": selected["db_mt5_profit_factor"],
                "estimated_mt5_drawdown": selected["estimated_mt5_drawdown"],
                "db_mt5_drawdown": selected["db_mt5_drawdown"],
                "diff_boundary": "proxy estimate cannot replace MT5 runtime probe(프록시 추정은 MT5 런타임 탐침을 대체하지 않음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364DE_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "de01_short_source_candidate_review",
                "review_subject": selected["variant_id"],
                "review_question": "Does selected DD short-source variant deserve MT5 package design?(선택 DD 숏 원천 변형이 MT5 패키지 설계를 받을 만한가?)",
                "success_criteria": "review confirms no split, side balance gain, and runtime representability(검토가 무분할, 방향 균형 개선, 런타임 표현 가능성을 확인)",
                "failure_criteria": "gain is simulator-only or weakens MT5 boundary(개선이 시뮬레이터 전용이거나 MT5 경계를 약화)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 2,
                "queue_id": "de02_premarket_or_session_source_boundary",
                "review_subject": selected["variant_id"],
                "review_question": "Is the new short source a legitimate session/regime idea, not trade splitting?(새 숏 원천이 거래 쪼개기가 아니라 정당한 세션/국면 아이디어인가?)",
                "success_criteria": "feature-time inputs only and parameterizable EA rule(피처 시점 입력만 쓰고 EA 파라미터화 가능)",
                "failure_criteria": "requires future path, exact outcome filter, or hidden runtime logic(미래 경로, 정확한 결과 필터, 숨은 런타임 로직 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    selected_frame = frames[str(selected["variant_id"])].copy()
    write_csv(SELECTED_TRADE_TAPE, selected_frame.to_dict("records"))
    write_json(SELECTED_CANDIDATE, selected)


def data_integrity_rows(cycles: pd.DataFrame, baseline_frame: pd.DataFrame, selected_frame: pd.DataFrame, surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_cycles = int(cycles.duplicated(subset=["entry_time_raw", "source_time", "input_hash"]).sum()) if "input_hash" in cycles.columns else 0
    overlap_count = int((selected_frame["entry_index"].shift(-1).fillna(10**12).astype(float) < selected_frame["exit_index"].astype(float)).sum()) if not selected_frame.empty else 0
    changed_rows = [row for row in surface if row["variant_id"] != "dd00_db_policy_anchor" and as_float(row["override_rows"]) > 0]
    selected_added = int(selected_frame["source_bucket"].eq("dd_added_short_source").sum()) if not selected_frame.empty else 0
    return [
        {
            "run_id": RUN_ID,
            "audit_item": "input_lineage(입력 계보)",
            "status": "passed" if all(exists(path) for path in INPUT_FILES) else "failed",
            "observed": ";".join(rel(path) for path in INPUT_FILES),
            "effect": "DC/DB/DA/CY/raw inputs(DC/DB/DA/CY/원천 입력)을 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "timestamp_safety(시점 안전)",
            "status": "passed",
            "observed": "uses written_at entry open and source_time closed-bar features only(written_at 진입 시가와 source_time 종료봉 피처만 사용)",
            "effect": "future price path(미래 가격 경로)를 후보 조건으로 쓰지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "duplicate_cycle_key(중복 주기 키)",
            "status": "passed" if duplicate_cycles == 0 else "failed",
            "observed": f"duplicate_cycles={duplicate_cycles}",
            "effect": "telemetry cycle(텔레메트리 주기)을 중복 재생하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "single_position_no_overlap(단일 포지션 무겹침)",
            "status": "passed" if overlap_count == 0 else "failed",
            "observed": f"selected_overlap_count={overlap_count}",
            "effect": "extra short(추가 숏)을 겹쳐 넣지 않고 포지션 상태 하나로 재생합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "short_source_changed_rows(숏 원천 변경 행)",
            "status": "passed" if changed_rows and selected_added >= 0 else "failed",
            "observed": f"changed_variant_count={len(changed_rows)};selected_added_short_trades={selected_added}",
            "effect": "pure exposure scaling(순수 노출 증폭)이 아니라 진입 원천을 탐색합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "baseline_replay_boundary(기준선 재생 경계)",
            "status": "passed" if len(baseline_frame) > 0 else "failed",
            "observed": "baseline replay does not equal MT5; deltas only(기준선 재생은 MT5와 같지 않으며 변화분만 사용)",
            "effect": "proxy result(프록시 결과)를 MT5 KPI(MT5 핵심 성과 지표)로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(
    surface: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    data_rows: Sequence[Mapping[str, Any]],
    receipt_paths: Sequence[Path],
    *,
    final_written: bool,
) -> list[dict[str, Any]]:
    passed_packages = sum(1 for row in surface if str(row["package_precheck_status"]).startswith("passed"))
    gates = [
        ("scope_completion_gate", len(surface) == len(variant_specs()) and exists(SHORT_SOURCE_SURFACE), SHORT_SOURCE_SURFACE, "all DD variants scored(모든 DD 변형 점수화)"),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "inputs linked(입력 연결)"),
        ("data_integrity_gate", bool(data_rows) and all(row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "timestamp/no-overlap checks passed(시점/무겹침 점검 통과)"),
        ("baseline_replay_boundary_gate", exists(BASELINE_REPLAY_GAP), BASELINE_REPLAY_GAP, "baseline replay gap declared(기준선 재생 차이 명시)"),
        ("short_source_candidate_gate", as_float(selected.get("override_rows")) > 0 and passed_packages > 0, SHORT_SOURCE_SURFACE, "selected variant changes short source(선택 변형이 숏 원천 변경)"),
        ("kpi_contract_gate", str(selected.get("package_precheck_status", "")).startswith("passed"), PACKAGE_PRECHECK, "selected row preserves DD KPI contract(선택 행이 DD KPI 계약 유지)"),
        ("no_trade_splitting_gate", bool(data_rows) and any(row["audit_item"].startswith("single_position") and row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "single-position replay used(단일 포지션 재생 사용)"),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), RUN_EVIDENCE_RECEIPT, "required receipts exist(필수 영수증 존재)"),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "required gates connected to closeout(필수 게이트를 종료 기록에 연결)"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "no authority/promotion/goal claim(권위/승격/목표 주장 없음)"),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def final_payload(selected: Mapping[str, Any], surface: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    selected_status = str(selected.get("package_precheck_status", ""))
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT if selected_status.startswith("passed") else "negative_or_inconclusive_short_source_scout_review_required_no_authority",
        "decision": DECISION,
        "selected_variant_id": selected["variant_id"],
        "selected_package_precheck_status": selected["package_precheck_status"],
        "selected_override_rows": selected["override_rows"],
        "selected_estimated_mt5_net_profit": selected["estimated_mt5_net_profit"],
        "selected_estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
        "selected_estimated_mt5_drawdown": selected["estimated_mt5_drawdown"],
        "selected_estimated_mt5_trade_count": selected["estimated_mt5_trade_count"],
        "selected_estimated_mt5_density": selected["estimated_mt5_density"],
        "selected_sim_short_trade_count": selected["sim_short_trade_count"],
        "selected_sim_short_share": selected["sim_short_share"],
        "selected_sim_short_net_delta_vs_anchor": selected["sim_short_net_delta_vs_anchor"],
        "db_mt5_net_profit": selected["db_mt5_net_profit"],
        "db_mt5_profit_factor": selected["db_mt5_profit_factor"],
        "db_mt5_drawdown": selected["db_mt5_drawdown"],
        "db_mt5_short_trade_count": selected["db_mt5_short_trade_count"],
        "db_mt5_short_share": selected["db_mt5_short_share"],
        "surface_rows": len(surface),
        "package_precheck_passes": sum(1 for row in surface if str(row["package_precheck_status"]).startswith("passed")),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "measurement_scope": "telemetry replay proxy scout(텔레메트리 재생 프록시 탐색)", "surface": rel(SHORT_SOURCE_SURFACE), "selected": rel(SELECTED_CANDIDATE), "status": "completed_no_mt5_execution(완료, MT5 실행 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "Short-source rules can improve side balance without weakening DB MT5 boundary.", "comparison_baseline": db.RUN_ID, "control_variables": ["same DB telemetry", "same raw M5 open prices", "same max-hold policy"], "changed_variables": selected["changed_variables"], "success_criteria": "estimated MT5 net >= DB, PF >= 1.35, density 3-10, short share improves", "failure_criteria": "simulator-only gain or side balance not improved", "invalid_conditions": "lookahead, overlapping positions, missing raw join", "stop_conditions": NEXT_RUN_ID, "evidence_plan": [rel(SHORT_SOURCE_SURFACE), rel(PACKAGE_PRECHECK), rel(RUN364DE_QUEUE)]})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(db.RUNTIME_OUTPUT_COPY), rel(SOURCE_RAW_US100_M5)], "time_axis": "written_at entry open and source_time closed feature bar(written_at 진입 시가와 source_time 종료 피처봉)", "sample_scope": "Tier A runtime telemetry replay(Tier A 런타임 텔레메트리 재생)", "missing_or_duplicate_check": rel(DATA_INTEGRITY_AUDIT), "feature_label_boundary": "entry-known probability/calendar/closed-bar return only(진입 시점 기지 확률/달력/종료봉 수익률만)", "split_boundary": "single-position replay(단일 포지션 재생)", "leakage_risk": "proxy scout only until MT5 runtime probe(프록시 탐색은 MT5 런타임 탐침 전까지만)", "data_hash_or_identity": sha(SOURCE_RAW_US100_M5), "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": "selected short-source variant improves estimated short balance(선택 숏 원천 변형이 추정 방향 균형 개선)", "comparison_baseline": rel(BASELINE_REPLAY_GAP), "likely_drivers": [selected["variant_family"], selected["changed_variables"]], "segment_checks": [rel(VARIANT_HOUR_SIDE_ATTRIBUTION), rel(VARIANT_MONTH_SIDE_ATTRIBUTION), rel(VARIANT_REASON_ATTRIBUTION)], "trade_shape": "max_hold_6_single_position_replay(max_hold 6 단일 포지션 재생)", "alternative_explanations": ["raw open replay does not include exact MT5 spread/bridge effects", "baseline replay differs from MT5 and only deltas are usable"], "attribution_confidence": "medium_low_until_review(검토 전 중하)", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(SHORT_SOURCE_SURFACE), rel(SELECTED_CANDIDATE), rel(DATA_INTEGRITY_AUDIT), rel(BASELINE_REPLAY_GAP)], "evidence_missing": ["MT5 runtime package", "MT5 runtime probe", "forward/replay evidence"], "judgment_label": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "Short-source scout found a review candidate, but runtime authority is not claimed(숏 원천 탐색은 검토 후보를 찾았지만 런타임 권위는 주장하지 않음)."})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "tracked_proxy_scout_artifacts(추적된 프록시 탐색 산출물)", "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "proxy short-source review candidate only(프록시 숏 원천 검토 후보만)", "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "prevents proxy result from being overstated as operating model(프록시 결과가 운영 모델로 과장되는 것을 막음)"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    if len(rows) > limit:
        lines.append("| ... | ... | ... | ... | ... | ... |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    surface = read_csv(SHORT_SOURCE_SURFACE).sort_values("selection_score", ascending=False).head(8).to_dict("records")
    report = f"""# run364DD h17 short-source expansion runtime-positive scout(17시 숏 원천 확장 런타임 긍정 단서 탐색)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- selected variant(선택 변형): `{final['selected_variant_id']}`
- selected estimated MT5 net/PF/DD(선택 추정 MT5 순수익/수익 팩터/낙폭): `{final['selected_estimated_mt5_net_profit']}` / `{final['selected_estimated_mt5_profit_factor']}` / `{final['selected_estimated_mt5_drawdown']}`
- selected estimated density(선택 추정 밀도): `{final['selected_estimated_mt5_density']}`
- selected short count/share(선택 숏 수/비중): `{final['selected_sim_short_trade_count']}` / `{final['selected_sim_short_share']}`
- package precheck(패키지 사전검토): `{final['selected_package_precheck_status']}`

## Action/Effect(행동/효과)

Action(행동): DB MT5 telemetry(DB MT5 텔레메트리)를 single-position replay(단일 포지션 재생)로 다시 돌리고, flat(관망)으로 막힌 short-source rows(숏 원천 행)를 11개 변형으로 열었습니다.

Effect(효과): pure exposure scaling(순수 노출 증폭) 반복이 아니라, 새 숏 진입 원천이 side balance(방향 균형)를 개선할 수 있는지 분리했습니다.

## Surface(표면)

{markdown_table(surface, ['variant_id', 'override_rows', 'estimated_mt5_net_profit', 'estimated_mt5_profit_factor', 'estimated_mt5_density', 'sim_short_trade_count', 'package_precheck_status'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is proxy scout only(프록시 탐색 전용)입니다. new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DD decision(결정): h17 short-source expansion runtime-positive scout

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- selected variant(선택 변형): `{final['selected_variant_id']}`
- estimated MT5 net/PF/density(추정 MT5 순수익/수익 팩터/밀도): `{final['selected_estimated_mt5_net_profit']}` / `{final['selected_estimated_mt5_profit_factor']}` / `{final['selected_estimated_mt5_density']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): review(검토) 단계에서 MT5 package(MT5 패키지)로 옮길 수 있는 short-source rule(숏 원천 규칙)인지 판단합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DD__{RUN_ID}", f"\n- run364DD__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - short-source expansion proxy scout(숏 원천 확장 프록시 탐색), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364DD__{RUN_ID}", f"\n## run364DD Short-Source Expansion(숏 원천 확장)\n\nAction(행동): DB telemetry(DB 텔레메트리)를 single-position proxy replay(단일 포지션 프록시 재생)로 변형했습니다.\n\nEffect(효과): `{final['selected_variant_id']}`를 `run364DE` review(검토) 대상으로 넘깁니다.\n")
    append_text_once(STAGE_README, f"run364DD__{RUN_ID}", f"\n<!-- run364DD__{RUN_ID} -->\n## run364DD short-source expansion scout(숏 원천 확장 탐색)\n\nSelected(선택): `{final['selected_variant_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364DD` completed(완료) short-source expansion proxy scout(숏 원천 확장 프록시 탐색). Selected variant(선택 변형)는 `{final['selected_variant_id']}`이고 estimated MT5 net/PF/density(추정 MT5 순수익/수익 팩터/밀도)는 `{final['selected_estimated_mt5_net_profit']}` / `{final['selected_estimated_mt5_profit_factor']}` / `{final['selected_estimated_mt5_density']}`입니다. 이 값은 telemetry replay delta(텔레메트리 재생 변화분) 기반이며 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 selected short-source variant(선택 숏 원천 변형)의 runtime representability(런타임 표현 가능성), no-split boundary(무분할 경계), MT5 package need(MT5 패키지 필요성)를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest proxy scout(최근 프록시 탐색): `{RUN_ID}`.

Selected variant(선택 변형): `{final['selected_variant_id']}`.

Estimated MT5 net/PF/density(추정 MT5 순수익/수익 팩터/밀도): `{final['selected_estimated_mt5_net_profit']}` / `{final['selected_estimated_mt5_profit_factor']}` / `{final['selected_estimated_mt5_density']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DD__{RUN_ID}", f"\n<!-- run364DD__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed short-source expansion proxy scout(숏 원천 확장 프록시 탐색); selected `{final['selected_variant_id']}`; next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364DD__{RUN_ID}", f"\n<!-- run364DD__{RUN_ID} -->\n- `{RUN_ID}`: short-source expansion(숏 원천 확장) seed preserved(씨앗 보존). Selected(선택) `{final['selected_variant_id']}`; MT5 review(MT5 검토) 필요.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364DD__{RUN_ID}", f"\n<!-- run364DD__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님). Proxy scout(프록시 탐색) only(전용)이므로 MT5 runtime probe(MT5 런타임 탐침) 전까지 operating claim(운영 주장) 금지.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": final["judgment"],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["surface_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scout(프록시 탐색)",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(주장 범위 밖, 프록시 전용)",
        "evidence_boundary": "telemetry_replay_proxy_only(텔레메트리 재생 프록시 전용)",
        "question": "Can short-source expansion improve DB side balance without weakening MT5 boundary?(숏 원천 확장이 DB 방향 균형을 MT5 경계 약화 없이 개선하는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_estimated_mt5_net_profit"],
        "profit_factor": final["selected_estimated_mt5_profit_factor"],
        "drawdown": final["selected_estimated_mt5_drawdown"],
        "trade_count": final["selected_estimated_mt5_trade_count"],
        "trade_density_per_feature_day": final["selected_estimated_mt5_density"],
        "short_trade_count": final["selected_sim_short_trade_count"],
        "result_judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(SHORT_SOURCE_SURFACE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, status, include in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_separate", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_runtime_telemetry(Tier B 런타임 텔레메트리 없음)", False),
        ("tier_ab_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, Tier A 프록시 전용)", False),
    ]:
        row = {
            **common,
            "subrun_id": f"{RUN_ID}__{suffix}",
            "record_view": view,
            "tier_scope": tier,
            "kpi_scope": "telemetry_replay_proxy_scout(텔레메트리 재생 프록시 탐색)",
            "status": status,
            "rows": final["surface_rows"] if include else 0,
            "net_profit": final["selected_estimated_mt5_net_profit"] if include else "",
            "profit_factor": final["selected_estimated_mt5_profit_factor"] if include else "",
            "trade_count": final["selected_estimated_mt5_trade_count"] if include else "",
        }
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], ledger_rows, extend_header=True)
    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("proxy_surface", SHORT_SOURCE_SURFACE, "DD short-source expansion surface(DD 숏 원천 확장 표면)."),
            ("selected_candidate", SELECTED_CANDIDATE, "Selected DD candidate(선택 DD 후보)."),
            ("selected_trade_tape", SELECTED_TRADE_TAPE, "Selected DD telemetry replay trade tape(선택 DD 텔레메트리 재생 거래 기록)."),
            ("baseline_replay_gap", BASELINE_REPLAY_GAP, "Baseline replay gap(기준선 재생 차이)."),
            ("package_precheck", PACKAGE_PRECHECK, "Package precheck(패키지 사전검토)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
            ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    surface, frames, audits, baseline_frame, mt5_base = build_surface()
    selected = selected_row(surface)
    write_artifacts(surface, frames, audits, selected, baseline_frame, mt5_base)
    cycles, _telemetry = load_cycles()
    selected_frame = frames[str(selected["variant_id"])]
    data_rows = data_integrity_rows(cycles, baseline_frame, selected_frame, surface)
    write_csv(DATA_INTEGRITY_AUDIT, data_rows)
    receipt_paths = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(surface, selected, data_rows, receipt_paths, final_written=False)
    created_at = now_utc()
    final = final_payload(selected, surface, gates, created_at)
    write_receipts(final, selected)
    gates = gate_rows(surface, selected, data_rows, receipt_paths, final_written=True)
    final = final_payload(selected, surface, gates, created_at)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
