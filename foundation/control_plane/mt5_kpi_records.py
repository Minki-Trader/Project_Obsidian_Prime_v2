from __future__ import annotations

import math
from typing import Any, Mapping, Sequence


TIER_A = "Tier A"
TIER_B = "Tier B"
TIER_AB = "Tier A+B"
ROUTING_MODE_A_B_FALLBACK = "tier_a_primary_tier_b_fallback"
ROUTING_MODE_A_ONLY = "tier_a_primary_no_fallback"


def _to_int(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, float) and not math.isfinite(value):
        return 0
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def _first_present(source: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in source and source.get(key) is not None:
            return source.get(key)
    return None


def mt5_metrics_with_runtime_counts(result: Mapping[str, Any]) -> dict[str, Any]:
    metrics = dict(result.get("strategy_tester_report", {}).get("metrics", {}))
    last_summary = result.get("runtime_outputs", {}).get("last_summary", {})
    order_attempt_count = _to_int(_first_present(last_summary, "order_attempt_count"))
    order_fill_count = _to_int(_first_present(last_summary, "order_fill_count", "fill_count"))
    feature_skip_count = _to_int(_first_present(last_summary, "feature_skip_count", "skip_count"))
    reject_count = max(order_attempt_count - order_fill_count, 0)
    metrics.update(
        {
            "order_attempt_count": order_attempt_count,
            "fill_count": order_fill_count,
            "reject_count": reject_count,
            "skip_count": feature_skip_count,
            "fill_rate": float(order_fill_count / order_attempt_count) if order_attempt_count else None,
            "feature_ready_count": _to_int(last_summary.get("feature_ready_count")),
            "model_ok_count": _to_int(last_summary.get("model_ok_count")),
            "model_fail_count": _to_int(last_summary.get("model_fail_count")),
            "tier_a_used_count": _to_int(last_summary.get("tier_a_used_count")),
            "tier_b_fallback_used_count": _to_int(last_summary.get("tier_b_fallback_used_count")),
            "no_tier_count": _to_int(last_summary.get("no_tier_count")),
            "tier_a_long_count": _to_int(last_summary.get("tier_a_long_count")),
            "tier_a_short_count": _to_int(last_summary.get("tier_a_short_count")),
            "tier_a_flat_count": _to_int(last_summary.get("tier_a_flat_count")),
            "tier_a_order_attempt_count": _to_int(last_summary.get("tier_a_order_attempt_count")),
            "tier_a_order_fill_count": _to_int(_first_present(last_summary, "tier_a_order_fill_count", "tier_a_fill_count")),
            "tier_b_fallback_long_count": _to_int(last_summary.get("tier_b_fallback_long_count")),
            "tier_b_fallback_short_count": _to_int(last_summary.get("tier_b_fallback_short_count")),
            "tier_b_fallback_flat_count": _to_int(last_summary.get("tier_b_fallback_flat_count")),
            "tier_b_fallback_order_attempt_count": _to_int(last_summary.get("tier_b_fallback_order_attempt_count")),
            "tier_b_fallback_order_fill_count": _to_int(
                _first_present(last_summary, "tier_b_fallback_order_fill_count", "tier_b_fallback_fill_count")
            ),
        }
    )
    return metrics


def routed_component_metrics(total_metrics: Mapping[str, Any], route_role: str) -> dict[str, Any]:
    if route_role == "primary_used":
        prefix = "tier_a"
        tier_scope = TIER_A
        record_status = "completed"
    elif route_role == "fallback_used":
        prefix = "tier_b_fallback"
        tier_scope = TIER_B
        record_status = "completed"
    else:
        raise ValueError(f"Unsupported route_role: {route_role}")

    used_count = _to_int(total_metrics.get(f"{prefix}_used_count"))
    long_count = _to_int(total_metrics.get(f"{prefix}_long_count"))
    short_count = _to_int(total_metrics.get(f"{prefix}_short_count"))
    flat_count = _to_int(total_metrics.get(f"{prefix}_flat_count"))
    order_attempt_count = _to_int(total_metrics.get(f"{prefix}_order_attempt_count"))
    fill_count = _to_int(total_metrics.get(f"{prefix}_order_fill_count"))
    route_denominator = _to_int(total_metrics.get("model_ok_count")) or (
        _to_int(total_metrics.get("tier_a_used_count")) + _to_int(total_metrics.get("tier_b_fallback_used_count"))
    )
    return {
        "status": record_status,
        "tier_scope": tier_scope,
        "route_role": route_role,
        "aggregation": "actual_routed_component",
        "profit_attribution": "not_separable_from_single_routed_account_path",
        "net_profit": None,
        "profit_factor": None,
        "expectancy": None,
        "trade_count": None,
        "win_rate_percent": None,
        "max_drawdown_amount": None,
        "max_drawdown_percent": None,
        "recovery_factor": None,
        "route_bar_count": used_count,
        "route_share": float(used_count / route_denominator) if route_denominator else None,
        "signal_count": long_count + short_count,
        "long_count": long_count,
        "short_count": short_count,
        "flat_count": flat_count,
        "order_attempt_count": order_attempt_count,
        "fill_count": fill_count,
        "reject_count": max(order_attempt_count - fill_count, 0),
        "skip_count": 0,
        "fill_rate": float(fill_count / order_attempt_count) if order_attempt_count else None,
    }


def build_mt5_kpi_records(execution_results: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for result in execution_results:
        if result.get("status") != "completed":
            continue
        tier = str(result.get("tier"))
        split = str(result.get("split"))
        metrics = mt5_metrics_with_runtime_counts(result)
        routing_mode = result.get("routing_mode")
        if routing_mode in {ROUTING_MODE_A_B_FALLBACK, ROUTING_MODE_A_ONLY}:
            component_specs = [("primary_used", f"mt5_routed_tier_a_used_{split}", TIER_A)]
            if routing_mode == ROUTING_MODE_A_B_FALLBACK:
                component_specs.append(("fallback_used", f"mt5_routed_tier_b_fallback_used_{split}", TIER_B))
            for route_role, record_view, tier_scope in component_specs:
                component = routed_component_metrics(metrics, route_role)
                records.append(
                    {
                        "record_view": record_view,
                        "tier_scope": tier_scope,
                        "split": split,
                        "status": component["status"],
                        "route_role": route_role,
                        "metrics": component,
                        "report": {
                            "aggregation": "actual_routed_component",
                            "source_report": result.get("strategy_tester_report", {}),
                            "profit_attribution": component["profit_attribution"],
                        },
                    }
                )
            metrics["aggregation"] = "actual_routed_tester_run"
            metrics["route_role"] = "routed_total"
            records.append(
                {
                    "record_view": f"mt5_routed_total_{split}",
                    "tier_scope": TIER_AB,
                    "split": split,
                    "status": metrics.get("status", "partial"),
                    "route_role": "routed_total",
                    "metrics": metrics,
                    "report": result.get("strategy_tester_report", {}),
                }
            )
            continue
        metrics["aggregation"] = "actual_tier_only_tester_run"
        metrics["route_role"] = result.get("attempt_role", "tier_only_total")
        record_view_prefix = str(
            result.get("record_view_prefix") or f"mt5_{tier.lower().replace(' ', '_').replace('+', 'ab')}"
        )
        records.append(
            {
                "record_view": f"{record_view_prefix}_{split}",
                "tier_scope": tier,
                "split": split,
                "status": metrics.get("status", "partial"),
                "route_role": result.get("attempt_role", "tier_only_total"),
                "metrics": metrics,
                "report": result.get("strategy_tester_report", {}),
            }
        )
    return records


def enrich_mt5_kpi_records_with_route_coverage(
    records: Sequence[dict[str, Any]],
    route_coverage: Mapping[str, Any],
) -> list[dict[str, Any]]:
    split_aliases = {"validation_is": "validation", "validation": "validation", "oos": "oos", "train": "train"}
    by_split = route_coverage.get("by_split", {})
    subtype_by_split = route_coverage.get("tier_b_fallback_by_split_subtype", {})
    no_tier_by_split = route_coverage.get("no_tier_by_split", {})
    for record in records:
        split = split_aliases.get(str(record.get("split")), str(record.get("split")))
        metrics = record.setdefault("metrics", {})
        split_summary = dict(by_split.get(split, {})) if isinstance(by_split, Mapping) else {}
        metrics["route_coverage_split"] = split
        metrics["tier_a_primary_labelable_rows"] = split_summary.get("tier_a_primary_rows")
        metrics["tier_b_fallback_labelable_rows"] = split_summary.get("tier_b_fallback_rows")
        metrics["no_tier_labelable_rows"] = no_tier_by_split.get(split)
        metrics["routed_labelable_rows"] = split_summary.get("routed_labelable_rows")
        if record.get("route_role") in {"fallback_used", "routed_total", "tier_b_fallback_only_total"}:
            metrics["partial_context_subtype_counts"] = subtype_by_split.get(split, {})
    return list(records)
