from __future__ import annotations

import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path


STAGE_ID = "stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk"
RUN_ID = "frontier67B_config_parity_depth_pilot_v1"
F66_STAGE_ID = "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64"
F66_RUN_ID = "frontier66C_proxy_signal_mt5_backfill_v1"
F66_RUN_ROOT = ROOT / "stages" / F66_STAGE_ID / "02_runs" / F66_RUN_ID
F67_STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = F67_STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = F67_STAGE_ROOT / "03_reviews"

ATTEMPTS_JSON = F66_RUN_ROOT / "frontier66_proxy_signal_mt5_attempts.json"
F67A_ROWS = REVIEWS_ROOT / "frontier67A_dd_basis_crosswalk_rows_review.csv"
RUNTIME_ROWS = ROOT / "stages" / F66_STAGE_ID / "03_reviews" / "frontier66_proxy_signal_runtime_rows_review.csv"

ROWS_CSV = RUN_ROOT / "frontier67B_config_parity_rows.csv"
SUMMARY_JSON = RUN_ROOT / "frontier67B_config_parity_summary.json"
REPORT_MD = REVIEWS_ROOT / "frontier67B_config_parity_depth_pilot_report.md"
REVIEW_ROWS_CSV = REVIEWS_ROOT / "frontier67B_config_parity_rows_review.csv"
REVIEW_SUMMARY_JSON = REVIEWS_ROOT / "frontier67B_config_parity_summary_review.json"

TESTER_FIELDS = (
    "Symbol",
    "Period",
    "Model",
    "Deposit",
    "Leverage",
    "Optimization",
    "ExecutionMode",
    "ForwardMode",
    "UseLocal",
    "UseRemote",
    "UseCloud",
)
SET_FIELDS = (
    "InpFixedLot",
    "InpMaxConcurrentPositions",
    "InpMaxHoldBars",
    "InpAtrSltpEnabled",
    "InpAtrStopMultiplier",
    "InpAtrTakeProfitMultiplier",
    "InpModelBackend",
    "InpFeatureCount",
    "InpDecisionMode",
    "InpEntryTransitionOnly",
    "InpReentryCooldownBars",
    "InpSameDirectionReentryCooldownBars",
)
COST_FIELDS = ("Spread", "Commission", "Slippage", "Swap")


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_set_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def key(stage_num: Any, split: Any) -> tuple[str, str]:
    return str(stage_num), str(split)


def counter_payload(values: list[Any]) -> dict[str, int]:
    return dict(sorted(Counter("missing" if value in {None, ""} else str(value) for value in values).items()))


def grouped_counts(rows: list[dict[str, Any]], group_field: str) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(group_field) or "missing")].append(row)
    output: dict[str, dict[str, Any]] = {}
    for group, group_rows in sorted(grouped.items()):
        basis_reads = Counter(str(row.get("dd_basis_read") or "missing") for row in group_rows)
        output[group] = {
            "rows": len(group_rows),
            "runtime_dd_gt10_rows": sum(1 for row in group_rows if row.get("runtime_dd_gt10") == "true"),
            "proxy_under10_runtime_gt10_rows": sum(
                1 for row in group_rows if row.get("dd_basis_read") == "runtime_breaks_dd10_proxy_under10"
            ),
            "basis_reads": dict(sorted(basis_reads.items())),
        }
    return output


def build_rows() -> list[dict[str, Any]]:
    attempts = read_json(ATTEMPTS_JSON)
    f67a_by_key = {key(row.get("stage_num"), row.get("split")): row for row in read_csv(F67A_ROWS)}
    runtime_by_key = {key(row.get("stage_num"), row.get("split")): row for row in read_csv(RUNTIME_ROWS)}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        stage_split_key = key(attempt.get("stage_num"), attempt.get("split"))
        tester = dict((attempt.get("ini") or {}).get("tester") or {})
        set_path = ROOT / str((attempt.get("set") or {}).get("path") or "")
        set_values = read_set_values(set_path) if str(set_path) else {}
        extra_values = dict(attempt.get("extra_set_values") or {})
        for field, value in extra_values.items():
            set_values.setdefault(field, str(value))
        f67a_row = f67a_by_key.get(stage_split_key, {})
        runtime_row = runtime_by_key.get(stage_split_key, {})
        cost_presence = {field: ("present" if field in tester or field in set_values else "missing") for field in COST_FIELDS}
        rows.append(
            {
                "stage_num": str(attempt.get("stage_num") or ""),
                "stage_id": str(attempt.get("stage_id") or ""),
                "candidate_id": str(attempt.get("candidate_id") or ""),
                "split": str(attempt.get("split") or ""),
                "attempt_name": str(attempt.get("attempt_name") or ""),
                "symbol": tester.get("Symbol", ""),
                "period": tester.get("Period", ""),
                "model": tester.get("Model", ""),
                "deposit": tester.get("Deposit", ""),
                "leverage": tester.get("Leverage", ""),
                "optimization": tester.get("Optimization", ""),
                "execution_mode": tester.get("ExecutionMode", ""),
                "use_local": tester.get("UseLocal", ""),
                "use_remote": tester.get("UseRemote", ""),
                "use_cloud": tester.get("UseCloud", ""),
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "report": tester.get("Report", ""),
                "set_path": (attempt.get("set") or {}).get("path", ""),
                "set_sha256": (attempt.get("set") or {}).get("sha256", ""),
                "ini_path": (attempt.get("ini") or {}).get("path", ""),
                "ini_sha256": (attempt.get("ini") or {}).get("sha256", ""),
                "fixed_lot": set_values.get("InpFixedLot", ""),
                "max_positions": set_values.get("InpMaxConcurrentPositions", ""),
                "max_hold_bars": set_values.get("InpMaxHoldBars", str(attempt.get("max_hold_bars") or "")),
                "atr_sltp_enabled": set_values.get("InpAtrSltpEnabled", ""),
                "atr_stop_multiplier": set_values.get("InpAtrStopMultiplier", ""),
                "atr_take_profit_multiplier": set_values.get("InpAtrTakeProfitMultiplier", ""),
                "model_backend": set_values.get("InpModelBackend", ""),
                "feature_count": set_values.get("InpFeatureCount", ""),
                "decision_mode": set_values.get("InpDecisionMode", ""),
                "entry_transition_only": set_values.get("InpEntryTransitionOnly", ""),
                "reentry_cooldown": set_values.get("InpReentryCooldownBars", ""),
                "same_direction_reentry_cooldown": set_values.get("InpSameDirectionReentryCooldownBars", ""),
                "spread_identity": cost_presence["Spread"],
                "commission_identity": cost_presence["Commission"],
                "slippage_identity": cost_presence["Slippage"],
                "swap_identity": cost_presence["Swap"],
                "runtime_dd_percent": f67a_row.get("runtime_dd_percent", runtime_row.get("max_drawdown_percent", "")),
                "proxy_dd": f67a_row.get("proxy_dd", ""),
                "dd_basis_read": f67a_row.get("dd_basis_read", "missing_dd_basis_read"),
                "runtime_dd_gt10": "true"
                if float(f67a_row.get("runtime_dd_percent") or runtime_row.get("max_drawdown_percent") or 0) > 10
                else "false",
                "runtime_trade_count": runtime_row.get("trade_count", ""),
                "runtime_pf": runtime_row.get("profit_factor", ""),
                "runtime_net_profit": runtime_row.get("net_profit", ""),
            }
        )
    return rows


def unique_signature_count(rows: list[dict[str, Any]], fields: tuple[str, ...]) -> int:
    return len({tuple(str(row.get(field) or "") for field in fields) for row in rows})


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tester_summary = {field: counter_payload([row.get(field.lower() if field != "UseLocal" else "use_local") for row in rows]) for field in ()}
    tester_field_map = {
        "Symbol": "symbol",
        "Period": "period",
        "Model": "model",
        "Deposit": "deposit",
        "Leverage": "leverage",
        "Optimization": "optimization",
        "ExecutionMode": "execution_mode",
        "UseLocal": "use_local",
        "UseRemote": "use_remote",
        "UseCloud": "use_cloud",
    }
    tester_summary = {
        field: counter_payload([row.get(column) for row in rows]) for field, column in tester_field_map.items()
    }
    set_summary = {
        "InpFixedLot": counter_payload([row.get("fixed_lot") for row in rows]),
        "InpMaxConcurrentPositions": counter_payload([row.get("max_positions") for row in rows]),
        "InpMaxHoldBars": counter_payload([row.get("max_hold_bars") for row in rows]),
        "InpAtrSltpEnabled": counter_payload([row.get("atr_sltp_enabled") for row in rows]),
        "InpAtrStopMultiplier": counter_payload([row.get("atr_stop_multiplier") for row in rows]),
        "InpAtrTakeProfitMultiplier": counter_payload([row.get("atr_take_profit_multiplier") for row in rows]),
        "InpModelBackend": counter_payload([row.get("model_backend") for row in rows]),
        "InpFeatureCount": counter_payload([row.get("feature_count") for row in rows]),
        "InpDecisionMode": counter_payload([row.get("decision_mode") for row in rows]),
    }
    cost_identity = {
        "spread": counter_payload([row.get("spread_identity") for row in rows]),
        "commission": counter_payload([row.get("commission_identity") for row in rows]),
        "slippage": counter_payload([row.get("slippage_identity") for row in rows]),
        "swap": counter_payload([row.get("swap_identity") for row in rows]),
    }
    uniform_tester_fields = [
        field
        for field, counts in tester_summary.items()
        if len(counts) == 1 and "missing" not in counts
    ]
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_attempts": str(ATTEMPTS_JSON.relative_to(ROOT)).replace("\\", "/"),
        "source_f67a_rows": str(F67A_ROWS.relative_to(ROOT)).replace("\\", "/"),
        "row_count": len(rows),
        "tester_summary": tester_summary,
        "set_summary": set_summary,
        "cost_identity": cost_identity,
        "uniform_tester_fields": uniform_tester_fields,
        "tester_signature_count": unique_signature_count(
            rows,
            (
                "symbol",
                "period",
                "model",
                "deposit",
                "leverage",
                "optimization",
                "execution_mode",
                "use_local",
                "use_remote",
                "use_cloud",
            ),
        ),
        "ea_core_signature_count": unique_signature_count(
            rows,
            ("fixed_lot", "max_positions", "model_backend", "feature_count", "decision_mode"),
        ),
        "trade_shape_signature_count": unique_signature_count(
            rows,
            (
                "max_hold_bars",
                "atr_sltp_enabled",
                "atr_stop_multiplier",
                "atr_take_profit_multiplier",
                "entry_transition_only",
                "reentry_cooldown",
                "same_direction_reentry_cooldown",
            ),
        ),
        "by_max_hold_bars": grouped_counts(rows, "max_hold_bars"),
        "by_atr_sltp_enabled": grouped_counts(rows, "atr_sltp_enabled"),
        "by_fixed_lot": grouped_counts(rows, "fixed_lot"),
        "config_gap_read": (
            "tester_identity_uniform_but_explicit_cost_fields_missing"
            if all(counts == {"missing": len(rows)} for counts in cost_identity.values())
            else "tester_identity_uniform_with_some_cost_fields_present"
        ),
        "claim_boundary": "config_parity_depth_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve",
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    columns = [
        "stage_num",
        "stage_id",
        "candidate_id",
        "split",
        "attempt_name",
        "symbol",
        "period",
        "model",
        "deposit",
        "leverage",
        "optimization",
        "execution_mode",
        "use_local",
        "use_remote",
        "use_cloud",
        "from_date",
        "to_date",
        "report",
        "set_path",
        "set_sha256",
        "ini_path",
        "ini_sha256",
        "fixed_lot",
        "max_positions",
        "max_hold_bars",
        "atr_sltp_enabled",
        "atr_stop_multiplier",
        "atr_take_profit_multiplier",
        "model_backend",
        "feature_count",
        "decision_mode",
        "entry_transition_only",
        "reentry_cooldown",
        "same_direction_reentry_cooldown",
        "spread_identity",
        "commission_identity",
        "slippage_identity",
        "swap_identity",
        "runtime_dd_percent",
        "proxy_dd",
        "dd_basis_read",
        "runtime_dd_gt10",
        "runtime_trade_count",
        "runtime_pf",
        "runtime_net_profit",
    ]
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def build_report(summary: dict[str, Any]) -> str:
    return f"""# F67B Config Parity Depth Pilot(F67B 설정 동등성 깊이 파일럿)

- stage_id(단계 ID): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- source_attempts(원천 시도 목록): `{summary['source_attempts']}`
- source_f67a_rows(F67A 원천 행): `{summary['source_f67a_rows']}`
- row_count(행 수): `{summary['row_count']}`
- claim_boundary(주장 경계): `{summary['claim_boundary']}`

## Read(판독)

Action(행동): F66 MT5 attempts(F66 MT5 시도) `64`개에서 generated `.ini/.set` identity(생성 설정 정체성)와 F67A DD basis rows(F67A 손실폭 기준 행)를 결합했다.

Effect(효과): DD gap(손실폭 간극)이 tester identity drift(테스터 정체성 드리프트)인지, intentional trade-shape config variation(의도된 거래 형태 설정 차이)인지, explicit cost identity missing(명시 비용 정체성 누락)인지 분리했다.

- tester_signature_count(테스터 정체성 서명 수): `{summary['tester_signature_count']}`
- EA core signature count(EA 핵심 설정 서명 수): `{summary['ea_core_signature_count']}`
- trade_shape_signature_count(거래 형태 설정 서명 수): `{summary['trade_shape_signature_count']}`
- config_gap_read(설정 간극 판독): `{summary['config_gap_read']}`

## Tester Summary(테스터 요약)

```json
{json.dumps(summary['tester_summary'], ensure_ascii=False, indent=2)}
```

## EA Set Summary(EA 설정 요약)

```json
{json.dumps(summary['set_summary'], ensure_ascii=False, indent=2)}
```

## Cost Identity(비용 정체성)

```json
{json.dumps(summary['cost_identity'], ensure_ascii=False, indent=2)}
```

## DD By Trade Shape(거래 형태별 손실폭)

```json
{json.dumps({'by_max_hold_bars': summary['by_max_hold_bars'], 'by_atr_sltp_enabled': summary['by_atr_sltp_enabled']}, ensure_ascii=False, indent=2)}
```

## Next Action(다음 행동)

F67B does not close(마감 아님). Next action(다음 행동)은 F67C runtime-native order intent economics(런타임 기반 주문 의도 경제성) 또는 narrow MT5 Runtime Probe(MT5 런타임 탐침) 설계 전에, missing explicit spread/commission/slippage identity(명시 스프레드/수수료/슬리피지 정체성 누락)를 tester report/report parser(테스터 보고서/보고서 파서)에서 보강할 수 있는지 확인하는 것이다. F67 closeout(마감) 전에는 별도 MT5 Runtime Probe(MT5 런타임 탐침)가 필요하다.
"""


def main() -> int:
    rows = build_rows()
    summary = build_summary(rows)
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS_ROOT).mkdir(parents=True, exist_ok=True)
    write_csv(ROWS_CSV, rows)
    write_csv(REVIEW_ROWS_CSV, rows)
    io_path(SUMMARY_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    io_path(REVIEW_SUMMARY_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    io_path(REPORT_MD).write_text(build_report(summary), encoding="utf-8-sig")
    print(json.dumps({"run_id": RUN_ID, "row_count": len(rows), "report": str(REPORT_MD)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
