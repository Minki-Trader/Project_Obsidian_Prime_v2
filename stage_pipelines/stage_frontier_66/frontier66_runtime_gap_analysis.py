from __future__ import annotations

import csv
import json
import math
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready


STAGE_ID = "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64"
RUN_ID = "frontier66C_proxy_signal_mt5_backfill_v1"
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REVIEW_ROOT = Path("stages") / STAGE_ID / "03_reviews"
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or ["empty"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
                    for key, value in row.items()
                }
            )


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def num(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "" or text.lower() in {"nan", "inf", "-inf", "none", "null"}:
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    return parsed if math.isfinite(parsed) else None


def split_prefix(split: str) -> str:
    return "validation" if split == "validation_is" else split


def first_metric(payload: Mapping[str, Any], split: str, kind: str) -> tuple[float | None, str]:
    prefix = split_prefix(split)
    candidates = {
        "pf": (
            f"{prefix}_profit_factor",
            f"{prefix}_pf",
        ),
        "dd": (
            f"{prefix}_dd_risk_percent",
            f"{prefix}_dd_risk",
            f"{prefix}_dd",
            f"{prefix}_drawdown_percent",
            f"{prefix}_max_drawdown_percent",
        ),
        "trade_count": (
            f"{prefix}_trade_count",
            f"{prefix}_trades",
            f"{prefix}_selected_count",
        ),
        "trades_per_day": (
            f"{prefix}_trades_per_day",
            f"{prefix}_density",
            f"{prefix}_selected_density_per_day",
        ),
        "net_profit": (
            f"{prefix}_net_profit",
            f"{prefix}_profit",
        ),
    }[kind]
    for field in candidates:
        parsed = num(payload.get(field))
        if parsed is not None:
            return parsed, field
    return None, ""


def days_from_attempt(attempt: Mapping[str, Any]) -> int:
    tester = (attempt.get("ini") or {}).get("tester") or {}
    start = str(tester.get("FromDate", ""))
    end = str(tester.get("ToDate", ""))
    try:
        a = datetime.strptime(start, "%Y.%m.%d")
        b = datetime.strptime(end, "%Y.%m.%d")
    except ValueError:
        return 0
    return max((b - a).days, 0)


def gap_taxonomy_by_stage(rows: Sequence[Mapping[str, str]]) -> dict[int, str]:
    out: dict[int, str] = {}
    for row in rows:
        try:
            stage_num = int(row.get("stage_num", ""))
        except ValueError:
            continue
        out[stage_num] = row.get("expected_gap_taxonomy", "")
    return out


def status_ok(row: Mapping[str, Any]) -> bool:
    return (
        row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
        and str(row.get("blocker") or "") == ""
    )


def primary_gap(row: Mapping[str, Any], attempt: Mapping[str, Any], proxy_pf: float | None, proxy_dd: float | None) -> tuple[str, list[str]]:
    causes: list[str] = []
    if not status_ok(row):
        return "runtime_execution_blocker(런타임 실행 차단)", ["tester/runtime/report status did not all complete"]

    feature_diff = int(num(row.get("feature_ready_diff")) or 0)
    signal_diff = int(num(row.get("signal_count_diff")) or 0)
    if feature_diff != 0 or signal_diff != 0:
        return "signal_handoff_gap(신호 인계 간극)", [f"feature_diff={feature_diff}", f"signal_diff={signal_diff}"]

    causes.append("signal_handoff_exact(신호 인계 정확)")
    expected_signals = num(row.get("expected_signal_count")) or 0.0
    trade_count = num(row.get("trade_count")) or 0.0
    if expected_signals > 0 and trade_count / expected_signals < 0.75:
        causes.append("position_cap_hold_time_density_gap(단일 포지션/보유시간에 따른 거래 밀도 간극)")

    runtime_pf = num(row.get("profit_factor"))
    runtime_dd = num(row.get("max_drawdown_percent"))
    if proxy_pf is not None and runtime_pf is not None and abs(runtime_pf - proxy_pf) >= 0.25:
        causes.append("profitability_repricing_gap(수익성 재가격화 간극)")
    if proxy_dd is not None and runtime_dd is not None and abs(runtime_dd - proxy_dd) >= 5.0:
        causes.append("drawdown_basis_gap(손실폭 기준 간극)")
    if runtime_dd is not None and runtime_dd > 10.0:
        causes.append("account_risk_scaling_gap(계좌 위험 스케일 간극)")

    source_kind = str(attempt.get("source_kind", ""))
    if "trade_log" in source_kind or "lifecycle" in source_kind:
        primary = "entry_preserved_exit_risk_representation_gap(진입 보존, 청산/위험 표현 간극)"
    elif "rule_proxy" in source_kind:
        primary = "rule_proxy_execution_economics_gap(규칙 프록시 실행/경제성 간극)"
    elif "score" in source_kind or "joblib" in source_kind or "probability" in source_kind or "selection_json" in source_kind:
        primary = "signal_compression_execution_gap(신호 압축/실행 간극)"
    else:
        primary = "runtime_probe_semantics_gap(런타임 탐침 의미 간극)"
    return primary, causes


def split_rows(
    runtime_rows: Sequence[Mapping[str, str]],
    attempts: Sequence[Mapping[str, Any]],
    taxonomy: Mapping[int, str],
) -> list[dict[str, Any]]:
    attempt_by_name = {str(item["attempt_name"]): item for item in attempts}
    out: list[dict[str, Any]] = []
    for row in runtime_rows:
        attempt = attempt_by_name[str(row["attempt_name"])]
        payload = attempt.get("proxy_row_payload") or {}
        split = str(row["split"])
        proxy_pf, proxy_pf_field = first_metric(payload, split, "pf")
        proxy_dd, proxy_dd_field = first_metric(payload, split, "dd")
        proxy_trade_count, proxy_trade_count_field = first_metric(payload, split, "trade_count")
        proxy_trades_per_day, proxy_tpd_field = first_metric(payload, split, "trades_per_day")
        proxy_net_profit, proxy_net_profit_field = first_metric(payload, split, "net_profit")
        runtime_pf = num(row.get("profit_factor"))
        runtime_dd = num(row.get("max_drawdown_percent"))
        runtime_trade_count = num(row.get("trade_count"))
        runtime_net_profit = num(row.get("net_profit"))
        day_count = days_from_attempt(attempt)
        runtime_tpd = (runtime_trade_count / day_count) if runtime_trade_count is not None and day_count > 0 else None
        primary, causes = primary_gap(row, attempt, proxy_pf, proxy_dd)
        expected_signal = num(row.get("expected_signal_count"))
        signal_to_trade_ratio = (
            runtime_trade_count / expected_signal
            if runtime_trade_count is not None and expected_signal not in (None, 0)
            else None
        )
        out.append(
            {
                "stage_num": int(row["stage_num"]),
                "stage_id": row["stage_id"],
                "candidate_id": row["candidate_id"],
                "split": split,
                "source_kind": attempt.get("source_kind", ""),
                "runtime_status_triplet": f"{row['tester_status']}/{row['runtime_status']}/{row['report_status']}",
                "expected_rows": int(num(row.get("expected_rows")) or 0),
                "feature_ready_count": int(num(row.get("feature_ready_count")) or 0),
                "feature_ready_diff": int(num(row.get("feature_ready_diff")) or 0),
                "expected_signal_count": int(num(row.get("expected_signal_count")) or 0),
                "mt5_signal_count": int(num(row.get("mt5_signal_count")) or 0),
                "signal_count_diff": int(num(row.get("signal_count_diff")) or 0),
                "proxy_pf": proxy_pf,
                "runtime_pf": runtime_pf,
                "pf_delta_runtime_minus_proxy": None if proxy_pf is None or runtime_pf is None else runtime_pf - proxy_pf,
                "proxy_dd": proxy_dd,
                "runtime_dd_percent": runtime_dd,
                "dd_delta_runtime_minus_proxy": None if proxy_dd is None or runtime_dd is None else runtime_dd - proxy_dd,
                "proxy_trade_count": proxy_trade_count,
                "runtime_trade_count": runtime_trade_count,
                "trade_count_delta_runtime_minus_proxy": (
                    None if proxy_trade_count is None or runtime_trade_count is None else runtime_trade_count - proxy_trade_count
                ),
                "proxy_trades_per_day": proxy_trades_per_day,
                "runtime_trades_per_day": runtime_tpd,
                "proxy_net_profit": proxy_net_profit,
                "runtime_net_profit": runtime_net_profit,
                "signal_to_trade_ratio": signal_to_trade_ratio,
                "primary_gap": primary,
                "gap_causes": causes,
                "predeclared_gap_taxonomy": taxonomy.get(int(row["stage_num"]), ""),
                "metric_fields_used": {
                    "proxy_pf": proxy_pf_field,
                    "proxy_dd": proxy_dd_field,
                    "proxy_trade_count": proxy_trade_count_field,
                    "proxy_trades_per_day": proxy_tpd_field,
                    "proxy_net_profit": proxy_net_profit_field,
                },
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def stage_rows(split_level: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    by_stage: dict[int, list[Mapping[str, Any]]] = defaultdict(list)
    for row in split_level:
        by_stage[int(row["stage_num"])].append(row)

    out: list[dict[str, Any]] = []
    materialized = {int(row["stage_num"]): row for row in manifest_rows}
    for stage_num in sorted(materialized):
        manifest = materialized[stage_num]
        rows = by_stage.get(stage_num, [])
        if not rows:
            out.append(
                {
                    "stage_num": stage_num,
                    "stage_id": manifest.get("stage_id"),
                    "candidate_id": manifest.get("candidate_id"),
                    "stage_runtime_probe_status": manifest.get("status"),
                    "split_count": 0,
                    "completed_split_count": 0,
                    "all_signal_counts_match": "",
                    "min_runtime_pf": "",
                    "max_runtime_dd_percent": "",
                    "total_runtime_trades": "",
                    "avg_runtime_trades_per_day": "",
                    "runtime_stage_gap": "stage_logic_zero_signal_no_mt5_attempt(단계 로직상 신호 0, MT5 시도 없음)",
                    "stage_gap_causes": "stage_hypothesis_materialized_to_zero_nonflat_signal(단계 가설이 비평탄 신호 0으로 물질화됨)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue

        completed = [row for row in rows if row["runtime_status_triplet"] == "completed/completed/completed"]
        runtime_pfs = [num(row.get("runtime_pf")) for row in rows]
        runtime_pfs = [value for value in runtime_pfs if value is not None]
        runtime_dds = [num(row.get("runtime_dd_percent")) for row in rows]
        runtime_dds = [value for value in runtime_dds if value is not None]
        runtime_trades = [num(row.get("runtime_trade_count")) for row in rows]
        runtime_trades = [value for value in runtime_trades if value is not None]
        runtime_tpd = [num(row.get("runtime_trades_per_day")) for row in rows]
        runtime_tpd = [value for value in runtime_tpd if value is not None]
        signal_match = all(int(row["signal_count_diff"]) == 0 and int(row["feature_ready_diff"]) == 0 for row in rows)
        gap_counts: dict[str, int] = defaultdict(int)
        causes: dict[str, int] = defaultdict(int)
        for row in rows:
            gap_counts[str(row["primary_gap"])] += 1
            for cause in row.get("gap_causes") or []:
                causes[str(cause)] += 1
        dominant_gap = sorted(gap_counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
        out.append(
            {
                "stage_num": stage_num,
                "stage_id": rows[0].get("stage_id"),
                "candidate_id": rows[0].get("candidate_id"),
                "stage_runtime_probe_status": "completed_runtime_probe_observation(런타임 탐침 관찰 완료)",
                "split_count": len(rows),
                "completed_split_count": len(completed),
                "all_signal_counts_match": signal_match,
                "min_runtime_pf": min(runtime_pfs) if runtime_pfs else "",
                "max_runtime_dd_percent": max(runtime_dds) if runtime_dds else "",
                "total_runtime_trades": sum(runtime_trades) if runtime_trades else "",
                "avg_runtime_trades_per_day": sum(runtime_tpd) / len(runtime_tpd) if runtime_tpd else "",
                "runtime_stage_gap": dominant_gap,
                "stage_gap_causes": [f"{key}:{value}" for key, value in sorted(causes.items())],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return out


def report(split_level: Sequence[Mapping[str, Any]], stage_level: Sequence[Mapping[str, Any]]) -> str:
    completed_splits = sum(1 for row in split_level if row["runtime_status_triplet"] == "completed/completed/completed")
    signal_exact = sum(1 for row in split_level if int(row["feature_ready_diff"]) == 0 and int(row["signal_count_diff"]) == 0)
    blocked = len(split_level) - completed_splits
    high_dd = [row for row in split_level if (num(row.get("runtime_dd_percent")) or 0.0) > 10.0]
    pf_2_plus = [row for row in split_level if (num(row.get("runtime_pf")) or 0.0) >= 2.0]
    executable_stage_rows = [row for row in stage_level if num(row.get("max_runtime_dd_percent")) is not None]
    stage_high_dd = [row for row in executable_stage_rows if (num(row.get("max_runtime_dd_percent")) or 0.0) > 10.0]
    stage_min_pf_under_1 = [row for row in executable_stage_rows if (num(row.get("min_runtime_pf")) or 0.0) < 1.0]
    best_pf = sorted(split_level, key=lambda row: num(row.get("runtime_pf")) or -999.0, reverse=True)[:8]
    worst_dd = sorted(split_level, key=lambda row: num(row.get("runtime_dd_percent")) or -1.0, reverse=True)[:8]

    lines = [
        "# Frontier66 Proxy-Runtime Gap Decomposition(F66 프록시-런타임 간극 해체)",
        "",
        f"Run(실행): `{RUN_ID}`",
        "",
        "Action(행동): Stage11,15,18-49의 proxy signal(프록시 신호)을 MT5 runtime probe(런타임 탐침)로 실행하고 proxy/runtime(프록시/런타임)을 split(분할) 단위로 대조했습니다.",
        "",
        "Effect(효과): 기록 부재가 아니라 실제 MT5 실행 결과로 간극 원인을 분리합니다.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Execution Coverage(실행 커버리지)",
        "",
        f"- executable MT5 split runs(실행 가능 MT5 분할 실행): `{len(split_level)}`",
        f"- completed tester/runtime/report(테스터/런타임/보고서 완료): `{completed_splits}`",
        f"- blocked(차단): `{blocked}`",
        f"- exact feature/signal handoff(피처/신호 인계 정확): `{signal_exact}/{len(split_level)}`",
        "- logic-zero stages(로직상 신호 0 단계): `F26`, `F34`",
        "",
        "## Main Read(핵심 판독)",
        "",
        "1. Signal handoff gap(신호 인계 간극)은 이번 실행의 주 문제가 아니었습니다. 모든 실행 split(분할)에서 `feature_ready_diff=0`, `signal_count_diff=0`입니다.",
        "2. Gap(간극)의 핵심은 execution semantics(실행 의미론)입니다. Proxy(프록시)는 후보별 이벤트/점수/수익률 기반 평가였고, MT5 runtime(런타임)은 fixed lot(고정 랏), one-position cap(단일 포지션 제한), max hold(최대 보유), SL/TP(손절/익절), spread/cost(스프레드/비용), broker report DD(브로커 보고서 손실폭)를 적용했습니다.",
        "3. DD(drawdown, 손실폭) 간극은 특히 큽니다. Proxy risk percent(프록시 위험 퍼센트)와 MT5 account DD percent(계좌 손실폭 퍼센트)의 기준이 달라, 신호가 정확히 넘어가도 런타임 DD가 크게 재가격화됩니다.",
        "4. Trade density(거래 밀도)도 재압축됩니다. 많은 proxy signal bar(프록시 신호 봉)가 있어도 MT5는 포지션 보유 중 추가 진입을 하지 않아 실제 trade count(거래 수)가 줄어듭니다.",
        "",
        "## KPI Snapshot(KPI 스냅샷)",
        "",
        f"- runtime PF >= 2 split(런타임 수익 팩터 2 이상 분할): `{len(pf_2_plus)}/{len(split_level)}`",
        f"- runtime DD > 10% split(런타임 손실폭 10% 초과 분할): `{len(high_dd)}/{len(split_level)}`",
        f"- executable stages with max runtime DD > 10%(실행 단계 중 최대 런타임 손실폭 10% 초과): `{len(stage_high_dd)}/{len(executable_stage_rows)}`",
        f"- executable stages with min runtime PF < 1(실행 단계 중 최소 런타임 수익 팩터 1 미만): `{len(stage_min_pf_under_1)}/{len(executable_stage_rows)}`",
        "",
        "## Best Runtime PF Splits(런타임 수익 팩터 상위 분할)",
        "",
        "| stage | split | runtime PF | runtime DD% | trades | primary gap |",
        "|---:|---|---:|---:|---:|---|",
    ]
    for row in best_pf:
        lines.append(
            f"| F{int(row['stage_num']):02d} | {row['split']} | {num(row.get('runtime_pf')):.2f} | "
            f"{num(row.get('runtime_dd_percent')):.2f} | {num(row.get('runtime_trade_count')):.0f} | {row['primary_gap']} |"
        )
    lines.extend(
        [
            "",
            "## Worst Runtime DD Splits(런타임 손실폭 상위 분할)",
            "",
            "| stage | split | runtime PF | runtime DD% | trades | primary gap |",
            "|---:|---|---:|---:|---:|---|",
        ]
    )
    for row in worst_dd:
        lines.append(
            f"| F{int(row['stage_num']):02d} | {row['split']} | {num(row.get('runtime_pf')):.2f} | "
            f"{num(row.get('runtime_dd_percent')):.2f} | {num(row.get('runtime_trade_count')):.0f} | {row['primary_gap']} |"
        )
    lines.extend(
        [
            "",
            "## Artifacts(산출물)",
            "",
            "- split gap table(분할 간극 표): `frontier66_proxy_runtime_gap_by_split.csv`",
            "- stage gap table(단계 간극 표): `frontier66_proxy_runtime_gap_by_stage.csv`",
            "- summary JSON(요약 JSON): `frontier66_proxy_runtime_gap_summary.json`",
            "",
            "Judgment(판정): runtime_probe_observation(런타임 탐침 관찰). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    attempts = json.loads(io_path(RUN_ROOT / "frontier66_proxy_signal_mt5_attempts.json").read_text(encoding="utf-8-sig"))
    runtime = read_csv(RUN_ROOT / "frontier66_proxy_signal_runtime_rows.csv")
    manifest = read_csv(RUN_ROOT / "frontier66_proxy_signal_materialization_manifest.csv")
    taxonomy = gap_taxonomy_by_stage(read_csv(RUN_ROOT / "frontier66_pre_mt5_gap_taxonomy.csv"))
    split_level = split_rows(runtime, attempts, taxonomy)
    stage_level = stage_rows(split_level, manifest)
    split_path = RUN_ROOT / "frontier66_proxy_runtime_gap_by_split.csv"
    stage_path = RUN_ROOT / "frontier66_proxy_runtime_gap_by_stage.csv"
    summary_path = RUN_ROOT / "frontier66_proxy_runtime_gap_summary.json"
    report_path = REVIEW_ROOT / "frontier66_proxy_runtime_gap_decomposition_report.md"
    write_csv(split_path, split_level)
    write_csv(stage_path, stage_level)
    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "split_rows": len(split_level),
        "stage_rows": len(stage_level),
        "completed_split_rows": sum(1 for row in split_level if row["runtime_status_triplet"] == "completed/completed/completed"),
        "exact_signal_handoff_rows": sum(1 for row in split_level if int(row["feature_ready_diff"]) == 0 and int(row["signal_count_diff"]) == 0),
        "logic_zero_stages": [row["stage_num"] for row in stage_level if str(row["runtime_stage_gap"]).startswith("stage_logic_zero")],
        "claim_boundary": CLAIM_BOUNDARY,
        "artifacts": {
            "split_gap_table": split_path.as_posix(),
            "stage_gap_table": stage_path.as_posix(),
            "report": report_path.as_posix(),
        },
    }
    write_json(summary_path, summary)
    io_path(report_path.parent).mkdir(parents=True, exist_ok=True)
    io_path(report_path).write_text(report(split_level, stage_level), encoding="utf-8-sig")
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
