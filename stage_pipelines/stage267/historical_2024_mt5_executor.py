from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    EA_TESTER_SET_NAME,
    clear_runtime_outputs,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe


STAGE_ID = input_probe.STAGE_ID
RUN_ID = input_probe.RUN_ID
RUN_ROOT = input_probe.RUN_ROOT
HIST_ROOT = input_probe.HIST_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

INPUT_MANIFEST_PATH = HIST_ROOT / "manifest.json"
EXECUTION_RESULT_PATH = HIST_ROOT / "execution_result.json"
KPI_RECORDS_PATH = HIST_ROOT / "mt5_kpi_records.json"
KPI_SUMMARY_PATH = HIST_ROOT / "mt5_kpi_summary.csv"
FORENSICS_PATH = HIST_ROOT / "backtest_forensics.csv"
EXECUTION_REPORT_PATH = REVIEWS_ROOT / "stage267_historical_2024_mt5_execution_report.md"
STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
PRODUCER_PATH = Path("stage_pipelines/stage267/historical_2024_mt5_executor.py")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in fieldnames})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def parse_set_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    text = io_path(path).read_text(encoding="utf-8-sig")
    for line in text.splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def select_attempts(attempts: Sequence[Mapping[str, Any]], names: Sequence[str], limit: int | None) -> list[dict[str, Any]]:
    selected = [dict(item) for item in attempts]
    if names:
        wanted = set(names)
        selected = [item for item in selected if str(item.get("attempt_name")) in wanted]
    if limit is not None:
        selected = selected[: max(0, int(limit))]
    return selected


def execution_status(execution_results: Sequence[Mapping[str, Any]], kpi_records: Sequence[Mapping[str, Any]]) -> str:
    if not execution_results:
        return "blocked_no_attempts_executed"
    completed = all(item.get("status") == "completed" for item in execution_results)
    report_completed = bool(kpi_records) and all(item.get("status") == "completed" for item in kpi_records)
    if completed and report_completed:
        return "completed"
    if any(item.get("status") == "completed" for item in execution_results):
        return "partial"
    return "blocked"


def kpi_summary_rows(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        metrics = dict(record.get("metrics", {}))
        rows.append(
            {
                "record_view": record.get("record_view"),
                "tier_scope": record.get("tier_scope"),
                "split": record.get("split"),
                "status": record.get("status"),
                "route_role": record.get("route_role"),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "expectancy": metrics.get("expectancy"),
                "max_drawdown_amount": metrics.get("max_drawdown_amount"),
                "max_drawdown_percent": metrics.get("max_drawdown_percent"),
                "recovery_factor": metrics.get("recovery_factor"),
                "order_attempt_count": metrics.get("order_attempt_count"),
                "fill_count": metrics.get("fill_count"),
                "reject_count": metrics.get("reject_count"),
                "skip_count": metrics.get("skip_count"),
                "feature_ready_count": metrics.get("feature_ready_count"),
                "model_ok_count": metrics.get("model_ok_count"),
            }
        )
    return rows


def forensic_rows(
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_attempt = {str(item.get("attempt_name")): item for item in execution_results}
    reports = {str(item.get("attempt_name")): item for item in report_records}
    rows: list[dict[str, Any]] = []
    module_hashes = mt5.mt5_runtime_module_hashes()
    module_hash_text = ";".join(f"{item.get('path')}={item.get('sha256')}" for item in module_hashes)
    for attempt in attempts:
        attempt_name = str(attempt.get("attempt_name"))
        ini = dict(attempt.get("ini", {}).get("tester", {}))
        set_path = Path(str(attempt.get("set", {}).get("path")))
        set_values = parse_set_values(set_path) if path_exists(set_path) else {}
        report = reports.get(attempt_name, {})
        metrics = dict(report.get("metrics", {})) if isinstance(report, Mapping) else {}
        execution = by_attempt.get(attempt_name, {})
        rows.append(
            {
                "attempt_name": attempt_name,
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "tester_status": execution.get("status"),
                "runtime_status": execution.get("runtime_outputs", {}).get("status") if isinstance(execution, Mapping) else None,
                "report_status": report.get("status") if isinstance(report, Mapping) else None,
                "terminal": TERMINAL_PATH_DEFAULT.as_posix(),
                "symbol": ini.get("Symbol"),
                "timeframe": ini.get("Period"),
                "deposit": ini.get("Deposit"),
                "leverage": ini.get("Leverage"),
                "model": ini.get("Model"),
                "execution_mode": ini.get("ExecutionMode"),
                "from_date": ini.get("FromDate"),
                "to_date": ini.get("ToDate"),
                "ea": ini.get("Expert"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "model_path": set_values.get("InpModelPath"),
                "feature_path": set_values.get("InpFeatureCsvPath"),
                "feature_order_hash": set_values.get("InpFeatureOrderHash"),
                "magic": set_values.get("InpMagic"),
                "fixed_lot": set_values.get("InpFixedLot"),
                "atr_enabled": set_values.get("InpAtrSltpEnabled"),
                "model_risk_enabled": set_values.get("InpModelRiskSizingEnabled"),
                "report_path": report.get("html_report", {}).get("path") if isinstance(report, Mapping) else None,
                "report_sha256": report.get("html_report", {}).get("sha256") if isinstance(report, Mapping) else None,
                "chart_path": report.get("chart", {}).get("path") if isinstance(report, Mapping) else None,
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "max_drawdown_percent": metrics.get("max_drawdown_percent"),
                "module_hashes": module_hash_text,
            }
        )
    return rows


def upsert_stage_ledger(status: str, report_path: Path) -> None:
    row = {
        "row_id": "stage267_run267B_historical_2024_mt5_execution",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "historical_2024_mt5_execution",
        "tier_scope": "Tier A and Tier A+B historical stress attempts",
        "scoreboard": "regular_risk_execution",
        "status": status,
        "judgment": "inconclusive_until_balance_equity_review" if status in {"completed", "partial"} else "blocked_mt5_execution",
        "evidence_boundary": "mt5_2024_strategy_tester_reports_no_candidate_selection_no_onnx_readiness",
        "report_path": rel(report_path),
        "notes": "2024 historical stress MT5 execution attempt recorded; no selected candidate and no operating meaning.",
    }
    rows = input_probe.read_csv_rows(STAGE_LEDGER_PATH)
    merged = [item for item in rows if item.get("row_id") != row["row_id"]]
    merged.append(row)
    input_probe.write_csv(
        STAGE_LEDGER_PATH,
        merged,
        (
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
        ),
    )


def upsert_artifacts(created_at: str) -> None:
    rows = input_probe.read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows = [
        {
            "artifact_id": "stage267_run267B_historical_2024_mt5_executor",
            "artifact_type": "producer_script",
            "path": rel(PRODUCER_PATH),
            "sha256": sha256_file_lf_normalized(PRODUCER_PATH),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Executes Stage267 historical 2024 MT5 tester attempts.",
        },
        {
            "artifact_id": "stage267_run267B_historical_2024_execution_result",
            "artifact_type": "execution_result",
            "path": rel(EXECUTION_RESULT_PATH),
            "sha256": sha256_file_lf_normalized(EXECUTION_RESULT_PATH) if path_exists(EXECUTION_RESULT_PATH) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "MT5 execution result payload for 2024 historical stress.",
        },
        {
            "artifact_id": "stage267_run267B_historical_2024_kpi_summary",
            "artifact_type": "kpi_summary",
            "path": rel(KPI_SUMMARY_PATH),
            "sha256": sha256_file_lf_normalized(KPI_SUMMARY_PATH) if path_exists(KPI_SUMMARY_PATH) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "MT5 KPI summary for 2024 historical stress.",
        },
        {
            "artifact_id": "stage267_run267B_historical_2024_forensics",
            "artifact_type": "backtest_forensics",
            "path": rel(FORENSICS_PATH),
            "sha256": sha256_file_lf_normalized(FORENSICS_PATH) if path_exists(FORENSICS_PATH) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Tester identity, EA identity, report identity, and trade evidence for 2024 stress.",
        },
        {
            "artifact_id": "stage267_run267B_historical_2024_mt5_execution_report",
            "artifact_type": "review_report",
            "path": rel(EXECUTION_REPORT_PATH),
            "sha256": sha256_file_lf_normalized(EXECUTION_REPORT_PATH) if path_exists(EXECUTION_REPORT_PATH) else "missing",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "User-facing 2024 historical stress MT5 execution boundary report.",
        },
    ]
    replacement = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(new_rows)
    input_probe.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        (
            "artifact_id",
            "artifact_type",
            "path",
            "sha256",
            "stage_id",
            "run_id",
            "created_at_utc",
            "notes",
        ),
    )


def report_markdown(result: Mapping[str, Any]) -> str:
    status = result["execution_status"]
    kpi_rows = result.get("kpi_summary_rows", [])
    completed_reports = sum(1 for row in result.get("strategy_tester_reports", []) if row.get("status") == "completed")
    lines = [
        "# Stage267 Historical 2024 MT5 Execution Report(267단계 2024 MT5 실행 보고)",
        "",
        f"- action(행동): `{len(result.get('attempts_executed', []))}` MT5 Strategy Tester(전략 테스터) attempt(시도)를 실행했다.",
        f"- effect(효과): 2024 historical stress(2024 과거 압박)가 input-only(입력만 있음)에서 `{status}` evidence(근거) 상태로 이동했다.",
        f"- completed_reports(완료 보고서): `{completed_reports}`",
        f"- kpi_records(KPI 기록): `{len(result.get('mt5_kpi_records', []))}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Backtest Forensics(백테스트 포렌식)",
        "",
        f"- tester_identity(테스터 정체성): terminal(터미널) `{TERMINAL_PATH_DEFAULT}`, symbol(심볼) `US100`, timeframe(시간프레임) `M5`, deposit(예치금) `500`, leverage(레버리지) `1:100`, model(모델링) `4`, date range(기간) `2024.01.02` to `2025.01.01`.",
        f"- ea_identity(EA 정체성): `Project_Obsidian_Prime_v2\\foundation\\mt5\\ObsidianPrimeV2_RuntimeProbeEA.ex5`; module hash(모듈 해시)는 `{rel(EXECUTION_RESULT_PATH)}`에 기록했다.",
        f"- report_identity(보고서 정체성): reports(보고서)는 `{rel(HIST_ROOT / 'mt5' / 'reports')}` 아래에 수집한다.",
        "- cost_assumptions(비용 가정): tester broker environment(테스터 브로커 환경)의 spread/commission/slippage(스프레드/수수료/슬리피지)를 따른다. 세부 비용은 개별 HTML report(HTML 보고서)에서 확인해야 한다.",
        f"- backtest_judgment(백테스트 판정): `{status}`.",
        "",
        "## KPI Read(KPI 판독)",
        "",
    ]
    if kpi_rows:
        lines.extend(
            [
                "| record_view(기록 보기) | net_profit(순수익) | PF(수익 팩터) | trades(거래 수) | DD%(손실폭%) |",
                "| --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in kpi_rows:
            lines.append(
                f"| `{row.get('record_view')}` | {row.get('net_profit', '')} | {row.get('profit_factor', '')} | {row.get('trade_count', '')} | {row.get('max_drawdown_percent', '')} |"
            )
    else:
        lines.append("- KPI(핵심 성과 지표)는 아직 없다. Effect(효과): 이 실행은 후보 선택 근거로 사용할 수 없다.")
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            "- selected_candidate(선택 후보): `none`",
            "- selected_research_baseline(선택 연구 기준선): `none`",
            "- ONNX readiness(ONNX 준비): `not_claimed`",
            "- operating meaning(운영 의미): `none`",
            "- next_condition(다음 조건): balance/equity curve(잔액/평가금 곡선), monthly/session/time-slice KPI(월별/세션별/시간대별 KPI), trade quality(거래 품질)를 보고 후보별 깨짐 정도를 판정한다.",
        ]
    )
    return "\n".join(lines)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    input_manifest = read_json(INPUT_MANIFEST_PATH)
    attempts = select_attempts(input_manifest.get("attempts", []), args.attempt_name or [], args.limit)
    compile_payload = mt5.compile_mql5_ea(
        args.metaeditor_path,
        mt5.EA_SOURCE_PATH,
        HIST_ROOT / "mt5" / "compile.log",
    )
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        for attempt in attempts:
            clear_runtime_outputs(args.common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(args.terminal_data_root, attempt)
            tester_result = mt5.run_mt5_tester(
                args.terminal_path,
                Path(str(attempt["ini"]["path"])),
                set_path=Path(str(attempt["set"]["path"])),
                tester_profile_set_path=args.tester_profile_root / EA_TESTER_SET_NAME,
                tester_profile_ini_path=args.tester_profile_root / f"opv2_s267_{attempt['attempt_name']}.ini",
                timeout_seconds=args.timeout_seconds,
            )
            tester_result["tier"] = attempt["tier"]
            tester_result["split"] = attempt["split"]
            tester_result["attempt_name"] = attempt["attempt_name"]
            tester_result["attempt_role"] = attempt.get("attempt_role")
            tester_result["record_view_prefix"] = attempt.get("record_view_prefix")
            tester_result["candidate_id"] = attempt.get("candidate_id")
            tester_result["candidate_alias"] = attempt.get("candidate_alias")
            tester_result["ini_path"] = attempt["ini"]["path"]
            tester_result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                args.common_files_root,
                attempt,
                timeout_seconds=args.runtime_timeout_seconds,
                poll_seconds=2,
            )
            if tester_result["runtime_outputs"].get("status") != "completed":
                tester_result["status"] = "blocked"
            execution_results.append(tester_result)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=args.terminal_data_root,
        run_output_root=HIST_ROOT,
        attempts=attempts,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    kpi_rows = kpi_summary_rows(kpi_records)
    forensics = forensic_rows(attempts, execution_results, report_records)
    status = execution_status(execution_results, kpi_records)
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "execution_status": status,
        "claim_boundary": CLAIM_BOUNDARY,
        "compile": compile_payload,
        "attempts_executed": attempts,
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": kpi_records,
        "kpi_summary_rows": kpi_rows,
        "backtest_forensics": forensics,
        "runtime_module_hashes": mt5.mt5_runtime_module_hashes(),
        "input_manifest": rel(INPUT_MANIFEST_PATH),
    }
    write_json(EXECUTION_RESULT_PATH, result)
    write_json(KPI_RECORDS_PATH, kpi_records)
    write_csv(KPI_SUMMARY_PATH, kpi_rows)
    write_csv(FORENSICS_PATH, forensics)
    write_md(EXECUTION_REPORT_PATH, report_markdown(result))
    upsert_stage_ledger(status, EXECUTION_REPORT_PATH)
    upsert_artifacts(created_at)
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempt-name", action="append", default=[])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    parser.add_argument("--terminal-path", type=Path, default=TERMINAL_PATH_DEFAULT)
    parser.add_argument("--metaeditor-path", type=Path, default=METAEDITOR_PATH_DEFAULT)
    parser.add_argument("--terminal-data-root", type=Path, default=TERMINAL_DATA_ROOT_DEFAULT)
    parser.add_argument("--common-files-root", type=Path, default=COMMON_FILES_ROOT_DEFAULT)
    parser.add_argument("--tester-profile-root", type=Path, default=TESTER_PROFILE_ROOT_DEFAULT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = execute(args)
    print(
        json.dumps(
            {
                "execution_status": result["execution_status"],
                "attempt_count": len(result["attempts_executed"]),
                "kpi_records": len(result["mt5_kpi_records"]),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
