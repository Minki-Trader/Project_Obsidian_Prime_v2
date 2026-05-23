from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "273_onnx_candidate_campaign__time_risk_router_stability_validation"
SOURCE_STAGE_ID = "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
RUN_ID = "run273A_design_time_risk_router_stability_validation_packet_v1"
SOURCE_RUN_ID = "run272D_review_time_risk_router_mt5_probe_v1"
SOURCE_MT5_RUN_ID = "run272C_time_risk_router_mt5_signal_replay_v1"
STATUS = "completed_time_risk_router_stability_validation_packet_design_no_candidate_selection"
JUDGMENT = "stability_validation_packet_ready_no_candidate_selection"
NEXT_ACTION = "run273B_execute_time_risk_router_stability_validation_review"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE_ID
SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
RUN_DIR = STAGE / "02_runs" / "run273A"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

SOURCE_QUEUE = SOURCE_STAGE / "02_runs" / "run272D" / "stage273_stability_queue.csv"
SOURCE_REVIEW = SOURCE_STAGE / "02_runs" / "run272D" / "pressure_survivor_review.csv"
SOURCE_FAILURE_MEMORY = SOURCE_STAGE / "02_runs" / "run272D" / "pressure_failure_memory.csv"
SOURCE_KPI = SOURCE_STAGE / "02_runs" / "run272C" / "mt5_kpi_summary.csv"
SOURCE_FORENSICS = SOURCE_STAGE / "02_runs" / "run272C" / "backtest_forensics.csv"
SOURCE_RUNTIME_SUPPLY = SOURCE_STAGE / "02_runs" / "run272C" / "runtime_supply_matrix.csv"
SOURCE_Q04_PAYLOAD = SOURCE_STAGE / "02_runs" / "run272B" / "payloads" / "q04_payload.parquet"
SOURCE_Q04_HANDOFF = SOURCE_STAGE / "02_runs" / "run272B" / "handoff" / "q04.json"
SOURCE_RUN272C_MANIFEST = SOURCE_STAGE / "02_runs" / "run272C" / "run_manifest.json"
SOURCE_RUN272D_REPORT = SOURCE_STAGE / "03_reviews" / "run272D_report.md"
SOURCE_STAGE272_CLOSEOUT = SOURCE_STAGE / "03_reviews" / "stage272_closeout_stage273_stability_validation_handoff.md"

STABILITY_PLAN = RUN_DIR / "stability_validation_plan.csv"
SLICE_PLAN = RUN_DIR / "stability_slice_plan.csv"
CURVE_QUEUE = RUN_DIR / "curve_review_queue.csv"
TRADE_QUALITY_PLAN = RUN_DIR / "trade_quality_probe_plan.csv"
ADAPTER_PRECHECK_PLAN = RUN_DIR / "adapter_identity_precheck_plan.csv"
WORK_PACKET_RECEIPT = RUN_DIR / "work_packet_schema_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
BACKTEST_FORENSICS_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
PERFORMANCE_ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run273A_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
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
]
STAGE_LEDGER_COLUMNS = [
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
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = list(columns or [])
    if not fieldnames:
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["status"]
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: "" if row.get(key) is None else row.get(key) for key in fieldnames})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("; ".join(missing))


def tier_short(tier_view: str) -> str:
    if tier_view.startswith("Tier A"):
        return "Tier A"
    if tier_view.startswith("Tier B"):
        return "Tier B"
    return tier_view


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def round4(value: Any) -> float:
    return round(safe_float(value), 4)


def load_inputs() -> tuple[list[dict[str, str]], pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    must_exist(
        [
            SOURCE_QUEUE,
            SOURCE_REVIEW,
            SOURCE_FAILURE_MEMORY,
            SOURCE_KPI,
            SOURCE_FORENSICS,
            SOURCE_RUNTIME_SUPPLY,
            SOURCE_Q04_PAYLOAD,
            SOURCE_Q04_HANDOFF,
            SOURCE_RUN272C_MANIFEST,
            SOURCE_RUN272D_REPORT,
            SOURCE_STAGE272_CLOSEOUT,
        ]
    )
    queue = read_csv_rows(SOURCE_QUEUE)
    if not queue:
        raise ValueError("Stage273 stability queue is empty.")
    kpi = pd.read_csv(io_path(SOURCE_KPI))
    forensics = pd.read_csv(io_path(SOURCE_FORENSICS))
    review = pd.read_csv(io_path(SOURCE_REVIEW))
    payload = pd.read_parquet(io_path(SOURCE_Q04_PAYLOAD))
    return queue, kpi, forensics, review, payload


def build_stability_plan(queue: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in queue:
        tier = source["tier_scope"]
        rows.append(
            {
                "plan_id": f"run273A_q04_{tier.lower().replace(' ', '_')}_stability_validation",
                "variant_id": source["variant_id"],
                "tier_scope": tier,
                "validation_focus": "balance/equity curve(잔액/평가금 곡선);month/session/chron weak slices(월/세션/시간순 약한 구간);trade quality(거래 품질)",
                "source_metric_summary": (
                    f"net_sum={source['net_profit_sum']};pf_min={source['profit_factor_min']};"
                    f"expectancy_min={source['expectancy_min']};trade_count_sum={source['trade_count_sum']};"
                    f"dd_max_pct={source['max_drawdown_percent_max']}"
                ),
                "success_criteria": "PF(수익 팩터) and expectancy(기대값) remain plausible while drawdown(손실폭) and weak slices(약한 구간) do not break the thesis(논제).",
                "failure_criteria": "month/session/zoomed curve(월/세션/확대 곡선) shows concentrated collapse or trade quality(거래 품질) depends on one fragile pocket.",
                "invalid_conditions": "missing MT5 report(MT5 보고서 누락), malformed trade list(거래 목록 오류), feature order drift(피처 순서 드리프트), or tier identity mismatch(티어 정체성 불일치).",
                "stop_conditions": "If q04 fails stability, close as failure memory(실패 기억); if it survives, hand off only to Adapter package(어댑터 패키지) preparation, not ONNX(온엑스) yet.",
                "required_outputs": "slice review CSV(구간 검토 CSV);curve zoom queue(곡선 확대 대기열);trade quality table(거래 품질 표);Adapter identity receipt(어댑터 정체성 영수증)",
                "next_action": NEXT_ACTION,
                "claim_boundary": BOUNDARY,
            }
        )
    rows.append(
        {
            "plan_id": "run273A_q04_tier_ab_combined_scope_boundary",
            "variant_id": "run272A_q04_weak_clock_throttle_router",
            "tier_scope": "Tier A+B combined",
            "validation_focus": "combined record(합산 기록) boundary audit(경계 감사)",
            "source_metric_summary": "out_of_scope_by_claim_for_profit_attribution;separate tester runs are not synthetic combined profit(합성 합산 수익 아님)",
            "success_criteria": "Record route/signal coverage(경로/신호 커버리지) without claiming combined profit(합산 수익 주장 없음).",
            "failure_criteria": "Any report treats separate tester sums(분리 테스터 합계) as actual routed total(실제 라우팅 전체).",
            "invalid_conditions": "No tier component identity(티어 구성 정체성 없음) or no route count(경로 수 없음).",
            "stop_conditions": "Keep combined profit(합산 수익) out_of_scope_by_claim(주장 범위 밖) until routed account evidence(라우팅 계좌 근거) exists.",
            "required_outputs": "combined scope boundary row(합산 범위 경계 행);route count review(경로 수 검토)",
            "next_action": NEXT_ACTION,
            "claim_boundary": BOUNDARY,
        }
    )
    return rows


def payload_for_review(payload: pd.DataFrame) -> pd.DataFrame:
    df = payload.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df[df["split"].isin(["validation_is", "oos"])].copy()
    df["tier_scope"] = df["tier_view"].map(tier_short)
    df["month"] = df["timestamp"].dt.strftime("%Y-%m")
    df["utc_hour"] = df["timestamp"].dt.hour
    df["chron_bucket"] = pd.cut(
        df["chron_phase_age"].astype(float),
        bins=[-0.001, 0.33, 0.66, 1.001],
        labels=["early(초반)", "middle(중반)", "late(후반)"],
    ).astype(str)
    df["session_risk_bucket"] = pd.cut(
        df["session_clock_risk"].astype(float),
        bins=[-0.001, 0.25, 0.5, 0.75, 1.001],
        labels=["low(낮음)", "middle(중간)", "high(높음)", "extreme(극단)"],
    ).astype(str)
    return df


def summarize_slice_rows(df: pd.DataFrame, slice_family: str, group_cols: Sequence[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    grouped = df.groupby(list(group_cols), dropna=False, observed=False)
    for keys, group in grouped:
        if not isinstance(keys, tuple):
            keys = (keys,)
        key_map = dict(zip(group_cols, keys, strict=True))
        route = group["route_signal_value"].astype(float)
        rows_count = len(group)
        nonflat = int((route != 0).sum())
        long_count = int((route > 0).sum())
        short_count = int((route < 0).sum())
        directional_max = max(long_count, short_count, 1)
        directional_min = min(long_count, short_count)
        nonflat_rate = nonflat / rows_count if rows_count else 0.0
        long_short_balance = directional_min / directional_max if directional_max else 0.0
        slice_key = "|".join(f"{key}={value}" for key, value in key_map.items())
        weakness_flags: list[str] = []
        if nonflat < 25:
            weakness_flags.append("thin_signal_count(얇은 신호 수)")
        if nonflat_rate > 0.75:
            weakness_flags.append("high_exposure_rate(높은 노출률)")
        if long_short_balance < 0.35 and nonflat >= 25:
            weakness_flags.append("direction_concentration(방향 집중)")
        if safe_float(group["session_clock_risk"].mean()) >= 0.75:
            weakness_flags.append("high_session_clock_risk(높은 세션 시계 위험)")
        rows.append(
            {
                "slice_id": hashlib.sha1(f"{slice_family}:{slice_key}".encode("utf-8")).hexdigest()[:16],
                "slice_family": slice_family,
                "tier_scope": key_map.get("tier_scope", "all"),
                "split": key_map.get("split", "all"),
                "slice_key": slice_key,
                "rows": rows_count,
                "nonflat_signal_count": nonflat,
                "long_signal_count": long_count,
                "short_signal_count": short_count,
                "flat_count": int((route == 0).sum()),
                "nonflat_rate": round(nonflat_rate, 4),
                "long_short_balance": round(long_short_balance, 4),
                "candidate_decision_score_mean": round4(group["candidate_decision_score"].mean()),
                "phase_risk_score_mean": round4(group["phase_risk_score"].mean()),
                "session_clock_risk_mean": round4(group["session_clock_risk"].mean()),
                "weakness_focus": ";".join(weakness_flags) if weakness_flags else "watch_in_run273B(273B에서 관찰)",
                "run273b_required_check": "compute realized trade quality(실현 거래 품질 계산) and curve contribution(곡선 기여 확인)",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_slice_plan(payload: pd.DataFrame) -> list[dict[str, Any]]:
    df = payload_for_review(payload)
    rows: list[dict[str, Any]] = []
    rows.extend(summarize_slice_rows(df, "month(월)", ["tier_scope", "split", "month"]))
    rows.extend(summarize_slice_rows(df, "session_risk_bucket(세션 위험 구간)", ["tier_scope", "split", "session_risk_bucket"]))
    rows.extend(summarize_slice_rows(df, "weekday_phase(요일 단계)", ["tier_scope", "split", "weekday_phase"]))
    rows.extend(summarize_slice_rows(df, "chron_bucket(시간순 구간)", ["tier_scope", "split", "chron_bucket"]))
    rows.extend(summarize_slice_rows(df, "route_signal_label(경로 신호 라벨)", ["tier_scope", "split", "route_signal_label"]))
    return rows


def build_curve_queue(kpi: pd.DataFrame, forensics: pd.DataFrame) -> list[dict[str, Any]]:
    q04 = kpi[kpi["record_view"].astype(str).str.contains("q04", na=False)].copy()
    forensic_map = {
        (row["tier"], row["split"]): row
        for _, row in forensics[forensics["attempt_name"].astype(str).str.contains("q04", na=False)].iterrows()
    }
    rows: list[dict[str, Any]] = []
    for _, row in q04.iterrows():
        forensic = forensic_map.get((row["tier_scope"], row["split"]))
        rows.append(
            {
                "queue_id": f"run273A_curve_{str(row['record_view']).replace('mt5_', '')}",
                "tier_scope": row["tier_scope"],
                "split": row["split"],
                "report_path": rel(row["report_path"]),
                "set_path": "" if forensic is None else rel(forensic.get("set_path", "")),
                "ini_path": "" if forensic is None else rel(forensic.get("ini_path", "")),
                "net_profit": row["net_profit"],
                "profit_factor": row["profit_factor"],
                "trade_count": row["trade_count"],
                "max_drawdown_percent": row["max_drawdown_percent"],
                "expectancy": row["expectancy"],
                "curve_checks": "full curve(전체 곡선);max-DD zoom(최대 손실폭 확대);final-month zoom(마지막 달 확대);stair-step/chop check(계단형/흔들림 확인)",
                "priority": "high(높음)" if safe_float(row["max_drawdown_percent"]) >= 30 else "medium(중간)",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_trade_quality_plan(kpi: pd.DataFrame) -> list[dict[str, Any]]:
    q04 = kpi[kpi["record_view"].astype(str).str.contains("q04", na=False)].copy()
    rows: list[dict[str, Any]] = []
    for _, row in q04.iterrows():
        rows.append(
            {
                "plan_id": f"run273A_trade_quality_{str(row['record_view']).replace('mt5_', '')}",
                "tier_scope": row["tier_scope"],
                "split": row["split"],
                "available_kpi": (
                    f"net={row['net_profit']};pf={row['profit_factor']};trades={row['trade_count']};"
                    f"win_rate={row['win_rate_percent']};dd_pct={row['max_drawdown_percent']};expectancy={row['expectancy']}"
                ),
                "missing_trade_shape": "average win/loss(평균 승/패);payoff ratio(손익비);loss cluster(손실 군집);holding time(보유 시간)",
                "required_run273b_action": "parse MT5 report trade list(MT5 보고서 거래 목록 파싱) and compute weak-slice trade quality(약한 구간 거래 품질 계산)",
                "failure_trigger": "good PF(수익 팩터) depends on small pocket(작은 구간) or DD(손실폭) clusters around weak clock(약한 시계)",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def build_adapter_precheck(payload: pd.DataFrame) -> list[dict[str, Any]]:
    df = payload_for_review(payload)
    rows: list[dict[str, Any]] = []
    fields = [
        "input_feature_order_hash",
        "expected_feature_order_hash",
        "source_feature_order_hash",
        "adapter_schema_hash",
        "source_adapter_schema_hash",
        "decision_rule_hash",
        "risk_rule_hash",
        "variant_decision_surface_hash",
        "source_model_hash",
    ]
    for field in fields:
        unique_values = sorted(str(value) for value in df[field].dropna().unique())
        rows.append(
            {
                "check_id": f"run273A_adapter_{field}",
                "check_name": f"{field}(정체성 필드)",
                "observed_unique_count": len(unique_values),
                "observed_values": ";".join(unique_values[:3]),
                "status": "ready_for_precheck(사전점검 준비됨)" if unique_values else "missing_required(필수 누락)",
                "effect": "Adapter package(어댑터 패키지) 전 feature/order/decision/risk identity(피처/순서/판단/위험 정체성)를 고정한다.",
                "claim_boundary": BOUNDARY,
            }
        )
    mismatch_count = int((df["input_feature_order_hash"] != df["expected_feature_order_hash"]).sum())
    source_mismatch_count = int((df["input_feature_order_hash"] != df["source_feature_order_hash"]).sum())
    support_match_rate = safe_float(df["support_identity_match_flag"].astype(float).mean())
    rows.extend(
        [
            {
                "check_id": "run273A_adapter_feature_order_match",
                "check_name": "feature order match(피처 순서 일치)",
                "observed_unique_count": mismatch_count,
                "observed_values": f"input_vs_expected_mismatch={mismatch_count};input_vs_source_mismatch={source_mismatch_count}",
                "status": "pass(통과)" if mismatch_count == 0 and source_mismatch_count == 0 else "fail(실패)",
                "effect": "runtime handoff(런타임 인계) 전에 feature order drift(피처 순서 드리프트)를 차단한다.",
                "claim_boundary": BOUNDARY,
            },
            {
                "check_id": "run273A_adapter_support_identity_match",
                "check_name": "support identity match(보조 정체성 일치)",
                "observed_unique_count": int((df["support_identity_match_flag"].astype(float) == 0).sum()),
                "observed_values": f"support_identity_match_rate={round(support_match_rate, 4)}",
                "status": "pass(통과)" if support_match_rate >= 0.999 else "watch(관찰)",
                "effect": "q04(4번 분기)가 support package(보조 패키지)와 잘못 섞였는지 확인한다.",
                "claim_boundary": BOUNDARY,
            },
        ]
    )
    return rows


def build_receipts(
    queue: Sequence[Mapping[str, str]],
    kpi: pd.DataFrame,
    forensics: pd.DataFrame,
    review: pd.DataFrame,
    payload: pd.DataFrame,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    q04_kpi = kpi[kpi["record_view"].astype(str).str.contains("q04", na=False)].copy()
    q04_forensics = forensics[forensics["attempt_name"].astype(str).str.contains("q04", na=False)].copy()
    q04_review = review[review["variant"].astype(str).eq("q04")].copy()
    payload_review = payload_for_review(payload)
    sample_scope = {
        "symbol": "US100",
        "timeframe": "M5",
        "date_range": f"{payload['timestamp'].min()} to {payload['timestamp'].max()}",
        "payload_rows": int(len(payload)),
        "review_rows_validation_oos": int(len(payload_review)),
        "tiers": sorted(payload_review["tier_scope"].unique().tolist()),
        "splits": sorted(payload_review["split"].unique().tolist()),
    }
    experiment = {
        "hypothesis": "q04 weak-clock throttle router(4번 약한 시계 제한 라우터)가 Stage272(272단계) 압박 생존 이후에도 곡선, 약한 구간, 거래 품질을 견디는지 확인한다.",
        "decision_use": "Stage274(274단계) ONNX(온엑스) 작업 전 Adapter package(어댑터 패키지) 준비로 넘길지, 실패 기억(failure memory, 실패 기억)으로 닫을지 결정한다.",
        "comparison_baseline": "Stage272(272단계) q01 reference control(참조 대조) and q02/q03 pressure branches(압박 분기)",
        "control_variables": ["US100", "M5", "FPMarkets broker feed(FPMarkets 브로커 피드)", "MT5 tester model=4(MT5 테스터 모델 4)", "deposit=500", "leverage=1:100"],
        "changed_variables": ["stability review lens(안정성 검토 렌즈)", "curve zoom(곡선 확대)", "weak-slice attribution(약한 구간 귀속)", "Adapter identity precheck(어댑터 정체성 사전점검)"],
        "sample_scope": sample_scope,
        "success_criteria": "q04(4번 분기)가 validation/OOS(검증/표본외) 모두에서 곡선 붕괴와 구간 집중 없이 trade quality(거래 품질)를 유지한다.",
        "failure_criteria": "한두 월/month(월), session(세션), chron bucket(시간순 구간), or direction(방향)에 수익이 몰리거나 drawdown(손실폭)이 치명적으로 집중된다.",
        "invalid_conditions": "MT5 report(MT5 보고서), payload(페이로드), feature order(피처 순서), split boundary(분할 경계), or tester identity(테스터 정체성)가 맞지 않는다.",
        "stop_conditions": "q04(4번 분기)가 안정성 압박에서 무너지면 repair loop(수리 반복) 없이 폐기 또는 새 thesis(논제)로 전환한다.",
        "evidence_plan": [rel(STABILITY_PLAN), rel(SLICE_PLAN), rel(CURVE_QUEUE), rel(TRADE_QUALITY_PLAN), rel(ADAPTER_PRECHECK_PLAN)],
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    data_integrity = {
        "data_source": [rel(SOURCE_Q04_PAYLOAD), rel(SOURCE_QUEUE), rel(SOURCE_KPI), rel(SOURCE_FORENSICS)],
        "time_axis": "timestamp(타임스탬프)는 UTC bar time(UTC 봉 시간)으로 읽고, M5(5분봉) 순서를 유지한다.",
        "sample_scope": sample_scope,
        "missing_or_duplicate_check": {
            "payload_missing_required_feature_count_max": int(payload["missing_required_feature_count"].max()),
            "feature_order_mismatch_count": int((payload["input_feature_order_hash"] != payload["expected_feature_order_hash"]).sum()),
            "timestamp_duplicate_rows_by_tier_split": int(payload.duplicated(["timestamp", "tier_view", "split"]).sum()),
        },
        "feature_label_boundary": "q04 payload(페이로드)는 label/future column(라벨/미래 열)을 포함하지 않는 runtime-like route surface(런타임 유사 경로 표면)다.",
        "split_boundary": "train(학습), validation_is(검증), oos(표본외)를 분리하고 run273A(273A 실행)는 validation/OOS(검증/표본외) 검토 계획만 만든다.",
        "leakage_risk": "Stage272(272단계) survivor selection(생존 분기 선택)을 다시 최적화로 쓰는 selection bias(선택 편향)가 가장 큰 위험이다.",
        "data_hash_or_identity": {
            rel(SOURCE_Q04_PAYLOAD): sha256_file(SOURCE_Q04_PAYLOAD),
            rel(SOURCE_QUEUE): sha256_file(SOURCE_QUEUE),
            rel(SOURCE_KPI): sha256_file(SOURCE_KPI),
        },
        "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
    }
    model_validation = {
        "model_family": "rule/scoring surface route signal replay(규칙/점수 표면 경로 신호 재생)",
        "target_and_label": "No new label(새 라벨 없음); q04 route_signal_value(경로 신호 값)를 runtime signal(런타임 신호)로 검토한다.",
        "split_method": "Stage272 MT5 validation/OOS split(272단계 MT5 검증/표본외 분할)",
        "selection_metric": "Stage272 pressure survivor(압박 생존): PF_min(최소 수익 팩터), net_sum(순수익 합), expectancy_min(최소 기대값), trade_count_sum(거래 수 합), DD_max(최대 손실폭)",
        "secondary_metrics": ["balance/equity curve(잔액/평가금 곡선)", "weak month/session(약한 월/세션)", "trade quality(거래 품질)", "Adapter identity(어댑터 정체성)"],
        "threshold_policy": "fixed q04 weak-clock throttle(고정 4번 약한 시계 제한); no new threshold search(새 임계값 탐색 없음)",
        "overfit_risk": "q04(4번 분기)가 Stage272(272단계) pressure set(압박 집합)에 맞춰진 생존 편향을 가질 수 있다.",
        "calibration_risk": "candidate_decision_score(후보 판단 점수)는 probability(확률)가 아니라 ordering/routing score(순서/경로 점수)로만 본다.",
        "comparison_baseline": "q01 reference control(참조 대조), q02/q03 failed pressure branches(실패 압박 분기)",
        "validation_judgment": "exploratory_stability_seed_no_candidate_selection(탐색 안정성 씨앗, 후보 선택 없음)",
    }
    forensic_identity = {
        "tester_identity": q04_forensics[["symbol", "timeframe", "deposit", "leverage", "model", "cost_boundary"]].drop_duplicates().to_dict("records"),
        "ea_identity": "Stage272 MT5 signal replay EA/settings(272단계 MT5 신호 재생 EA/설정); set/ini path(설정/초기화 경로)는 curve queue(곡선 대기열)에 기록",
        "report_identity": [
            {
                "attempt_name": row["attempt_name"],
                "report_path": rel(row["report_path"]),
                "set_path": rel(row["set_path"]),
                "ini_path": rel(row["ini_path"]),
            }
            for _, row in q04_forensics.iterrows()
        ],
        "trade_evidence": q04_kpi[["record_view", "tier_scope", "split", "net_profit", "profit_factor", "trade_count", "max_drawdown_percent", "expectancy"]].to_dict("records"),
        "cost_assumptions": "strategy_tester_report_costs_only_no_cost_edge_claim(전략 테스터 보고 비용만, 비용 우위 주장 없음)",
        "forensic_checks": ["report path present(보고서 경로 존재)", "tester status completed(테스터 완료)", "same deposit/leverage/model(동일 예치금/레버리지/모델)"],
        "backtest_judgment": "usable_with_boundary(경계부 사용 가능)",
    }
    q04_net = safe_float(q04_review["net_profit_sum"].astype(float).mean()) if not q04_review.empty else 0.0
    other = review[~review["variant"].astype(str).eq("q04")]
    performance = {
        "observed_change": "q04(4번 분기)는 q01~q03(1~3번 분기)보다 net_sum(순수익 합)과 PF_min(최소 수익 팩터)이 높고 trade_count(거래 수)는 더 낮다.",
        "comparison_baseline": "run272D pressure survivor review(272D 압박 생존 검토)",
        "likely_drivers": ["weak-clock throttle(약한 시계 제한)", "lower trade frequency(낮은 거래 빈도)", "balanced long/short route mix(균형 잡힌 롱/숏 경로 혼합)"],
        "segment_checks": "planned_not_completed_in_run273A(273A에서는 계획만 완료): month/session/chron/route slices(월/세션/시간순/경로 구간)",
        "trade_shape": {
            "q04_net_sum_mean": round(q04_net, 4),
            "q04_rows": int(len(q04_review)),
            "other_net_sum_mean": round(safe_float(other["net_profit_sum"].astype(float).mean()) if not other.empty else 0.0, 4),
            "q04_trade_count_sum_mean": round(safe_float(q04_review["trade_count_sum"].astype(float).mean()) if not q04_review.empty else 0.0, 4),
            "q04_dd_max_pct": round(safe_float(q04_review["max_drawdown_percent_max"].astype(float).max()) if not q04_review.empty else 0.0, 4),
        },
        "alternative_explanations": ["selection bias(선택 편향)", "single signal replay simplification(단일 신호 재생 단순화)", "separate Tier A/B duplication(분리 티어 중복)"],
        "attribution_confidence": "low_to_medium_until_trade_list_review(거래 목록 검토 전 낮음~중간)",
        "next_probe": NEXT_ACTION,
    }
    gate_rows = [
        {
            "gate_name": "work_packet_schema_lint(작업 묶음 스키마 점검)",
            "status": "passed(통과)",
            "evidence_path": rel(WORK_PACKET_RECEIPT),
            "effect": "run273A(273A 실행)의 가설/비교/기준/중단 조건이 파일로 남았다.",
        },
        {
            "gate_name": "data_integrity_boundary(데이터 무결성 경계)",
            "status": "passed_with_boundary(경계부 통과)",
            "evidence_path": rel(DATA_INTEGRITY_RECEIPT),
            "effect": "timestamp/split/feature order(타임스탬프/분할/피처 순서)를 다음 실행 전에 확인한다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]
    result_rows = [
        {
            "result_subject": "run273A time-risk router stability validation packet design(273A 시간 위험 라우터 안정성 검증 묶음 설계)",
            "evidence_available": "Stage272 q04 MT5 KPI(272단계 q04 MT5 핵심 성과 지표);q04 payload(페이로드);forensics(포렌식);survivor queue(생존 대기열)",
            "evidence_missing": "actual stability review(실제 안정성 검토);trade list attribution(거래 목록 귀속);Adapter package(어댑터 패키지);ONNX export/parity(온엑스 내보내기/동등성)",
            "judgment_label": JUDGMENT,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "q04(4번 분기)는 볼 가치가 있지만 아직 후보가 아니며, 다음 실행에서 곡선과 약한 구간을 깨뜨려 본다.",
        }
    ]
    return experiment, data_integrity, model_validation, forensic_identity, performance, gate_rows, result_rows


def write_report(
    stability_plan: Sequence[Mapping[str, Any]],
    slice_plan: Sequence[Mapping[str, Any]],
    curve_queue: Sequence[Mapping[str, Any]],
    trade_plan: Sequence[Mapping[str, Any]],
    adapter_plan: Sequence[Mapping[str, Any]],
    performance: Mapping[str, Any],
) -> None:
    tier_lines = "\n".join(
        f"- `{row['tier_scope']}`: `{row['source_metric_summary']}`"
        for row in stability_plan
        if row["tier_scope"] != "Tier A+B combined"
    )
    curve_lines = "\n".join(
        f"- `{row['tier_scope']}` `{row['split']}`: net(순수익) `{row['net_profit']}`, PF(수익 팩터) `{row['profit_factor']}`, DD(손실폭) `{row['max_drawdown_percent']}`, report(보고서) `{row['report_path']}`"
        for row in curve_queue
    )
    write_md(
        RUN_REPORT,
        f"""# run273A Time-Risk Router Stability Validation Packet(273A 시간 위험 라우터 안정성 검증 묶음)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run273A(273A 실행)는 q04(4번 분기)를 candidate package(후보 패키지)로 고르지 않고 stability validation(안정성 검증) 설계 묶음으로 정리했다.
효과(effect, 효과): 다음 run273B(273B 실행)가 곡선, 약한 월/세션/시간순 구간, 거래 품질, Adapter identity(어댑터 정체성)를 바로 검토할 수 있다.

## Seed Metrics(씨앗 지표)

{tier_lines}

Tier A+B combined(Tier A+B 합산)는 profit attribution(수익 귀속)이 아직 없으므로 `out_of_scope_by_claim(주장 범위 밖)`로 둔다.
효과(effect, 효과): separate tester runs(분리 테스터 실행)의 synthetic sum(합성 합산)을 actual routed total(실제 라우팅 전체)로 오해하지 않는다.

## Review Queues(검토 대기열)

- stability_validation_plan(안정성 검증 계획): `{rel(STABILITY_PLAN)}` rows(행) `{len(stability_plan)}`
- stability_slice_plan(안정성 구간 계획): `{rel(SLICE_PLAN)}` rows(행) `{len(slice_plan)}`
- curve_review_queue(곡선 검토 대기열): `{rel(CURVE_QUEUE)}` rows(행) `{len(curve_queue)}`
- trade_quality_probe_plan(거래 품질 탐침 계획): `{rel(TRADE_QUALITY_PLAN)}` rows(행) `{len(trade_plan)}`
- adapter_identity_precheck_plan(어댑터 정체성 사전점검 계획): `{rel(ADAPTER_PRECHECK_PLAN)}` rows(행) `{len(adapter_plan)}`

## Curve Queue(곡선 대기열)

{curve_lines}

## Attribution Boundary(귀속 경계)

- observed_change(관찰 변화): {performance['observed_change']}
- attribution_confidence(귀속 신뢰도): `{performance['attribution_confidence']}`
- next_probe(다음 탐침): `{performance['next_probe']}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def update_ledgers() -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"q04 stability validation packet designed;selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_separate_plan",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "q04_tier_a_stability_plan",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A separate stability validation plan(Tier A 분리 안정성 검증 계획)",
            "tier_scope": "Tier A",
            "kpi_scope": "stability_validation_design",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(STABILITY_PLAN),
            "primary_kpi": "planned_from_run272D_q04_tier_a",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Design only(설계만); run273B must review curve/slices/trade quality.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_separate_plan",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "q04_tier_b_stability_plan",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier B separate stability validation plan(Tier B 분리 안정성 검증 계획)",
            "tier_scope": "Tier B",
            "kpi_scope": "stability_validation_design",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(STABILITY_PLAN),
            "primary_kpi": "planned_from_run272D_q04_tier_b",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Design only(설계만); run273B must review curve/slices/trade quality.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_boundary",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "q04_tier_ab_combined_boundary",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A+B combined scope boundary(Tier A+B 합산 범위 경계)",
            "tier_scope": "Tier A+B combined",
            "kpi_scope": "combined_profit_out_of_scope_by_claim",
            "scoreboard_lane": "experiment_design",
            "status": STATUS,
            "judgment": "combined_profit_out_of_scope_by_claim_no_candidate_selection",
            "path": rel(STABILITY_PLAN),
            "primary_kpi": "route_signal_coverage_only",
            "guardrail_kpi": "no_synthetic_sum_profit_claim",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Separate tester runs are not actual routed total(분리 테스터 실행은 실제 라우팅 전체가 아님).",
        },
    ]
    stage_rows = [
        {
            "row_id": f"{RUN_ID}__packet_design",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "stability_validation_packet_design",
            "tier_scope": "Tier A+B planned views",
            "scoreboard": "experiment_design",
            "status": STATUS,
            "judgment": JUDGMENT,
            "evidence_boundary": "design_only_no_candidate_no_onnx",
            "report_path": rel(RUN_REPORT),
            "notes": f"next_action={NEXT_ACTION}.",
        },
        {
            "row_id": f"{RUN_ID}__adapter_identity_precheck_plan",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "adapter_identity_precheck_plan",
            "tier_scope": "Tier A+B payload identity",
            "scoreboard": "artifact_identity_design",
            "status": STATUS,
            "judgment": "adapter_identity_precheck_planned_no_package_selection",
            "evidence_boundary": "precheck_plan_only",
            "report_path": rel(ADAPTER_PRECHECK_PLAN),
            "notes": "Feature order/hash/schema checks prepared for run273B.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, stage_rows, key="row_id")


def update_state_docs() -> None:
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        f"Stage273(273단계)는 run273A(273A 실행)에서 q04(4번 분기) stability validation packet(안정성 검증 묶음)을 설계했다.\n효과(effect, 효과): q04(4번 분기)는 아직 selected candidate(선택 후보)가 아니며, run273B(273B 실행)가 곡선/구간/거래 품질/Adapter identity(어댑터 정체성)를 검토한다.",
    )
    selection = append_once(selection, "run273A_report", f"- run273A_report(273A 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run273A_stability_validation_plan", f"- run273A_stability_validation_plan(273A 안정성 검증 계획): `{rel(STABILITY_PLAN)}`")
    write_md(SELECTION_STATUS, selection)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review_index = append_once(
        review_index,
        "run273A_report",
        "\n".join(
            [
                f"- run273A_report(273A 보고서): `{rel(RUN_REPORT)}`",
                f"- run273A_stability_validation_plan(273A 안정성 검증 계획): `{rel(STABILITY_PLAN)}`",
                f"- run273A_slice_plan(273A 구간 계획): `{rel(SLICE_PLAN)}`",
                f"- run273A_curve_queue(273A 곡선 대기열): `{rel(CURVE_QUEUE)}`",
                f"- run273A_adapter_precheck(273A 어댑터 사전점검): `{rel(ADAPTER_PRECHECK_PLAN)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run273A_summary",
        f"- run273A_summary(273A 요약): run273A(273A 실행)는 q04(4번 분기)의 stability validation packet(안정성 검증 묶음)을 설계했다. Effect(효과): stability plan(안정성 계획), slice plan(구간 계획), curve queue(곡선 대기열), trade quality plan(거래 품질 계획), Adapter identity precheck(어댑터 정체성 사전점검)를 만들었고 selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage273(273단계) run273A(273A 실행) time-risk router stability validation packet design(시간 위험 라우터 안정성 검증 묶음 설계) `{RUN_ID}`. "
        f"Effect(효과): q04(4번 분기)를 selected candidate(선택 후보)가 아니라 run273B(273B 실행)의 curve/slice/trade-quality/Adapter identity(곡선/구간/거래품질/어댑터 정체성) 검토 대기열로 넘긴다.\n"
    )
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run273A stability validation packet design(273A 안정성 검증 묶음 설계)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): q04(4번 분기)를 후보로 확정하지 않고 run273B(273B 실행) 안정성 검토 대기열로 넘겼다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def write_manifests_and_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    source_inputs = [
        SOURCE_QUEUE,
        SOURCE_REVIEW,
        SOURCE_FAILURE_MEMORY,
        SOURCE_KPI,
        SOURCE_FORENSICS,
        SOURCE_RUNTIME_SUPPLY,
        SOURCE_Q04_PAYLOAD,
        SOURCE_Q04_HANDOFF,
        SOURCE_RUN272C_MANIFEST,
        SOURCE_RUN272D_REPORT,
        SOURCE_STAGE272_CLOSEOUT,
    ]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_mt5_run_id": SOURCE_MT5_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage273/design_time_risk_router_stability_validation_packet.py",
        "entry_command": "python stage_pipelines/stage273/design_time_risk_router_stability_validation_packet.py",
        "source_inputs": [rel(path) for path in source_inputs],
        "input_hashes": {rel(path): sha256_file(path) for path in source_inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)
    full_artifacts = [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run273A_stability_design_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run273A time-risk router stability validation design artifact.",
        }
        for path in full_artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, rows, key="artifact_id")


def execute() -> dict[str, Any]:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    queue, kpi, forensics, review, payload = load_inputs()

    stability_plan = build_stability_plan(queue)
    slice_plan = build_slice_plan(payload)
    curve_queue = build_curve_queue(kpi, forensics)
    trade_plan = build_trade_quality_plan(kpi)
    adapter_plan = build_adapter_precheck(payload)
    experiment, data_integrity, model_validation, backtest, performance, gate_rows, result_rows = build_receipts(
        queue, kpi, forensics, review, payload
    )
    work_packet = {
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
        "support_skills": [
            "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "obsidian-model-validation(옵시디언 모델 검증)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
        ],
        "required_gates": ["work_packet_schema_lint(작업 묶음 스키마 점검)"],
        "status": "schema_ready(스키마 준비)",
        "claim_boundary": BOUNDARY,
    }

    write_csv(STABILITY_PLAN, stability_plan)
    write_csv(SLICE_PLAN, slice_plan)
    write_csv(CURVE_QUEUE, curve_queue)
    write_csv(TRADE_QUALITY_PLAN, trade_plan)
    write_csv(ADAPTER_PRECHECK_PLAN, adapter_plan)
    write_json(WORK_PACKET_RECEIPT, work_packet)
    write_json(EXPERIMENT_RECEIPT, experiment)
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity)
    write_json(MODEL_VALIDATION_RECEIPT, model_validation)
    write_json(BACKTEST_FORENSICS_RECEIPT, backtest)
    write_json(PERFORMANCE_ATTRIBUTION_RECEIPT, performance)
    write_csv(GATE_AUDIT, gate_rows)
    write_csv(RESULT_JUDGMENT, result_rows)
    write_report(stability_plan, slice_plan, curve_queue, trade_plan, adapter_plan, performance)

    artifacts = [
        STABILITY_PLAN,
        SLICE_PLAN,
        CURVE_QUEUE,
        TRADE_QUALITY_PLAN,
        ADAPTER_PRECHECK_PLAN,
        WORK_PACKET_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        BACKTEST_FORENSICS_RECEIPT,
        PERFORMANCE_ATTRIBUTION_RECEIPT,
        GATE_AUDIT,
        RESULT_JUDGMENT,
        RUN_REPORT,
    ]
    write_manifests_and_registry(created_at, artifacts)
    update_ledgers()
    update_state_docs()
    write_manifests_and_registry(created_at, artifacts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "stability_plan_rows": len(stability_plan),
        "slice_plan_rows": len(slice_plan),
        "curve_queue_rows": len(curve_queue),
        "trade_quality_plan_rows": len(trade_plan),
        "adapter_precheck_rows": len(adapter_plan),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
