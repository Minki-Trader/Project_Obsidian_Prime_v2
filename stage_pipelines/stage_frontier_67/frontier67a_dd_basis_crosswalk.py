from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path


STAGE_ID = "stage_frontier_67__count_parity_not_pnl_parity_runtime_economics_crosswalk"
RUN_ID = "frontier67A_dd_basis_crosswalk_execution_v1"
F66_STAGE_ID = "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64"
SOURCE_SPLIT_TABLE = (
    ROOT
    / "stages"
    / F66_STAGE_ID
    / "03_reviews"
    / "frontier66_proxy_runtime_gap_by_split_review.csv"
)
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
ROWS_CSV = RUN_ROOT / "frontier67A_dd_basis_crosswalk_rows.csv"
SUMMARY_JSON = RUN_ROOT / "frontier67A_dd_basis_crosswalk_summary.json"
REPORT_MD = REVIEWS_ROOT / "frontier67A_dd_basis_crosswalk_report.md"
REVIEW_ROWS_CSV = REVIEWS_ROOT / "frontier67A_dd_basis_crosswalk_rows_review.csv"
REVIEW_SUMMARY_JSON = REVIEWS_ROOT / "frontier67A_dd_basis_crosswalk_summary_review.json"


def as_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def dd_bucket(value: float | None) -> str:
    if value is None:
        return "missing"
    if value < 10:
        return "lt10"
    if value < 20:
        return "10_to_20"
    if value < 50:
        return "20_to_50"
    return "gte50"


def basis_read(delta: float | None, proxy_dd: float | None, runtime_dd: float | None) -> str:
    if delta is None or proxy_dd is None or runtime_dd is None:
        return "missing_dd_basis"
    if abs(delta) <= 1.0:
        return "near_aligned_within_1pp"
    if runtime_dd > 10 and proxy_dd < 10:
        return "runtime_breaks_dd10_proxy_under10"
    if runtime_dd - proxy_dd >= 10:
        return "runtime_much_worse_ge10pp"
    if proxy_dd - runtime_dd >= 10:
        return "proxy_much_worse_ge10pp"
    if runtime_dd > proxy_dd:
        return "runtime_worse_lt10pp"
    return "proxy_worse_lt10pp"


def load_rows() -> list[dict[str, str]]:
    with io_path(SOURCE_SPLIT_TABLE).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def metric_payload(row: dict[str, str]) -> dict[str, Any]:
    raw = row.get("metric_fields_used") or "{}"
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def proxy_dd_family(field: str) -> str:
    if not field:
        return "missing_proxy_dd_field"
    if "risk_percent" in field:
        return "risk_percent_proxy_dd"
    if field in {"validation_dd", "oos_dd"}:
        return "generic_proxy_dd"
    if "drawdown" in field:
        return "drawdown_named_proxy_dd"
    return "other_proxy_dd_field"


def build_crosswalk(source_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in source_rows:
        metrics = metric_payload(row)
        proxy_dd = as_float(row.get("proxy_dd"))
        runtime_dd = as_float(row.get("runtime_dd_percent"))
        delta = None if proxy_dd is None or runtime_dd is None else runtime_dd - proxy_dd
        ratio = None
        if proxy_dd not in {None, 0.0} and runtime_dd is not None:
            ratio = runtime_dd / proxy_dd
        proxy_field = str(metrics.get("proxy_dd") or "")
        output.append(
            {
                "stage_num": row.get("stage_num", ""),
                "stage_id": row.get("stage_id", ""),
                "candidate_id": row.get("candidate_id", ""),
                "split": row.get("split", ""),
                "proxy_dd": proxy_dd,
                "runtime_dd_percent": runtime_dd,
                "dd_delta_runtime_minus_proxy": delta,
                "runtime_to_proxy_dd_ratio": ratio,
                "proxy_dd_bucket": dd_bucket(proxy_dd),
                "runtime_dd_bucket": dd_bucket(runtime_dd),
                "dd_basis_read": basis_read(delta, proxy_dd, runtime_dd),
                "proxy_dd_field": proxy_field,
                "proxy_dd_family": proxy_dd_family(proxy_field),
                "runtime_dd_field": "max_drawdown_percent",
                "metric_fields_used": row.get("metric_fields_used", ""),
                "gap_causes": row.get("gap_causes", ""),
                "claim_boundary": row.get("claim_boundary", ""),
            }
        )
    return output


def finite(values: list[float | None]) -> list[float]:
    return [float(value) for value in values if value is not None and math.isfinite(float(value))]


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[int(position)]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def numeric_summary(values: list[float | None]) -> dict[str, Any]:
    clean = finite(values)
    if not clean:
        return {"count": 0}
    return {
        "count": len(clean),
        "min": min(clean),
        "p25": quantile(clean, 0.25),
        "median": median(clean),
        "p75": quantile(clean, 0.75),
        "max": max(clean),
    }


def grouped_counts(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get(key) or "")].append(row)
    payload: dict[str, dict[str, Any]] = {}
    for group_key, group_rows in sorted(groups.items()):
        deltas = [row.get("dd_delta_runtime_minus_proxy") for row in group_rows]
        reads = Counter(str(row.get("dd_basis_read") or "") for row in group_rows)
        payload[group_key] = {
            "rows": len(group_rows),
            "delta_summary": numeric_summary(deltas),
            "runtime_dd_gt10_rows": sum(1 for row in group_rows if (row.get("runtime_dd_percent") or 0) > 10),
            "proxy_dd_gt10_rows": sum(1 for row in group_rows if (row.get("proxy_dd") or 0) > 10),
            "basis_reads": dict(sorted(reads.items())),
        }
    return payload


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    deltas = [row.get("dd_delta_runtime_minus_proxy") for row in rows]
    ratios = [row.get("runtime_to_proxy_dd_ratio") for row in rows]
    basis_reads = Counter(str(row.get("dd_basis_read") or "") for row in rows)
    runtime_buckets = Counter(str(row.get("runtime_dd_bucket") or "") for row in rows)
    proxy_buckets = Counter(str(row.get("proxy_dd_bucket") or "") for row in rows)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_table": str(SOURCE_SPLIT_TABLE.relative_to(ROOT)).replace("\\", "/"),
        "row_count": len(rows),
        "dd_delta_runtime_minus_proxy_summary": numeric_summary(deltas),
        "runtime_to_proxy_dd_ratio_summary": numeric_summary(ratios),
        "basis_read_counts": dict(sorted(basis_reads.items())),
        "runtime_dd_bucket_counts": dict(sorted(runtime_buckets.items())),
        "proxy_dd_bucket_counts": dict(sorted(proxy_buckets.items())),
        "runtime_dd_gt10_rows": sum(1 for row in rows if (row.get("runtime_dd_percent") or 0) > 10),
        "proxy_dd_gt10_rows": sum(1 for row in rows if (row.get("proxy_dd") or 0) > 10),
        "both_dd_under10_rows": sum(
            1
            for row in rows
            if (row.get("runtime_dd_percent") is not None and row.get("proxy_dd") is not None)
            and row["runtime_dd_percent"] < 10
            and row["proxy_dd"] < 10
        ),
        "runtime_breaks_dd10_proxy_under10_rows": sum(
            1 for row in rows if row.get("dd_basis_read") == "runtime_breaks_dd10_proxy_under10"
        ),
        "by_split": grouped_counts(rows, "split"),
        "by_proxy_dd_family": grouped_counts(rows, "proxy_dd_family"),
        "claim_boundary": "dd_basis_crosswalk_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve",
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    columns = [
        "stage_num",
        "stage_id",
        "candidate_id",
        "split",
        "proxy_dd",
        "runtime_dd_percent",
        "dd_delta_runtime_minus_proxy",
        "runtime_to_proxy_dd_ratio",
        "proxy_dd_bucket",
        "runtime_dd_bucket",
        "dd_basis_read",
        "proxy_dd_field",
        "proxy_dd_family",
        "runtime_dd_field",
        "metric_fields_used",
        "gap_causes",
        "claim_boundary",
    ]
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def fmt(value: Any) -> str:
    if value is None:
        return "missing"
    if isinstance(value, float):
        return f"{value:.4f}"
    return str(value)


def build_report(summary: dict[str, Any]) -> str:
    delta = summary["dd_delta_runtime_minus_proxy_summary"]
    ratio = summary["runtime_to_proxy_dd_ratio_summary"]
    return f"""# F67A DD Basis Crosswalk Report(F67A 손실폭 기준 대조 보고서)

- stage_id(단계 ID): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- source_table(원천 표): `{summary['source_table']}`
- row_count(행 수): `{summary['row_count']}`
- claim_boundary(주장 경계): `{summary['claim_boundary']}`

## Read(판독)

Action(행동): F66 split rows(F66 분할 행)의 proxy DD(프록시 손실폭)와 runtime DD percent(런타임 손실폭 %)를 같은 row grain(행 단위)에서 비교했다.

Effect(효과): F67B config parity(설정 동등성)와 F67C order-intent economics(주문 의도 경제성)로 가기 전에, DD gap(손실폭 차이)이 단순 scale/unit bug(스케일/단위 버그)인지 heterogeneous measurement basis(이질 측정 기준)인지 좁혔다.

- delta median(차이 중앙값): `{fmt(delta.get('median'))}`
- delta p25/p75(차이 25/75분위): `{fmt(delta.get('p25'))}` / `{fmt(delta.get('p75'))}`
- delta min/max(차이 최소/최대): `{fmt(delta.get('min'))}` / `{fmt(delta.get('max'))}`
- runtime/proxy DD ratio median(런타임/프록시 손실폭 비율 중앙값): `{fmt(ratio.get('median'))}`
- runtime DD > 10 rows(런타임 손실폭 10 초과 행): `{summary['runtime_dd_gt10_rows']}/{summary['row_count']}`
- proxy DD > 10 rows(프록시 손실폭 10 초과 행): `{summary['proxy_dd_gt10_rows']}/{summary['row_count']}`
- both DD < 10 rows(둘 다 손실폭 10 미만 행): `{summary['both_dd_under10_rows']}/{summary['row_count']}`
- runtime breaks DD10 while proxy under10(프록시 10 미만인데 런타임 10 초과): `{summary['runtime_breaks_dd10_proxy_under10_rows']}/{summary['row_count']}`

## Basis Read Counts(기준 판독 수)

```json
{json.dumps(summary['basis_read_counts'], ensure_ascii=False, indent=2)}
```

## Proxy DD Families(프록시 손실폭 계열)

```json
{json.dumps(summary['by_proxy_dd_family'], ensure_ascii=False, indent=2)}
```

## Next Action(다음 행동)

F67A does not close(마감 아님). Next action(다음 행동)은 F67B config parity depth pilot(설정 동등성 깊이 파일럿)에서 spread/commission/slippage/modeling/deposit/leverage(스프레드/수수료/슬리피지/모델링/예치금/레버리지)를 row sample(행 표본) 기준으로 대조하는 것이다. F67 closeout(마감) 전에는 별도 MT5 Runtime Probe(MT5 런타임 탐침)가 필요하다.
"""


def main() -> int:
    source_rows = load_rows()
    crosswalk_rows = build_crosswalk(source_rows)
    summary = build_summary(crosswalk_rows)

    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(REVIEWS_ROOT).mkdir(parents=True, exist_ok=True)
    write_csv(ROWS_CSV, crosswalk_rows)
    write_csv(REVIEW_ROWS_CSV, crosswalk_rows)
    io_path(SUMMARY_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    io_path(REVIEW_SUMMARY_JSON).write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    io_path(REPORT_MD).write_text(build_report(summary), encoding="utf-8-sig")
    print(json.dumps({"run_id": RUN_ID, "row_count": len(crosswalk_rows), "report": str(REPORT_MD)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
