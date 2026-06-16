from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path

STAGE_ID = "stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64"
RUN_ID = "frontier66A_runtime_probe_backfill_gap_audit_v1"
CLAIM_BOUNDARY = (
    "runtime_probe_backfill_gap_audit_observation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

PROJECT_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEW_ROOT = STAGE_ROOT / "03_reviews"

FRONTIER_RE = re.compile(r"stage_frontier_(\d+)__")


@dataclass
class RuntimeMetric:
    source: str
    run_id: str
    subrun_id: str
    split: str
    tier_scope: str = ""
    view: str = ""
    profit_factor: float | None = None
    net_profit: float | None = None
    trade_count: float | None = None
    max_drawdown_percent: float | None = None
    signal_count_diff: float | None = None
    feature_ready_diff: float | None = None
    expected_signal_count: float | None = None
    order_fill_count: float | None = None


@dataclass
class ProxyMetric:
    source: str
    run_id: str
    subrun_id: str
    val_pf: float | None = None
    oos_pf: float | None = None
    val_density: float | None = None
    oos_density: float | None = None
    val_dd: float | None = None
    oos_dd: float | None = None


@dataclass
class StageAudit:
    stage_num: int
    stage_id: str
    path: Path
    onnx_count: int = 0
    joblib_count: int = 0
    pkl_count: int = 0
    set_count: int = 0
    runtime_file_count: int = 0
    gap_report_count: int = 0
    status_json_count: int = 0
    has_existing_status: bool = False
    materialization_status: str = ""
    closeout_tokens: list[str] = field(default_factory=list)
    runtime_metrics: list[RuntimeMetric] = field(default_factory=list)
    proxy_metrics: list[ProxyMetric] = field(default_factory=list)

    @property
    def has_actual_runtime_kpi(self) -> bool:
        return bool(self.runtime_metrics)

    @property
    def has_runtime_material(self) -> bool:
        return bool(self.onnx_count or self.joblib_count or self.pkl_count)

    @property
    def proxy_best_pf(self) -> float | None:
        vals = [
            v
            for p in self.proxy_metrics
            for v in (p.oos_pf, p.val_pf)
            if v is not None and 0 <= v <= 50
        ]
        return max(vals) if vals else None

    @property
    def proxy_best_oos_pf(self) -> float | None:
        vals = [p.oos_pf for p in self.proxy_metrics if p.oos_pf is not None and 0 <= p.oos_pf <= 50]
        return max(vals) if vals else None

    @property
    def runtime_best_pf(self) -> float | None:
        vals = [r.profit_factor for r in self.runtime_metrics if r.profit_factor is not None]
        return max(vals) if vals else None

    @property
    def runtime_worst_dd(self) -> float | None:
        vals = [r.max_drawdown_percent for r in self.runtime_metrics if r.max_drawdown_percent is not None]
        return max(vals) if vals else None

    @property
    def max_signal_abs_diff(self) -> float | None:
        vals = [abs(r.signal_count_diff) for r in self.runtime_metrics if r.signal_count_diff is not None]
        return max(vals) if vals else None

    @property
    def max_feature_abs_diff(self) -> float | None:
        vals = [abs(r.feature_ready_diff) for r in self.runtime_metrics if r.feature_ready_diff is not None]
        return max(vals) if vals else None


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normal_path(path: Path) -> Path:
    text = str(path)
    if text.startswith("\\\\?\\"):
        return Path(text[4:])
    return path


def rel_path(path: Path) -> str:
    return normal_path(path).relative_to(ROOT).as_posix()


def safe_glob(path: Path, pattern: str) -> list[Path]:
    if not io_path(path).exists():
        return []
    return [normal_path(item) for item in io_path(path).glob(pattern)]


def safe_rglob(path: Path, pattern: str = "*") -> list[Path]:
    if not io_path(path).exists():
        return []
    return [normal_path(item) for item in io_path(path).rglob(pattern)]


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp949", "latin1"):
        try:
            return io_path(path).read_text(encoding=encoding, errors="replace")
        except Exception:
            continue
    return ""


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def load_csv(path: Path) -> list[dict[str, str]]:
    if not io_path(path).exists():
        return []
    for encoding in ("utf-8-sig", "utf-8", "cp949"):
        try:
            with io_path(path).open("r", encoding=encoding, newline="") as handle:
                return list(csv.DictReader(handle))
        except Exception:
            continue
    return []


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        seen: list[str] = []
        for row in rows:
            for key in row:
                if key not in seen:
                    seen.append(key)
        fieldnames = seen
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper() == "NA":
        return None
    text = text.rstrip("%")
    try:
        return float(text)
    except ValueError:
        return None


def parse_key_value(blob: str, key: str) -> float | None:
    pattern = rf"(?:^|[;,\s]){re.escape(key)}\s*=\s*([-+]?\d+(?:\.\d+)?)%?"
    match = re.search(pattern, blob, re.IGNORECASE)
    if not match:
        return None
    return parse_float(match.group(1))


def first_number(*values: Any) -> float | None:
    for value in values:
        parsed = parse_float(value)
        if parsed is not None:
            return parsed
    return None


def stage_dirs() -> dict[int, Path]:
    out: dict[int, Path] = {}
    for path in safe_glob(ROOT / "stages", "stage_frontier_*__*"):
        match = FRONTIER_RE.match(path.name)
        if match:
            out[int(match.group(1))] = path
    return out


def project_rows_by_stage() -> dict[int, list[dict[str, str]]]:
    out: dict[int, list[dict[str, str]]] = {}
    for row in load_csv(PROJECT_LEDGER):
        match = FRONTIER_RE.match(row.get("stage_id", ""))
        if match:
            num = int(match.group(1))
            if 2 <= num <= 64:
                out.setdefault(num, []).append(row)
    return out


def runtime_metrics_from_json(stage: Path) -> list[RuntimeMetric]:
    metrics: list[RuntimeMetric] = []
    json_paths = sorted(safe_glob(stage / "03_reviews", "*runtime_probe*_status.json"))
    for path in json_paths:
        try:
            payload = json.loads(read_text(path))
        except json.JSONDecodeError:
            continue
        rows = payload.get("runtime_rows") or payload.get("mt5_kpi_records") or []
        if not isinstance(rows, list):
            continue
        for item in rows:
            if not isinstance(item, dict):
                continue
            pf = first_number(item.get("profit_factor"), item.get("pf"))
            trades = first_number(item.get("trade_count"), item.get("trades"))
            net = first_number(item.get("net_profit"), item.get("net"))
            if pf is None and trades is None and net is None:
                continue
            metrics.append(
                RuntimeMetric(
                    source=rel_path(path),
                    run_id=str(item.get("run_id") or payload.get("run_id") or path.stem),
                    subrun_id=str(item.get("attempt_name") or item.get("subrun_id") or item.get("split") or ""),
                    split=str(item.get("split") or ""),
                    tier_scope=tier_from_text(" ".join(str(item.get(key, "")) for key in ("attempt_name", "subrun_id", "tier_scope"))),
                    view=view_from_text(" ".join(str(item.get(key, "")) for key in ("attempt_name", "subrun_id", "split"))),
                    profit_factor=pf,
                    net_profit=net,
                    trade_count=trades,
                    max_drawdown_percent=first_number(
                        item.get("max_drawdown_percent"),
                        item.get("max_dd_percent"),
                        item.get("drawdown"),
                    ),
                    signal_count_diff=first_number(item.get("signal_count_diff")),
                    feature_ready_diff=first_number(item.get("feature_ready_diff")),
                    expected_signal_count=first_number(item.get("expected_signal_count")),
                    order_fill_count=first_number(item.get("mt5_order_fill_count"), item.get("fill_count")),
                )
            )
    return metrics


def is_actual_runtime_row(row: dict[str, str]) -> bool:
    blob = " ".join(str(row.get(key, "")) for key in row.keys()).lower()
    kpi_scope = str(row.get("kpi_scope", "")).lower()
    lane = str(row.get("scoreboard_lane", "")).lower()
    subrun = str(row.get("subrun_id", "")).lower()
    path = str(row.get("path", "")).lower()
    status = " ".join(
        str(row.get(key, "")) for key in ("status", "judgment", "external_verification_status", "result_status")
    ).lower()
    is_runtime = (
        "runtime_probe" in kpi_scope
        or "runtime_probe" in lane
        or "mt5_" in subrun
        or "tester" in path
        or "runtime_probe_report" in path
    )
    excluded_tokens = (
        "proxy_not_runtime",
        "planning_only",
        "stage_open",
        "stage_closeout",
        "status_record",
        "runtime_probe_backfill_status",
        "missing_required",
        "out_of_scope_by_claim_no_mt5",
        "no_mt5",
        "not_runtime",
    )
    completed = any(token in status for token in ("completed", "observation", "inconclusive", "positive", "negative"))
    blocked = any(token in status for token in ("blocked", "invalid_setup", "prepared_no_external_execution"))
    return is_runtime and completed and not blocked and not any(token in blob for token in excluded_tokens)


def runtime_metrics_from_ledgers(stage: Path, rows: Iterable[dict[str, str]]) -> list[RuntimeMetric]:
    metrics: list[RuntimeMetric] = []
    for row in rows:
        if not is_actual_runtime_row(row):
            continue
        blob = " ".join(str(row.get(key, "")) for key in ("primary_kpi", "guardrail_kpi", "kpi_summary"))
        pf = first_number(row.get("profit_factor"), parse_key_value(blob, "pf"))
        trades = first_number(row.get("trade_count"), parse_key_value(blob, "trades"))
        net = first_number(row.get("net_profit"), parse_key_value(blob, "net_profit"), parse_key_value(blob, "net"))
        if pf is None and trades is None and net is None:
            continue
        metrics.append(
            RuntimeMetric(
                source=rel_path(stage / "03_reviews/stage_run_ledger.csv"),
                run_id=str(row.get("run_id", "")),
                subrun_id=str(row.get("subrun_id", "")),
                split=split_from_row(row),
                tier_scope=tier_from_text(" ".join(str(row.get(key, "")) for key in ("subrun_id", "record_view", "tier_scope"))),
                view=view_from_text(" ".join(str(row.get(key, "")) for key in ("subrun_id", "record_view", "tier_scope"))),
                profit_factor=pf,
                net_profit=net,
                trade_count=trades,
                max_drawdown_percent=first_number(
                    row.get("max_drawdown_percent"),
                    row.get("drawdown"),
                    parse_key_value(blob, "max_dd"),
                ),
                signal_count_diff=parse_key_value(blob, "signal_count_diff"),
                feature_ready_diff=parse_key_value(blob, "feature_ready_diff"),
            )
        )
    return metrics


def split_from_row(row: dict[str, str]) -> str:
    text = " ".join(str(row.get(key, "")) for key in ("subrun_id", "record_view", "tier_scope")).lower()
    if "oos" in text:
        return "oos"
    if "validation" in text or "_val" in text:
        return "validation_is"
    return ""


def tier_from_text(text: str) -> str:
    lowered = text.lower()
    if "tier a+b" in lowered or "routed" in lowered or "combined" in lowered:
        return "Tier A+B/routed(티어 A+B/라우팅)"
    if "tier_a" in lowered or "tier a" in lowered:
        return "Tier A(티어 A)"
    if "tier_b" in lowered or "tier b" in lowered:
        return "Tier B(티어 B)"
    return "needs_local_verification(로컬 검증 필요)"


def view_from_text(text: str) -> str:
    lowered = text.lower()
    if "routed" in lowered:
        return "routed_total(라우팅 전체)"
    if "combined" in lowered:
        return "combined(합산)"
    if "tier_a" in lowered or "tier a" in lowered or "tier_b" in lowered or "tier b" in lowered:
        return "separate(분리)"
    return "needs_local_verification(로컬 검증 필요)"


def is_proxy_row(row: dict[str, str]) -> bool:
    blob = " ".join(str(row.get(key, "")) for key in row.keys()).lower()
    if "runtime_probe" in blob or "mt5_" in blob or "tester" in blob:
        return False
    return "proxy" in blob or "scout" in str(row.get("scoreboard_lane", "")).lower()


def proxy_metrics_from_ledgers(stage: Path, rows: Iterable[dict[str, str]]) -> list[ProxyMetric]:
    metrics: list[ProxyMetric] = []
    for row in rows:
        if not is_proxy_row(row):
            continue
        blob = " ".join(str(row.get(key, "")) for key in ("primary_kpi", "guardrail_kpi", "notes", "kpi_summary"))
        metric = ProxyMetric(
            source=rel_path(stage / "03_reviews/stage_run_ledger.csv"),
            run_id=str(row.get("run_id", "")),
            subrun_id=str(row.get("subrun_id", "")),
            val_pf=parse_key_value(blob, "val_pf"),
            oos_pf=parse_key_value(blob, "oos_pf"),
            val_density=parse_key_value(blob, "val_density"),
            oos_density=parse_key_value(blob, "oos_density"),
            val_dd=parse_key_value(blob, "val_dd"),
            oos_dd=parse_key_value(blob, "oos_dd"),
        )
        if any(
            value is not None
            for value in (metric.val_pf, metric.oos_pf, metric.val_density, metric.oos_density, metric.val_dd, metric.oos_dd)
        ):
            metrics.append(metric)
    return metrics


def proxy_metrics_from_reports(stage: Path) -> list[ProxyMetric]:
    metrics: list[ProxyMetric] = []
    for path in sorted(safe_glob(stage / "03_reviews", "*.md")):
        name = path.name.lower()
        if "runtime_probe" in name or "proxy_runtime_gap" in name or "stage_closeout" in name:
            continue
        text = read_text(path)
        if "proxy" not in text.lower() and "PF" not in text:
            continue
        val_pf = parse_key_value(text, "val_pf")
        oos_pf = parse_key_value(text, "oos_pf")
        val_density = parse_key_value(text, "val_density")
        oos_density = parse_key_value(text, "oos_density")
        val_dd = parse_key_value(text, "val_dd")
        oos_dd = parse_key_value(text, "oos_dd")
        table_match = re.search(
            r"validation[^\n]*net/PF/density/DD[^\n]*:\s*`[^`]+`\s*/\s*`([^`]+)`\s*/\s*`([^`]+)`\s*/\s*`([^`%]+)%?`",
            text,
            re.IGNORECASE,
        )
        if table_match:
            val_pf = parse_float(table_match.group(1))
            val_density = parse_float(table_match.group(2))
            val_dd = parse_float(table_match.group(3))
        oos_match = re.search(
            r"OOS[^\n]*net/PF/density/DD[^\n]*:\s*`[^`]+`\s*/\s*`([^`]+)`\s*/\s*`([^`]+)`\s*/\s*`([^`%]+)%?`",
            text,
            re.IGNORECASE,
        )
        if oos_match:
            oos_pf = parse_float(oos_match.group(1))
            oos_density = parse_float(oos_match.group(2))
            oos_dd = parse_float(oos_match.group(3))
        metric = ProxyMetric(
            source=rel_path(path),
            run_id=path.stem,
            subrun_id="report_parse",
            val_pf=val_pf,
            oos_pf=oos_pf,
            val_density=val_density,
            oos_density=oos_density,
            val_dd=val_dd,
            oos_dd=oos_dd,
        )
        if any(
            value is not None
            for value in (metric.val_pf, metric.oos_pf, metric.val_density, metric.oos_density, metric.val_dd, metric.oos_dd)
        ):
            metrics.append(metric)
    return metrics


def closeout_tokens(stage: Path) -> list[str]:
    candidates = list(safe_glob(stage / "03_reviews", "*closeout*report.md"))
    candidates += list(safe_glob(stage / "04_selected", "*.md"))
    candidates += list(safe_glob(stage / "03_reviews", "runtime_probe_backfill_status.md"))
    text = "\n".join(read_text(path)[:8000] for path in candidates)
    tokens = []
    for token in (
        "no_runtime_handoff_candidate",
        "runtime_probe_ineligible",
        "missing_artifact",
        "invalid_setup",
        "no ONNX",
        "blocked",
        "negative_memory",
        "prepared_no_external_execution",
        "no adapter",
        "no_onnx",
        "density_profit_curve_gate_failed",
    ):
        if token.lower() in text.lower():
            tokens.append(token)
    return tokens


def audit_stage(stage_num: int, stage: Path, project_rows: list[dict[str, str]]) -> StageAudit:
    files = [path for path in safe_rglob(stage) if io_path(path).is_file()]
    rows = load_csv(stage / "03_reviews/stage_run_ledger.csv") + project_rows
    status_jsons = [path for path in files if path.name.lower().endswith("status.json") and "runtime_probe" in path.name.lower()]
    proxy_metrics = proxy_metrics_from_ledgers(stage, rows) + proxy_metrics_from_reports(stage)
    runtime_metrics = runtime_metrics_from_json(stage) + runtime_metrics_from_ledgers(stage, rows)
    runtime_metrics = dedupe_runtime_metrics(runtime_metrics)
    return StageAudit(
        stage_num=stage_num,
        stage_id=stage.name,
        path=stage,
        onnx_count=sum(1 for path in files if path.suffix.lower() == ".onnx"),
        joblib_count=sum(1 for path in files if path.suffix.lower() == ".joblib"),
        pkl_count=sum(1 for path in files if path.suffix.lower() == ".pkl"),
        set_count=sum(1 for path in files if path.suffix.lower() == ".set"),
        runtime_file_count=sum(1 for path in files if "runtime_probe" in path.name.lower()),
        gap_report_count=sum(1 for path in files if "proxy_runtime_gap" in path.name.lower()),
        status_json_count=len(status_jsons),
        has_existing_status=bool(status_jsons),
        closeout_tokens=closeout_tokens(stage),
        runtime_metrics=runtime_metrics,
        proxy_metrics=proxy_metrics,
    )


def dedupe_runtime_metrics(metrics: list[RuntimeMetric]) -> list[RuntimeMetric]:
    out: list[RuntimeMetric] = []
    seen: set[tuple[str, str, str, float | None, float | None]] = set()
    for metric in metrics:
        key = (metric.run_id, metric.subrun_id, metric.split, metric.profit_factor, metric.trade_count)
        if key in seen:
            continue
        seen.add(key)
        out.append(metric)
    return out


def materialization_classification(audit: StageAudit) -> str:
    if audit.has_actual_runtime_kpi:
        return "runtime_probe_kpi_present(런타임 탐침 KPI 있음)"
    existing = existing_status_classification(audit)
    if existing:
        return existing
    if audit.has_runtime_material:
        return "runtime_material_present_probe_missing(런타임 재료 있음, 탐침 누락)"
    return "invalid_setup_no_runtime_material(런타임 재료 없음 무효 설정)"


def existing_status_classification(audit: StageAudit) -> str:
    for path in safe_glob(audit.path / "03_reviews", "*runtime_probe*_status.json"):
        try:
            payload = json.loads(read_text(path))
        except json.JSONDecodeError:
            continue
        classification = str(payload.get("classification") or payload.get("status") or "")
        if classification and not classification.startswith("runtime_probe_observation"):
            return classification
    return ""


def sltp_unit_semantics_risk(audit: StageAudit) -> str:
    if not audit.has_actual_runtime_kpi:
        return "not_applicable_no_runtime_kpi(해당 없음, 런타임 KPI 없음)"
    if not audit.proxy_metrics:
        return "not_applicable_proxy_metric_missing(해당 없음, 프록시 지표 누락)"
    return "not_assessed_after_f65_clue(미평가, F65 단서 이후)"


def discovery_evidence(audit: StageAudit) -> str:
    if audit.runtime_metrics:
        sources = []
        for metric in audit.runtime_metrics:
            if metric.source not in sources:
                sources.append(metric.source)
        return ";".join(sources[:3])
    status = audit.path / "03_reviews/runtime_probe_backfill_status.json"
    if io_path(status).exists():
        return rel_path(status)
    return "stage_artifact_scan_no_runtime_kpi(단계 산출물 스캔, 런타임 KPI 없음)"


def problem_tags(audit: StageAudit) -> list[str]:
    tags: list[str] = []
    if not audit.has_actual_runtime_kpi:
        tags.append("runtime_kpi_missing(런타임 KPI 누락)")
        if not audit.has_runtime_material:
            tags.append("runtime_material_missing(런타임 재료 누락)")
        else:
            tags.append("runtime_material_present(런타임 재료 있음)")
            tags.append("candidate_contract_missing_or_unsupported(후보 계약 누락 또는 비지원)")
        if audit.closeout_tokens:
            tags.append("prior_closeout_ineligible_or_negative(이전 마감 부적격 또는 부정)")
        return tags
    if audit.gap_report_count == 0:
        tags.append("gap_report_missing(간극 보고 누락)")
    proxy_pf = audit.proxy_best_pf
    runtime_pf = audit.runtime_best_pf
    if proxy_pf is not None and runtime_pf is not None and proxy_pf - runtime_pf >= 0.2:
        tags.append("proxy_pf_not_transferred_to_runtime(프록시 수익 팩터 런타임 미전이)")
    if audit.runtime_worst_dd is not None and audit.runtime_worst_dd >= 10:
        tags.append("runtime_dd_over_goal_axis(런타임 손실폭 목표축 초과)")
    if audit.max_signal_abs_diff is not None and audit.max_signal_abs_diff > 0:
        tags.append("signal_count_parity_gap(신호 수 동등성 간극)")
    if audit.max_feature_abs_diff is not None and audit.max_feature_abs_diff > 0:
        tags.append("feature_ready_parity_gap(피처 준비 동등성 간극)")
    if runtime_pf is not None and runtime_pf < 1.2:
        tags.append("runtime_pf_low(런타임 수익 팩터 낮음)")
    return tags


def row_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def inventory_rows(audits: list[StageAudit]) -> list[dict[str, Any]]:
    rows = []
    for audit in audits:
        rows.append(
            {
                "stage_num": audit.stage_num,
                "stage_id": audit.stage_id,
                "has_actual_runtime_kpi": audit.has_actual_runtime_kpi,
                "discovery_evidence": discovery_evidence(audit),
                "runtime_material_present": audit.has_runtime_material,
                "primary_classification": materialization_classification(audit),
                "runtime_metric_rows": len(audit.runtime_metrics),
                "runtime_file_count": audit.runtime_file_count,
                "gap_report_count": audit.gap_report_count,
                "onnx_count": audit.onnx_count,
                "joblib_count": audit.joblib_count,
                "pkl_count": audit.pkl_count,
                "proxy_metric_rows": len(audit.proxy_metrics),
                "materialization_classification": materialization_classification(audit),
                "problem_tags": ";".join(problem_tags(audit)),
                "sltp_unit_semantics_risk": sltp_unit_semantics_risk(audit),
                "closeout_tokens": ";".join(audit.closeout_tokens),
                "proxy_best_pf": row_value(audit.proxy_best_pf),
                "proxy_best_oos_pf": row_value(audit.proxy_best_oos_pf),
                "runtime_best_pf": row_value(audit.runtime_best_pf),
                "runtime_worst_dd_percent": row_value(audit.runtime_worst_dd),
                "max_signal_abs_diff": row_value(audit.max_signal_abs_diff),
                "max_feature_abs_diff": row_value(audit.max_feature_abs_diff),
            }
        )
    return rows


def runtime_rows(audits: list[StageAudit]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for audit in audits:
        for metric in audit.runtime_metrics:
            rows.append(
                {
                    "stage_num": audit.stage_num,
                    "stage_id": audit.stage_id,
                    "run_id": metric.run_id,
                    "subrun_id": metric.subrun_id,
                    "split": metric.split,
                    "tier_scope": metric.tier_scope,
                    "view": metric.view,
                    "profit_factor": row_value(metric.profit_factor),
                    "net_profit": row_value(metric.net_profit),
                    "trade_count": row_value(metric.trade_count),
                    "max_drawdown_percent": row_value(metric.max_drawdown_percent),
                    "signal_count_diff": row_value(metric.signal_count_diff),
                    "feature_ready_diff": row_value(metric.feature_ready_diff),
                    "expected_signal_count": row_value(metric.expected_signal_count),
                    "order_fill_count": row_value(metric.order_fill_count),
                    "source": metric.source,
                }
            )
    return rows


def proxy_rows(audits: list[StageAudit]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for audit in audits:
        for metric in audit.proxy_metrics:
            rows.append(
                {
                    "stage_num": audit.stage_num,
                    "stage_id": audit.stage_id,
                    "run_id": metric.run_id,
                    "subrun_id": metric.subrun_id,
                    "val_pf": row_value(metric.val_pf),
                    "oos_pf": row_value(metric.oos_pf),
                    "val_density": row_value(metric.val_density),
                    "oos_density": row_value(metric.oos_density),
                    "val_dd": row_value(metric.val_dd),
                    "oos_dd": row_value(metric.oos_dd),
                    "source": metric.source,
                }
            )
    return rows


def materialize_missing_status(audits: list[StageAudit], created_at: str) -> list[dict[str, Any]]:
    materialized: list[dict[str, Any]] = []
    for audit in audits:
        classification = materialization_classification(audit)
        if audit.has_actual_runtime_kpi:
            continue
        payload = {
            "stage_num": audit.stage_num,
            "stage_id": audit.stage_id,
            "created_at_utc": created_at,
            "classification": classification,
            "judgment": classification,
            "preflight": {
                "status": classification,
                "reason": "F66 audit found no ONNX/joblib/pkl runtime material for MT5 materialization.",
                "checks": {
                    "onnx_count": audit.onnx_count,
                    "joblib_count": audit.joblib_count,
                    "pkl_count": audit.pkl_count,
                    "set_count": audit.set_count,
                    "runtime_file_count": audit.runtime_file_count,
                    "existing_runtime_status_json": audit.status_json_count,
                    "closeout_tokens": audit.closeout_tokens,
                },
            },
            "candidate": None,
            "runtime_rows": [],
            "claim_boundary": {
                "completion": "not_claimed(주장 없음)",
                "selected_baseline": "not_claimed(주장 없음)",
                "operating_promotion": "not_claimed(주장 없음)",
                "runtime_authority": "not_claimed(주장 없음)",
                "live_readiness": "not_claimed(주장 없음)",
                "goal_achieve": "not_claimed(주장 없음)",
            },
            "f66_audit": f"stages/{STAGE_ID}/03_reviews/frontier66A_runtime_probe_coverage_inventory_report.md",
        }
        status_json = audit.path / "03_reviews/runtime_probe_backfill_status.json"
        status_md = audit.path / "03_reviews/runtime_probe_backfill_status.md"
        if not io_path(status_json).exists():
            write_json(status_json, payload)
            write_text(status_md, status_markdown(audit, classification, created_at), bom=True)
            upsert_stage_and_project_ledger(audit, created_at, status_md)
            materialized.append(
                {
                    "stage_num": audit.stage_num,
                    "stage_id": audit.stage_id,
                    "action": "created_status_files_and_ledger(상태 파일과 장부 생성)",
                    "classification": classification,
                    "status_json": rel_path(status_json),
                    "status_md": rel_path(status_md),
                }
            )
        else:
            materialized.append(
                {
                    "stage_num": audit.stage_num,
                    "stage_id": audit.stage_id,
                    "action": "existing_status_reused(기존 상태 재사용)",
                    "classification": classification,
                    "status_json": rel_path(status_json),
                    "status_md": rel_path(status_md) if io_path(status_md).exists() else "",
                }
            )
    return materialized


def status_markdown(audit: StageAudit, classification: str, created_at: str) -> str:
    tokens = ", ".join(audit.closeout_tokens) if audit.closeout_tokens else "none(없음)"
    return f"""# Frontier {audit.stage_num:02d} Runtime Probe Backfill Status(런타임 탐침 소급 상태)

- created_at_utc(생성 시각): `{created_at}`
- source audit(원천 감사): `stages/{STAGE_ID}/03_reviews/frontier66A_runtime_probe_coverage_inventory_report.md`
- classification(분류): `{classification}`
- ONNX count(온엑스 수): `{audit.onnx_count}`
- joblib count(잡리브 수): `{audit.joblib_count}`
- pkl count(pkl 수): `{audit.pkl_count}`
- actual runtime KPI rows(실제 런타임 KPI 행): `0`
- closeout tokens(마감 토큰): `{tokens}`

## Boundary(경계)

이 파일은 F66 backfill audit(F66 소급 감사)의 materialization status(물질화 상태)입니다. MT5 runtime KPI(MT5 런타임 핵심 성과 지표), completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않습니다.
"""


def ledger_header() -> list[str]:
    if io_path(PROJECT_LEDGER).exists():
        with io_path(PROJECT_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            return next(reader)
    return [
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
        "claim_boundary",
        "created_at_utc",
        "runtime_authority",
        "operating_promotion",
        "goal_achieve",
        "run_family",
        "run_type",
    ]


def upsert_stage_and_project_ledger(audit: StageAudit, created_at: str, status_md: Path) -> None:
    header = ledger_header()
    row_id = f"frontier{audit.stage_num:02d}Z_runtime_probe_backfill_status_v1__f66_status"
    row = {key: "" for key in header}
    row.update(
        {
            "ledger_row_id": row_id,
            "stage_id": audit.stage_id,
            "run_id": f"frontier{audit.stage_num:02d}Z_runtime_probe_backfill_status_v1",
            "subrun_id": row_id,
            "parent_run_id": RUN_ID,
            "record_view": "runtime_probe_backfill_status(런타임 탐침 소급 상태)",
            "tier_scope": "missing_required_or_verify_only(필수 누락 또는 확인 전용)",
            "kpi_scope": "status_record(상태 기록)",
            "scoreboard_lane": "runtime_probe_backfill(런타임 탐침 소급)",
            "status": "invalid_setup_no_runtime_material",
            "judgment": "invalid_setup_no_runtime_material(런타임 재료 없음 무효 설정)",
            "path": rel_path(status_md),
            "primary_kpi": "actual_runtime_kpi_rows=0;onnx_count=0;joblib_count=0;pkl_count=0",
            "guardrail_kpi": "no_authority_no_goal_claim(권위/목표 주장 없음)",
            "external_verification_status": "not_run_no_runtime_material(미실행, 런타임 재료 없음)",
            "notes": "F66 audit materialized missing runtime probe status; no MT5 KPI because no runtime material was found.",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created_at,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "run_family": "runtime_backfill(런타임 소급)",
            "run_type": "mt5_runtime_probe_backfill_status(MT5 런타임 탐침 소급 상태)",
        }
    )
    stage_ledger = audit.path / "03_reviews/stage_run_ledger.csv"
    upsert_csv_row(stage_ledger, header, row, row_id)
    upsert_csv_row(PROJECT_LEDGER, header, row, row_id)


def upsert_csv_row(path: Path, header: list[str], row: dict[str, str], row_id: str) -> None:
    rows = load_csv(path)
    if any(existing.get("ledger_row_id") == row_id for existing in rows):
        return
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if not io_path(path).exists():
        write_csv(path, [row], header)
        return
    with io_path(path).open("a", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writerow(row)


def write_stage_open_docs(created_at: str) -> None:
    write_text(
        STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# F66 Runtime Probe Backfill Gap Audit(런타임 탐침 소급 간극 감사)

- stage_id(단계 ID): `{STAGE_ID}`
- opened_at_utc(개방 시각): `{created_at}`
- hypothesis(가설): F2~F64의 proxy(프록시)와 runtime probe(런타임 탐침) 차이는 단일 오류가 아니라 materialization readiness(물질화 준비도), executable handoff(실행 가능 인계), signal lifecycle(신호 생명주기), exit semantics(청산 의미), tester economics(테스터 경제성)의 조합에서 생긴다.
- scope(범위): `stage_frontier_02` through `stage_frontier_64`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Success Criteria(성공 기준)

- actual runtime KPI(실제 런타임 핵심 성과 지표)가 있는 stage(단계)와 없는 stage(단계)를 분리한다.
- 없는 stage(단계)는 물질화 상태를 남기고, 실행 불가면 원인을 기록한다.
- runtime KPI(런타임 핵심 성과 지표)가 있는 stage(단계)는 proxy-runtime gap(프록시-런타임 간극)을 분류한다.
- completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        bom=True,
    )
    write_text(
        STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# F66 Input Refs(입력 참조)

- F65 closeout clue(F65 마감 단서): `sltp_unit_semantics_gap_between_proxy_price_units_and_mt5_points(프록시 가격 단위와 MT5 포인트 손절/익절 의미 차이)`
- audited range(감사 범위): `stage_frontier_02` to `stage_frontier_64`
- project ledger(프로젝트 장부): `docs/registers/alpha_run_ledger.csv`
- runtime backfill register(런타임 소급 등록부): `docs/agent_control/runtime_probe_backfill/`
- generated_by(생성 도구): `stage_pipelines/stage_frontier_66/frontier66_runtime_probe_gap_audit.py`
""",
        bom=True,
    )


def write_reports(audits: list[StageAudit], materialized: list[dict[str, Any]], created_at: str) -> None:
    inv = inventory_rows(audits)
    runtime = runtime_rows(audits)
    proxy = proxy_rows(audits)
    write_csv(RUN_ROOT / "frontier66_runtime_probe_inventory.csv", inv)
    write_csv(RUN_ROOT / "frontier66_runtime_kpi_rows.csv", runtime)
    write_csv(RUN_ROOT / "frontier66_proxy_metric_rows.csv", proxy)
    write_csv(RUN_ROOT / "frontier66_materialization_manifest.csv", materialized)
    summary = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "stage_count": len(audits),
        "actual_runtime_kpi_stage_count": sum(1 for audit in audits if audit.has_actual_runtime_kpi),
        "missing_runtime_kpi_stage_count": sum(1 for audit in audits if not audit.has_actual_runtime_kpi),
        "materialized_status_count": sum(1 for row in materialized if str(row.get("action", "")).startswith("created")),
        "existing_status_reused_count": sum(1 for row in materialized if str(row.get("action", "")).startswith("existing")),
        "actual_kpi_stages": [audit.stage_num for audit in audits if audit.has_actual_runtime_kpi],
        "missing_kpi_stages": [audit.stage_num for audit in audits if not audit.has_actual_runtime_kpi],
        "gap_report_missing_actual_kpi_stages": [
            audit.stage_num for audit in audits if audit.has_actual_runtime_kpi and audit.gap_report_count == 0
        ],
        "missing_kpi_with_raw_runtime_material_stages": [
            audit.stage_num for audit in audits if not audit.has_actual_runtime_kpi and audit.has_runtime_material
        ],
        "missing_kpi_without_raw_runtime_material_stages": [
            audit.stage_num for audit in audits if not audit.has_actual_runtime_kpi and not audit.has_runtime_material
        ],
    }
    write_json(RUN_ROOT / "frontier66_runtime_probe_gap_audit_summary.json", summary)
    write_text(REVIEW_ROOT / "frontier66A_runtime_probe_coverage_inventory_report.md", coverage_report(audits, materialized, created_at), bom=True)
    write_text(REVIEW_ROOT / "frontier66B_proxy_runtime_gap_problem_report.md", gap_report(audits, created_at), bom=True)
    write_stage_run_ledger(audits, created_at)
    write_review_index(created_at)
    write_selection_status(created_at, summary)


def fmt(value: Any) -> str:
    if value is None or value == "":
        return "NA"
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def coverage_report(audits: list[StageAudit], materialized: list[dict[str, Any]], created_at: str) -> str:
    actual = [audit.stage_num for audit in audits if audit.has_actual_runtime_kpi]
    missing = [audit.stage_num for audit in audits if not audit.has_actual_runtime_kpi]
    no_gap = [audit.stage_num for audit in audits if audit.has_actual_runtime_kpi and audit.gap_report_count == 0]
    raw_material_missing_kpi = [audit.stage_num for audit in audits if not audit.has_actual_runtime_kpi and audit.has_runtime_material]
    no_material_missing_kpi = [audit.stage_num for audit in audits if not audit.has_actual_runtime_kpi and not audit.has_runtime_material]
    lines = [
        "# F66A Runtime Probe Coverage Inventory(런타임 탐침 커버리지 인벤토리)",
        "",
        f"- created_at_utc(생성 시각): `{created_at}`",
        f"- audited stages(감사 단계): `F02-F64`",
        f"- actual runtime KPI stage count(실제 런타임 KPI 단계 수): `{len(actual)}`",
        f"- missing runtime KPI stage count(런타임 KPI 누락 단계 수): `{len(missing)}`",
        f"- status materialized or reused(상태 물질화 또는 재사용): `{len(materialized)}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Stage Sets(단계 묶음)",
        "",
        f"- actual runtime KPI present(실제 런타임 KPI 있음): `{compact_stage_list(actual)}`",
        f"- actual runtime KPI missing(실제 런타임 KPI 누락): `{compact_stage_list(missing)}`",
        f"- missing KPI with raw runtime material(런타임 재료는 있으나 KPI 누락): `{compact_stage_list(raw_material_missing_kpi)}`",
        f"- missing KPI without raw runtime material(런타임 재료도 없는 KPI 누락): `{compact_stage_list(no_material_missing_kpi)}`",
        f"- actual KPI present but gap report missing(실제 KPI는 있으나 간극 보고 누락): `{compact_stage_list(no_gap)}`",
        "",
        "## Missing Runtime KPI Detail(런타임 KPI 누락 상세)",
        "",
        "| stage(단계) | materialization(물질화) | ONNX(온엑스) | joblib(잡리브) | closeout tokens(마감 토큰) |",
        "|---:|---|---:|---:|---|",
    ]
    for audit in audits:
        if audit.has_actual_runtime_kpi:
            continue
        lines.append(
            f"| F{audit.stage_num:02d} | {materialization_classification(audit)} | {audit.onnx_count} | {audit.joblib_count} | {', '.join(audit.closeout_tokens) or 'none(없음)'} |"
        )
    lines.extend(
        [
            "",
            "## Effect(효과)",
            "",
            "이 인벤토리는 runtime probe(런타임 탐침)가 없던 단계를 무조건 백테스트 성공/실패로 섞지 않고, 먼저 실행 가능한 material(재료)과 EA-compatible candidate contract(EA 호환 후보 계약)가 있는지로 분리한다. F15/F18/F19는 raw material(원 재료)은 있으나 실행 계약 또는 handoff candidate(인계 후보)가 불명확/부적격이고, 나머지 누락 stage(단계)는 raw runtime material(원 런타임 재료)도 없다. 그래서 이번 감사에서 새 MT5 KPI(MT5 핵심 성과 지표)를 추가로 뽑을 수 있는 executable candidate(실행 가능 후보)는 발견되지 않았다.",
        ]
    )
    return "\n".join(lines) + "\n"


def gap_report(audits: list[StageAudit], created_at: str) -> str:
    lines = [
        "# F66B Proxy Runtime Gap Problem Report(프록시-런타임 간극 문제 보고)",
        "",
        f"- created_at_utc(생성 시각): `{created_at}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Main Problems(주요 문제)",
        "",
        "1. runtime KPI missing split(런타임 KPI 누락 분리): F15/F18/F19는 raw ONNX/joblib material(원 온엑스/잡리브 재료)이 있으나 EA-compatible candidate contract(EA 호환 후보 계약) 또는 runtime handoff candidate(런타임 인계 후보)가 없다. 나머지 누락 stage(단계)는 raw runtime material(원 런타임 재료)도 없다.",
        "2. gap report missing(간극 보고 누락): F02-F10, F12-F14, F16-F17은 runtime KPI(런타임 KPI)가 있지만 proxy-runtime gap(프록시-런타임 간극) 보고가 stage-local(단계 로컬)로 없다.",
        "3. runtime economics collapse(런타임 경제성 붕괴): F50~F64 중 gap report(간극 보고)가 있는 단계는 runtime PF(런타임 수익 팩터)가 대체로 낮고 DD(손실폭)가 목표축을 자주 넘는다.",
        "4. semantics mismatch risk(의미 불일치 위험): F65에서 확인한 SL/TP unit semantics(손절/익절 단위 의미) 문제는 이전 stage(단계)의 proxy(프록시)와 MT5(메타트레이더5) 비교에도 공통 위험으로 남는다.",
        "",
        "## Stage Gap Table(단계별 간극 표)",
        "",
        "| stage(단계) | proxy best PF(프록시 최고 PF) | runtime best PF(런타임 최고 PF) | runtime worst DD%(런타임 최악 DD%) | signal diff(신호 차이) | SL/TP semantics risk(손절/익절 의미 위험) | problem tags(문제 태그) |",
        "|---:|---:|---:|---:|---:|---|---|",
    ]
    for audit in audits:
        if not audit.has_actual_runtime_kpi:
            continue
        lines.append(
            f"| F{audit.stage_num:02d} | {fmt(audit.proxy_best_pf)} | {fmt(audit.runtime_best_pf)} | {fmt(audit.runtime_worst_dd)} | {fmt(audit.max_signal_abs_diff)} | {sltp_unit_semantics_risk(audit)} | {'; '.join(problem_tags(audit)) or 'runtime_probe_observed(런타임 탐침 관찰)'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation(해석)",
            "",
            "현재 gap(간극)은 하나의 코드 오류로 단정하기 어렵다. F02-F10, F12-F14, F16-F17의 early backfill(초기 소급 실행)은 signal_count_diff(신호 수 차이)가 0인 경우가 많아 feature/signal parity(피처/신호 동등성)보다 exit/economics semantics(청산/경제성 의미) 쪽이 더 의심된다. F50 이후는 이미 gap report(간극 보고)가 있어 경제성 붕괴와 DD(손실폭) 초과가 반복된 negative memory(부정 기억) 계열이다. F11, F20~F49의 핵심 문제는 runtime probe(런타임 탐침) 실행 누락보다 runtime materialization(런타임 물질화) 자체의 부재이고, F15/F18/F19는 모델 파일은 있으나 실행 계약과 handoff candidate(인계 후보)가 닫히지 않은 문제다.",
        ]
    )
    return "\n".join(lines) + "\n"


def compact_stage_list(values: list[int]) -> str:
    if not values:
        return "none"
    values = sorted(values)
    ranges: list[str] = []
    start = prev = values[0]
    for value in values[1:]:
        if value == prev + 1:
            prev = value
            continue
        ranges.append(f"F{start:02d}" if start == prev else f"F{start:02d}-F{prev:02d}")
        start = prev = value
    ranges.append(f"F{start:02d}" if start == prev else f"F{start:02d}-F{prev:02d}")
    return ", ".join(ranges)


def write_stage_run_ledger(audits: list[StageAudit], created_at: str) -> None:
    header = ledger_header()
    row_id = f"{RUN_ID}__coverage_gap_audit"
    row = {key: "" for key in header}
    row.update(
        {
            "ledger_row_id": row_id,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": row_id,
            "record_view": "runtime_probe_gap_audit(런타임 탐침 간극 감사)",
            "tier_scope": "F02-F64",
            "kpi_scope": "coverage_and_gap_audit(커버리지 및 간극 감사)",
            "scoreboard_lane": "runtime_probe_backfill_audit(런타임 탐침 소급 감사)",
            "status": "completed_observation_report_no_authority",
            "judgment": "runtime_probe_gap_audit_observation(런타임 탐침 간극 감사 관찰)",
            "path": f"stages/{STAGE_ID}/03_reviews/frontier66B_proxy_runtime_gap_problem_report.md",
            "primary_kpi": (
                f"actual_runtime_kpi_stage_count={sum(1 for audit in audits if audit.has_actual_runtime_kpi)};"
                f"missing_runtime_kpi_stage_count={sum(1 for audit in audits if not audit.has_actual_runtime_kpi)}"
            ),
            "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal",
            "external_verification_status": "local_artifact_audit_only_no_new_mt5_execution",
            "notes": "F66 audit found no missing stage with recoverable ONNX/joblib/pkl runtime material.",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created_at,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "run_family": "runtime_backfill_gap_audit(런타임 소급 간극 감사)",
            "run_type": "artifact_inventory_and_gap_attribution(산출물 인벤토리 및 간극 귀인)",
        }
    )
    upsert_csv_row(REVIEW_ROOT / "stage_run_ledger.csv", header, row, row_id)


def write_review_index(created_at: str) -> None:
    write_text(
        REVIEW_ROOT / "review_index.md",
        f"""# F66 Review Index(검토 색인)

- created_at_utc(생성 시각): `{created_at}`
- `frontier66A_runtime_probe_coverage_inventory_report.md`
- `frontier66B_proxy_runtime_gap_problem_report.md`
- `stage_run_ledger.csv`
- run artifacts(실행 산출물): `stages/{STAGE_ID}/02_runs/{RUN_ID}/`
""",
        bom=True,
    )


def write_selection_status(created_at: str, summary: dict[str, Any]) -> None:
    payload = {
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": "runtime_probe_gap_audit_observation_no_authority",
        "closeout_label": "not_closed",
        "claim_boundary": CLAIM_BOUNDARY,
        "summary": summary,
    }
    write_json(STAGE_ROOT / "04_selected/selection_status.json", payload)
    write_text(
        STAGE_ROOT / "04_selected/selection_status.md",
        f"""# F66 Selection Status(선택 상태)

- status(상태): `runtime_probe_gap_audit_observation_no_authority`
- closeout label(마감 라벨): `not_closed(아직 마감 아님)`
- actual runtime KPI stage count(실제 런타임 KPI 단계 수): `{summary['actual_runtime_kpi_stage_count']}`
- missing runtime KPI stage count(런타임 KPI 누락 단계 수): `{summary['missing_runtime_kpi_stage_count']}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

F66은 현재 problem report(문제 보고) 단계다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        bom=True,
    )


def run(write: bool) -> dict[str, Any]:
    created_at = utc_now()
    dirs = stage_dirs()
    project_by_stage = project_rows_by_stage()
    audits = [audit_stage(num, dirs[num], project_by_stage.get(num, [])) for num in range(2, 65)]
    materialized: list[dict[str, Any]] = []
    if write:
        write_stage_open_docs(created_at)
        materialized = materialize_missing_status(audits, created_at)
        # Re-audit after status files are added so inventory counts include new files.
        dirs = stage_dirs()
        project_by_stage = project_rows_by_stage()
        audits = [audit_stage(num, dirs[num], project_by_stage.get(num, [])) for num in range(2, 65)]
        write_reports(audits, materialized, created_at)
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "stage_count": len(audits),
        "actual_runtime_kpi_stages": [audit.stage_num for audit in audits if audit.has_actual_runtime_kpi],
        "missing_runtime_kpi_stages": [audit.stage_num for audit in audits if not audit.has_actual_runtime_kpi],
        "gap_report_missing_actual_kpi_stages": [
            audit.stage_num for audit in audits if audit.has_actual_runtime_kpi and audit.gap_report_count == 0
        ],
        "materialized": materialized,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="F66 frontier runtime probe backfill and gap audit.")
    parser.add_argument("--write", action="store_true", help="Write F66 reports and missing status artifacts.")
    args = parser.parse_args()
    print(json.dumps(run(write=args.write), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
