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


STAGE_ID = "119_adapter_research__v41_dd_compression_followup_review"
RUN_ID = "run119A_stage119_v41_dd_compression_followup_review_v1"
PACKET_ID = "stage119_v41_dd_compression_followup_review_v1"
PARENT_RUN_ID = "run118A_stage118_v41_dd_compression_density_repair_v1"
SOURCE_STAGE118_ID = "118_adapter_research__v41_dd_compression_density_repair"
SOURCE_STAGE118_CLOSEOUT_COMMIT = "1edf5a69757ae2e58bfcf0e4126b325d291170af"
SOURCE_STAGE118_LATEST_COMMIT = "d643def47022c81f86847fc802973370ccdeb2db"
SOURCE_STAGE116_LATEST_COMMIT = "c115268a398da4c8334b2c21530016f110b8e927"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
NEXT_STAGE_ID = "120_adapter_research__v41_post_dd_density_expansion_repair"
NEXT_RUN_ID = "run120A_stage120_v41_post_dd_density_expansion_repair_v1"
NEXT_PACKET_ID = "stage120_v41_post_dd_density_expansion_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage118_mt5_runtime_evidence_reviewed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}
STAGE110_REFERENCE = {
    "source_stage": "stage110_balanced_reference",
    "adapter_id": "s110_v41_h3_cd9_lng53_early_adx19",
    "profit_factor": 1.637076853,
    "net_profit": 644.76,
    "max_drawdown_percent": 18.69,
    "trade_count": 147,
}
STAGE116_BASELINES = {
    "s116_v41_h3_cd9_session_margin_lng52": {
        "source_stage": "stage116_quality_anchor",
        "adapter_id": "s116_v41_h3_cd9_session_margin_lng52",
        "profit_factor": 1.810756505,
        "net_profit": 2041.72,
        "max_drawdown_percent": 19.10,
        "trade_count": 174,
    },
    "s116_v41_h3_cd8_session_margin_lng53": {
        "source_stage": "stage116_density_anchor",
        "adapter_id": "s116_v41_h3_cd8_session_margin_lng53",
        "profit_factor": 1.707481833,
        "net_profit": 1783.59,
        "max_drawdown_percent": 19.59,
        "trade_count": 176,
    },
}
SOURCE_BASELINE_BY_VARIANT = {
    "s118_v41_h3_cd9_session_margin_risk040_lng52": "s116_v41_h3_cd9_session_margin_lng52",
    "s118_v41_h3_cd9_session_margin_risk035_lng52": "s116_v41_h3_cd9_session_margin_lng52",
    "s118_v41_h3_cd9_session_margin_risk030_lng52": "s116_v41_h3_cd9_session_margin_lng52",
    "s118_v41_h3_cd8_session_margin_risk035_lng53": "s116_v41_h3_cd8_session_margin_lng53",
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

STAGE118_REVIEWS = Path("stages") / SOURCE_STAGE118_ID / "03_reviews"
STAGE118_SUMMARY = STAGE118_REVIEWS / "stage118_dd_compression_density_summary.csv"
STAGE118_SEGMENTS = STAGE118_REVIEWS / "stage118_segment_kpi_summary.csv"
STAGE118_RISK_ATR = STAGE118_REVIEWS / "stage118_risk_atr_telemetry.csv"
STAGE118_REPORT = STAGE118_REVIEWS / "stage118_dd_compression_density_report.md"
STAGE118_DECISION = STAGE118_REVIEWS / "stage118_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage119_dd_compression_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage119_stage116_stage118_34d_comparison.csv"
TRADEOFF_PATH = REVIEWS_ROOT / "stage119_dd_tradeoff_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage119_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def num(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        return default
    try:
        return float(str(value))
    except ValueError:
        return default


def fmt(value: float, digits: int = 6) -> str:
    return f"{value:.{digits}f}"


def stage118_oos_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(STAGE118_SUMMARY)
        if row.get("split") == "oos" and row.get("view") == "actual_routed_total" and row.get("status") == "completed"
    ]


def segment_row(adapter_id: str, segment_type: str, segment: str) -> dict[str, str]:
    for row in read_csv(STAGE118_SEGMENTS):
        if row.get("adapter_id") != adapter_id:
            continue
        if row.get("split") != "oos" or row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") == segment_type and row.get("segment") == segment:
            return row
    return {}


def stage118_metric(row: Mapping[str, Any]) -> dict[str, Any]:
    adapter_id = str(row.get("adapter_id", ""))
    full = segment_row(adapter_id, "full_split", "actual_routed_total")
    early = segment_row(adapter_id, "chronological_third", "early")
    mid = segment_row(adapter_id, "chronological_third", "mid")
    late = segment_row(adapter_id, "chronological_third", "late")
    source_id = SOURCE_BASELINE_BY_VARIANT.get(adapter_id, "")
    source = STAGE116_BASELINES.get(source_id, {})
    pf = num(full, "profit_factor", num(row, "profit_factor"))
    net = num(full, "net_profit", num(row, "net_profit"))
    dd = num(row, "max_drawdown_percent")
    trades = num(full, "trade_count", num(row, "trade_count"))
    return {
        "run_id": RUN_ID,
        "source_stage": "stage118_dd_compression_density_repair",
        "source_adapter_id": source_id,
        "adapter_id": adapter_id,
        "risk_cap": num(row, "model_risk_max_pct"),
        "profit_factor": pf,
        "net_profit": net,
        "max_drawdown_percent": dd,
        "trade_count": trades,
        "expectancy": num(full, "expectancy", num(row, "expectancy")),
        "cost_stressed_expectancy": num(row, "cost_stressed_expectancy"),
        "same_move_reentry_ratio": num(row, "same_move_reentry_ratio"),
        "mfe_capture_ratio": num(full, "mfe_capture_ratio", num(row, "mfe_capture_ratio")),
        "early_net_profit": num(early, "net_profit"),
        "early_profit_factor": num(early, "profit_factor"),
        "mid_net_profit": num(mid, "net_profit"),
        "mid_profit_factor": num(mid, "profit_factor"),
        "late_net_profit": num(late, "net_profit"),
        "late_profit_factor": num(late, "profit_factor"),
        "pf_gap_to_34d": pf - LEGACY_34D["profit_factor"],
        "net_gap_to_34d": net - LEGACY_34D["net_profit"],
        "dd_gap_to_34d": dd - LEGACY_34D["max_drawdown_percent"],
        "trade_count_gap_to_34d": trades - LEGACY_34D["trade_count"],
        "dd_gap_to_stage110": dd - STAGE110_REFERENCE["max_drawdown_percent"],
        "pf_delta_vs_stage116": pf - num(source, "profit_factor"),
        "net_delta_vs_stage116": net - num(source, "net_profit"),
        "dd_delta_vs_stage116": dd - num(source, "max_drawdown_percent"),
        "trade_count_delta_vs_stage116": trades - num(source, "trade_count"),
    }


def comparison_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = [
        {
            "run_id": RUN_ID,
            "source_stage": "legacy_34d_lesson_target",
            "source_adapter_id": "",
            "adapter_id": "legacy_34d_kpi_target_not_v2_result",
            "risk_cap": "",
            "profit_factor": LEGACY_34D["profit_factor"],
            "net_profit": LEGACY_34D["net_profit"],
            "max_drawdown_percent": LEGACY_34D["max_drawdown_percent"],
            "trade_count": LEGACY_34D["trade_count"],
            "expectancy": "",
            "cost_stressed_expectancy": "",
            "same_move_reentry_ratio": "",
            "mfe_capture_ratio": "",
            "early_net_profit": "",
            "early_profit_factor": "",
            "mid_net_profit": "",
            "mid_profit_factor": "",
            "late_net_profit": "",
            "late_profit_factor": "",
            "pf_gap_to_34d": "",
            "net_gap_to_34d": "",
            "dd_gap_to_34d": "",
            "trade_count_gap_to_34d": "",
            "dd_gap_to_stage110": "",
            "pf_delta_vs_stage116": "",
            "net_delta_vs_stage116": "",
            "dd_delta_vs_stage116": "",
            "trade_count_delta_vs_stage116": "",
            "stage119_read": "lesson_only_target_not_v2_result",
        },
        {
            "run_id": RUN_ID,
            "source_stage": STAGE110_REFERENCE["source_stage"],
            "source_adapter_id": "",
            "adapter_id": STAGE110_REFERENCE["adapter_id"],
            "risk_cap": "",
            "profit_factor": STAGE110_REFERENCE["profit_factor"],
            "net_profit": STAGE110_REFERENCE["net_profit"],
            "max_drawdown_percent": STAGE110_REFERENCE["max_drawdown_percent"],
            "trade_count": STAGE110_REFERENCE["trade_count"],
            "stage119_read": "lower_dd_reference_but_lower_net_density_than_stage118",
        },
    ]
    for source in STAGE116_BASELINES.values():
        row = {
            "run_id": RUN_ID,
            "source_stage": source["source_stage"],
            "source_adapter_id": "",
            "adapter_id": source["adapter_id"],
            "risk_cap": 0.0475,
            "profit_factor": source["profit_factor"],
            "net_profit": source["net_profit"],
            "max_drawdown_percent": source["max_drawdown_percent"],
            "trade_count": source["trade_count"],
            "stage119_read": "stage116_source_anchor_before_risk_cap_compression",
        }
        rows.append(row)
    for metric in [stage118_metric(row) for row in stage118_oos_rows()]:
        rows.append({**metric, "stage119_read": read_metric(metric)})
    return rows


def read_metric(row: Mapping[str, Any]) -> str:
    source = str(row.get("source_stage", ""))
    if source != "stage118_dd_compression_density_repair":
        return str(row.get("stage119_read", "reference"))
    pf = num(row, "profit_factor")
    net = num(row, "net_profit")
    dd = num(row, "max_drawdown_percent")
    trades = num(row, "trade_count")
    keeps_pf_net = pf >= LEGACY_34D["profit_factor"] and net >= LEGACY_34D["net_profit"]
    if dd <= LEGACY_34D["max_drawdown_percent"] and not keeps_pf_net:
        return "dd_hits_34d_but_net_drops_below_34d"
    if keeps_pf_net and dd <= STAGE110_REFERENCE["max_drawdown_percent"] and trades < 250:
        return "pf_net_preserved_dd_compressed_density_gap_remains"
    if keeps_pf_net and trades >= 250:
        return "density_candidate_needs_curve_review"
    return "risk_cap_tradeoff_requires_more_repair"


def best_balanced(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [
        row
        for row in rows
        if row.get("source_stage") == "stage118_dd_compression_density_repair"
        and num(row, "profit_factor") >= LEGACY_34D["profit_factor"]
        and num(row, "net_profit") >= LEGACY_34D["net_profit"]
        and num(row, "max_drawdown_percent") <= STAGE110_REFERENCE["max_drawdown_percent"]
    ]
    return max(
        candidates,
        key=lambda row: (-num(row, "max_drawdown_percent"), num(row, "profit_factor"), num(row, "net_profit")),
        default={},
    )


def best_dd(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if row.get("source_stage") == "stage118_dd_compression_density_repair"]
    return min(candidates, key=lambda row: num(row, "max_drawdown_percent", 999.0), default={})


def density_guardrail(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [
        row
        for row in rows
        if row.get("source_stage") == "stage118_dd_compression_density_repair"
        and num(row, "profit_factor") >= LEGACY_34D["profit_factor"]
        and num(row, "net_profit") >= LEGACY_34D["net_profit"]
        and num(row, "max_drawdown_percent") <= STAGE110_REFERENCE["max_drawdown_percent"]
    ]
    return max(candidates, key=lambda row: (num(row, "trade_count"), -num(row, "max_drawdown_percent")), default={})


def decide(rows: Sequence[Mapping[str, Any]]) -> str:
    balanced = best_balanced(rows)
    if balanced:
        return "continue_post_dd_density_expansion_repair_in_stage120"
    dd = best_dd(rows)
    if dd and num(dd, "max_drawdown_percent") <= LEGACY_34D["max_drawdown_percent"]:
        return "continue_net_recovery_after_dd_compression_in_stage120"
    return "continue_dd_compression_repair_in_stage120"


def formatted_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    columns = comparison_columns()
    output = []
    for row in rows:
        out = {}
        for column in columns:
            value = row.get(column, "")
            if isinstance(value, float):
                digits = 2 if column in {"net_profit", "net_gap_to_34d", "net_delta_vs_stage116"} else 6
                if column in {"trade_count", "trade_count_gap_to_34d", "trade_count_delta_vs_stage116"}:
                    digits = 0
                out[column] = fmt(value, digits)
            else:
                out[column] = value
        output.append(out)
    return output


def comparison_columns() -> list[str]:
    return [
        "run_id",
        "source_stage",
        "source_adapter_id",
        "adapter_id",
        "risk_cap",
        "profit_factor",
        "net_profit",
        "max_drawdown_percent",
        "trade_count",
        "expectancy",
        "cost_stressed_expectancy",
        "same_move_reentry_ratio",
        "mfe_capture_ratio",
        "early_net_profit",
        "early_profit_factor",
        "mid_net_profit",
        "mid_profit_factor",
        "late_net_profit",
        "late_profit_factor",
        "pf_gap_to_34d",
        "net_gap_to_34d",
        "dd_gap_to_34d",
        "trade_count_gap_to_34d",
        "dd_gap_to_stage110",
        "pf_delta_vs_stage116",
        "net_delta_vs_stage116",
        "dd_delta_vs_stage116",
        "trade_count_delta_vs_stage116",
        "stage119_read",
    ]


def tradeoff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in rows:
        if row.get("source_stage") != "stage118_dd_compression_density_repair":
            continue
        read = str(row.get("stage119_read", ""))
        if read == "pf_net_preserved_dd_compressed_density_gap_remains":
            next_probe = "use_risk035_guardrail_for_density_expansion"
        elif read == "dd_hits_34d_but_net_drops_below_34d":
            next_probe = "do_not_use_risk030_as_primary_without_net_recovery"
        else:
            next_probe = "keep_as_failure_memory_or_secondary_control"
        output.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "source_adapter_id": row.get("source_adapter_id", ""),
                "risk_cap": fmt(num(row, "risk_cap"), 4),
                "profit_factor": fmt(num(row, "profit_factor")),
                "net_profit": fmt(num(row, "net_profit"), 2),
                "max_drawdown_percent": fmt(num(row, "max_drawdown_percent")),
                "trade_count": fmt(num(row, "trade_count"), 0),
                "dd_delta_vs_stage116": fmt(num(row, "dd_delta_vs_stage116")),
                "net_delta_vs_stage116": fmt(num(row, "net_delta_vs_stage116"), 2),
                "trade_count_gap_to_34d": fmt(num(row, "trade_count_gap_to_34d"), 0),
                "read": read,
                "next_probe": next_probe,
            }
        )
    return output


def risk_atr_summary() -> dict[str, Any]:
    rows = [row for row in read_csv(STAGE118_RISK_ATR) if row.get("split") == "oos" and row.get("view") == "actual_routed_total"]
    if not rows:
        return {"status": "missing"}
    return {
        "status": "completed",
        "atr_enabled": all(row.get("atr_enabled") == "True" for row in rows),
        "model_risk_enabled": all(row.get("model_risk_enabled") == "True" for row in rows),
        "risk_floor_applied_count": int(sum(num(row, "risk_floor_applied_count") for row in rows)),
        "max_model_risk_pct": max(num(row, "max_model_risk_pct") for row in rows),
        "max_actual_risk_pct_after_floor": max(num(row, "max_actual_risk_pct_after_floor") for row in rows),
        "risk_buckets": ",".join(sorted({row.get("risk_bucket", "") for row in rows if row.get("risk_bucket")})),
    }


def markdown_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| source(원천) | adapter(어댑터) | risk cap(위험 상한) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {source} | {adapter} | {risk} | {pf} | {net} | {dd} | {trades} | {read} |".format(
                source=row.get("source_stage", ""),
                adapter=row.get("adapter_id", ""),
                risk=row.get("risk_cap", ""),
                pf=row.get("profit_factor", ""),
                net=row.get("net_profit", ""),
                dd=row.get("max_drawdown_percent", ""),
                trades=row.get("trade_count", ""),
                read=row.get("stage119_read", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(rows: Sequence[Mapping[str, Any]], tradeoffs: Sequence[Mapping[str, Any]], risk: Mapping[str, Any], decision: str) -> str:
    balanced = best_balanced(rows)
    dd = best_dd(rows)
    density = density_guardrail(rows)
    tradeoff_text = "\n".join(f"- `{row.get('adapter_id')}`: {row.get('read')} -> {row.get('next_probe')}" for row in tradeoffs)
    return f"""# Stage119 DD Compression Follow-up Review(119단계 손실률 압축 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE118_ID}`
- source_stage118_closeout_commit(원천 118단계 종료 커밋): `{SOURCE_STAGE118_CLOSEOUT_COMMIT}`
- source_stage118_latest_commit(원천 118단계 최신 커밋): `{SOURCE_STAGE118_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage118(118단계)의 DD%(손실률) 개선이 34D KPI(34D 핵심 성과 지표) 목표를 향한 유효한 full-adapter repair(전체 어댑터 수리) 단서인가, 아니면 단순 risk scaling(위험 축소) 효과라서 density repair(밀도 수리)를 별도로 이어가야 하는가?

Effect(효과): Stage119(119단계)은 새 MT5 실행(run, 실행)을 하지 않고, 기존 Stage118 runtime evidence(실행환경 근거)를 판독해서 다음 bounded repair(경계 수리)를 정한다.

## Comparison(비교)

{markdown_table(rows)}

## Best Reads(최선 판독)

- best_balanced_candidate(균형 최선 후보): `{balanced.get('adapter_id', 'none')}` PF(수익 팩터) `{fmt(num(balanced, 'profit_factor'))}`, net(순손익) `{fmt(num(balanced, 'net_profit'), 2)}`, DD%(손실률) `{fmt(num(balanced, 'max_drawdown_percent'))}`, trades(거래 수) `{fmt(num(balanced, 'trade_count'), 0)}`.
- lowest_dd_candidate(최저 손실률 후보): `{dd.get('adapter_id', 'none')}` PF(수익 팩터) `{fmt(num(dd, 'profit_factor'))}`, net(순손익) `{fmt(num(dd, 'net_profit'), 2)}`, DD%(손실률) `{fmt(num(dd, 'max_drawdown_percent'))}`, trades(거래 수) `{fmt(num(dd, 'trade_count'), 0)}`.
- density_guardrail_candidate(밀도 가드레일 후보): `{density.get('adapter_id', 'none')}` PF(수익 팩터) `{fmt(num(density, 'profit_factor'))}`, net(순손익) `{fmt(num(density, 'net_profit'), 2)}`, DD%(손실률) `{fmt(num(density, 'max_drawdown_percent'))}`, trades(거래 수) `{fmt(num(density, 'trade_count'), 0)}`.

## Risk/ATR Telemetry(위험/ATR 텔레메트리)

- atr_enabled(ATR 켜짐): `{risk.get('atr_enabled')}`
- model_risk_enabled(모델 위험 켜짐): `{risk.get('model_risk_enabled')}`
- risk_floor_applied_count(최소 lot 바닥 적용 수): `{risk.get('risk_floor_applied_count')}`
- max_model_risk_pct(최대 모델 위험 퍼센트): `{risk.get('max_model_risk_pct')}`
- max_actual_risk_pct_after_floor(바닥 적용 뒤 최대 실제 위험 퍼센트): `{risk.get('max_actual_risk_pct_after_floor')}`
- risk_buckets(위험 버킷): `{risk.get('risk_buckets')}`

## Tradeoff(상충)

{tradeoff_text}

## Judgment(판정)

- result_subject(판정 대상): Stage118 DD compression repair(118단계 손실률 압축 수리).
- evidence_available(있는 근거): Stage118 MT5 runtime summary(실행환경 요약), segment KPI(구간 핵심 성과 지표), risk/ATR telemetry(위험/ATR 텔레메트리), Stage116/Stage110/34D comparison(비교).
- evidence_missing(부족 근거): 34D trade count(34D 거래 수) `404`에 가까운 density(밀도)와 equity-shape audit(자본 곡선 형태 감사).
- judgment_label(판정 라벨): `dd_compression_succeeded_density_gap_remains`.
- claim_boundary(주장 경계): `{BOUNDARY}`.

## Decision(판정)

decision(판정): `{decision}`

Effect(효과): Stage120(120단계)은 0.035 risk cap(위험 상한 3.5%)을 DD guardrail(손실률 가드레일)로 삼고, trade density(거래 밀도)를 회복하는 좁은 repair(수리)로 간다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str) -> str:
    return f"""# Stage119 Decision(119단계 판정)

decision(판정): `{decision}`

Stage119(119단계)은 Stage118(118단계)의 실제 MT5 runtime evidence(실행환경 근거)를 후속 검토했다.

Effect(효과): risk cap 0.035(위험 상한 3.5%)는 PF/net(수익 팩터/순손익)을 지키며 DD%(손실률)를 Stage110(110단계)보다 낮췄지만, 34D trade count(34D 거래 수)에는 아직 멀다. 따라서 다음 단계는 density expansion(밀도 확장) 수리다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`
- source_stage118_report(원천 118단계 보고서): `{rel(STAGE118_REPORT)}`
- source_stage118_decision(원천 118단계 판정): `{rel(STAGE118_DECISION)}`
- source_stage118_closeout_commit(원천 118단계 종료 커밋): `{SOURCE_STAGE118_CLOSEOUT_COMMIT}`
- source_stage118_latest_commit(원천 118단계 최신 커밋): `{SOURCE_STAGE118_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage119(119단계) 종료는 전체 목표 완료가 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 이상을 노리는 v2-native research(브이투 고유 연구)는 Stage120(120단계)로 이어진다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    rows = []
    for path in [REPORT_PATH, COMPARISON_PATH, TRADEOFF_PATH, DECISION_PATH, STAGE_LEDGER_PATH]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage119_dd_compression_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage119 v2-native DD compression follow-up review artifact.",
                }
            )
    return rows


def write_ledgers(rows: Sequence[Mapping[str, Any]], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    balanced = best_balanced(rows)
    density = density_guardrail(rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_dd_compression_followup_review",
                "status": "completed",
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage118_closeout_commit", SOURCE_STAGE118_CLOSEOUT_COMMIT),
                        ("source_stage118_latest_commit", SOURCE_STAGE118_LATEST_COMMIT),
                        ("best_balanced", balanced.get("adapter_id")),
                        ("density_guardrail", density.get("adapter_id")),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage119_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage119_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage118_mt5_runtime_evidence_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage119_dd_compression_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": decision,
            "path": rel(REPORT_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_balanced", balanced.get("adapter_id")),
                    ("best_balanced_pf", fmt(num(balanced, "profit_factor"))),
                    ("best_balanced_net", fmt(num(balanced, "net_profit"), 2)),
                    ("best_balanced_dd", fmt(num(balanced, "max_drawdown_percent"))),
                    ("density_guardrail", density.get("adapter_id")),
                )
            ),
            "guardrail_kpi": f"target_surface={TARGET_SURFACE};decision={decision}",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage119 review only; no new MT5 execution; no operational claim.",
        }
    ]
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet_files(rows: Sequence[Mapping[str, Any]], decision: str, ledger_payload: Mapping[str, Any]) -> None:
    balanced = best_balanced(rows)
    density = density_guardrail(rows)
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": ["kpi_contract_audit", "result_judgment_gate", "artifact_lineage_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "kpi_contract_audit.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "source_stage118_summary": rel(STAGE118_SUMMARY),
            "source_stage118_segments": rel(STAGE118_SEGMENTS),
            "comparison_path": rel(COMPARISON_PATH),
            "tradeoff_path": rel(TRADEOFF_PATH),
            "status": "passed_review_only",
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "judgment_label": "dd_compression_succeeded_density_gap_remains",
            "best_balanced_candidate": balanced,
            "density_guardrail_candidate": density,
            "overall_goal_complete": False,
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
                "legacy_inheritance",
            ],
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "source_stage118_closeout_commit": SOURCE_STAGE118_CLOSEOUT_COMMIT,
            "source_stage118_latest_commit": SOURCE_STAGE118_LATEST_COMMIT,
            "best_balanced_candidate": balanced.get("adapter_id"),
            "density_guardrail_candidate": density.get("adapter_id"),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def create_next_stage(decision: str) -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage120(120단계)은 Stage119(119단계)의 판정대로 post-DD density expansion repair(손실률 압축 뒤 밀도 확장 수리)를 좁게 수행한다.

## Bounded Question(경계 질문)

Stage118/119(118/119단계)에서 확인한 risk cap 0.035(위험 상한 3.5%) DD guardrail(손실률 가드레일)을 유지하면서, trade count(거래 수)를 34D target(34D 목표)에 더 가깝게 늘릴 수 있는가?

Effect(효과): Stage120(120단계)은 DD%(손실률)를 다시 망가뜨리지 않고 density(밀도)를 회복하는 작은 수리만 한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage120 Input References(120단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- stage119_report(119단계 보고서): `{rel(REPORT_PATH)}`
- stage119_comparison(119단계 비교): `{rel(COMPARISON_PATH)}`
- stage118_summary(118단계 요약): `{rel(STAGE118_SUMMARY)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage120(120단계)은 Stage119(119단계)의 판정과 Stage118(118단계)의 실제 실행 근거를 입력으로 받는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage120 Review Index(120단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage120(120단계)은 Stage119(119단계) closeout(종료 기록)을 이어받아 density expansion repair(밀도 확장 수리)를 수행한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage120 Selection Status(120단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage120(120단계)은 34D KPI(34D 핵심 성과 지표) 격차를 계속 줄이지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth(decision: str) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage119(119단계) closed(종료) as `{decision}` and Stage120(120단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): risk cap 0.035(위험 상한 3.5%) DD guardrail(손실률 가드레일)을 보존하면서 density expansion(밀도 확장) 수리로 넘긴다.
- >-
  Stage119 result(119단계 결과)는 `{rel(COMPARISON_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 기록했다. Effect(효과): Stage118 DD compression(손실률 압축)이 단독 완료가 아니라 다음 밀도 수리 입력임을 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage119_v41_dd_compression_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_stage118_closeout_commit: {SOURCE_STAGE118_CLOSEOUT_COMMIT}
  source_stage118_latest_commit: {SOURCE_STAGE118_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage119_v41_dd_compression_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage119_v41_dd_compression_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage119 Selection Status(119단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE118_ID}`
- source_decision(원천 판정): `continue_dd_compression_followup_review_in_stage119`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage119_decision(119단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage119(119단계)은 후속 검토 결과를 기록하고, 운영 의미 없이 Stage120(120단계)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage119 Review Index(119단계 검토 색인)

- status(상태): `closed_{decision}`
- source_decision(원천 판정): `continue_dd_compression_followup_review_in_stage119`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage119(119단계)은 Stage118 evidence(근거)를 판독하고 Stage120(120단계) 수리로 넘긴다.
""",
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage120_post_dd_density_expansion_repair_surface`
- status(상태): `stage119_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage119(119단계) closed(종료) as v2-native v41 DD compression follow-up review(브이투 고유 브이41 손실률 압축 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰고, 다음 연구는 Stage120(120단계) density expansion repair(밀도 확장 수리)로 이어진다.

## Latest Stage119 Evidence(최신 119단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- tradeoff_summary(상충 요약): `{rel(TRADEOFF_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage(decision)


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-18 - Stage119 v41 DD compression follow-up review closeout(119단계 v41 손실률 압축 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage118(118단계)의 위험 상한 축소 결과를 판독해 0.035 risk cap(위험 상한 3.5%)을 DD guardrail(손실률 가드레일)로 보존하고 Stage120(120단계) density expansion repair(밀도 확장 수리)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main(argv: Sequence[str] | None = None) -> int:
    del argv
    rows = comparison_rows()
    formatted = formatted_rows(rows)
    tradeoffs = tradeoff_rows(rows)
    decision = decide(rows)
    risk = risk_atr_summary()
    write_csv(COMPARISON_PATH, formatted, comparison_columns())
    write_csv(
        TRADEOFF_PATH,
        tradeoffs,
        [
            "run_id",
            "adapter_id",
            "source_adapter_id",
            "risk_cap",
            "profit_factor",
            "net_profit",
            "max_drawdown_percent",
            "trade_count",
            "dd_delta_vs_stage116",
            "net_delta_vs_stage116",
            "trade_count_gap_to_34d",
            "read",
            "next_probe",
        ],
    )
    write_md(REPORT_PATH, report_markdown(formatted, tradeoffs, risk, decision))
    write_md(DECISION_PATH, decision_markdown(decision))
    write_csv(STAGE_LEDGER_PATH, [], ALPHA_LEDGER_COLUMNS)
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(rows, decision, artifacts)
    write_packet_files(rows, decision, ledger_payload)
    write_md(REPORT_PATH, report_markdown(formatted, tradeoffs, risk, decision))
    write_md(DECISION_PATH, decision_markdown(decision))
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(rows, decision, artifacts)
    write_packet_files(rows, decision, ledger_payload)
    update_current_truth(decision)
    append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "report": rel(REPORT_PATH),
                    "comparison": rel(COMPARISON_PATH),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
