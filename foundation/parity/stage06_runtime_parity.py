from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.features.session_calendar import broker_clock_key_to_event_utc  # noqa: E402
from foundation.pipelines.materialize_fpmarkets_v2_dataset import (  # noqa: E402
    EXPECTED_FEATURE_ORDER_HASH,
    FEATURE_ORDER,
)


RUN_ID = "20260425_stage06_runtime_parity_blocked_v1"
STAGE_ID = "06_runtime_parity__python_mt5_runtime_authority"
LANE = "runtime"
MATERIALIZER_VERSION = "fpmarkets_v2_stage06_runtime_parity_v1"

MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
SOURCE_DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"
FIXTURE_SET_ID = "fixture_fpmarkets_v2_stage06_runtime_minimum_v1"
BUNDLE_ID = "bundle_fpmarkets_v2_stage06_runtime_parity_v1"
RUNTIME_ID = "runtime_fpmarkets_v2_python_mt5_stage06_parity_v1"
REPORT_ID = "report_fpmarkets_v2_stage06_runtime_parity_blocked_v1"
PARSER_VERSION = "fpmarkets_v2_stage04_model_input_feature_set_v2_mt5_price_proxy_58"
PARSER_CONTRACT_VERSION = "docs/contracts/python_feature_parser_spec_fpmarkets_v2.md@2026-04-25"
FEATURE_CONTRACT_VERSION = "docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-25"
RUNTIME_CONTRACT_VERSION = "docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md@2026-04-25"
MT5_INPUT_ORDER_CONTRACT_VERSION = "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md@2026-04-25"

DEFAULT_MODEL_INPUT_PATH = (
    Path("data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58")
    / "model_input_dataset.parquet"
)
DEFAULT_MODEL_INPUT_SUMMARY_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_summary.json")
DEFAULT_WEIGHT_PATH = Path("foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv")
DEFAULT_STAGE05_AUDIT_PATH = (
    Path("stages/05_feature_integrity__formula_time_alignment_leakage_audit")
    / "02_runs/20260425_stage05_feature_integrity_audit_v1/audit_summary.json"
)
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
DEFAULT_MT5_SNAPSHOT_PATH = (
    Path.home()
    / "AppData/Roaming/MetaQuotes/Terminal/Common/Files/Project_Obsidian_Prime_v2/runtime_parity/"
    / f"{RUN_ID}/mt5_feature_snapshot.jsonl"
)
DEFAULT_MT5_SOURCE_PATHS = [
    Path("foundation/mt5/ObsidianPrimeV2_RuntimeParityAudit.mq5"),
    Path("foundation/mt5/ObsidianPrimeV2_RuntimeParityAuditEA.mq5"),
]

READY_TOLERANCE = 1e-5
BINARY_FEATURES = {
    "is_us_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
}
REQUIRED_IDENTITY_FIELDS = [
    "dataset_id",
    "fixture_set_id",
    "bundle_id",
    "runtime_id",
    "report_id",
    "parser_version",
    "feature_contract_version",
    "runtime_contract_version",
    "feature_order_hash",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Stage 06 runtime parity packet.")
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--model-input-summary-path", default=str(DEFAULT_MODEL_INPUT_SUMMARY_PATH))
    parser.add_argument("--weights-path", default=str(DEFAULT_WEIGHT_PATH))
    parser.add_argument("--stage05-audit-path", default=str(DEFAULT_STAGE05_AUDIT_PATH))
    parser.add_argument("--mt5-snapshot-path", default=str(DEFAULT_MT5_SNAPSHOT_PATH))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--tolerance", type=float, default=READY_TOLERANCE)
    parser.add_argument("--mt5-source-path", action="append", default=None)
    parser.add_argument("--compile-log-path", action="append", default=None)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def write_text(path: Path, text: str, *, encoding: str = "utf-8") -> None:
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text(text, encoding=encoding)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write_text(path, json.dumps(_json_ready(payload), indent=2), encoding="utf-8")


def _json_ready(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _iso(value: Any) -> str:
    return pd.Timestamp(value).isoformat()


def _event_time_payload(raw_broker_clock_key: pd.Timestamp) -> dict[str, str]:
    event_utc = pd.Timestamp(
        broker_clock_key_to_event_utc(pd.Series([raw_broker_clock_key], dtype="datetime64[ns, UTC]")).iloc[0]
    )
    timestamp_ny = event_utc.tz_convert("America/New_York")
    return {
        "raw_broker_clock_bar_close_key": raw_broker_clock_key.isoformat(),
        "timestamp_event_utc": event_utc.isoformat(),
        "timestamp_ny": timestamp_ny.isoformat(),
    }


def _feature_vector_hash(values: Iterable[float]) -> str:
    parts = [f"{float(value):.10g}" for value in values]
    return sha256_text("\n".join(parts))


def _base_identity() -> dict[str, str]:
    return {
        "dataset_id": MODEL_INPUT_DATASET_ID,
        "fixture_set_id": FIXTURE_SET_ID,
        "bundle_id": BUNDLE_ID,
        "runtime_id": RUNTIME_ID,
        "report_id": REPORT_ID,
        "parser_version": PARSER_VERSION,
        "parser_contract_version": PARSER_CONTRACT_VERSION,
        "feature_contract_version": FEATURE_CONTRACT_VERSION,
        "runtime_contract_version": RUNTIME_CONTRACT_VERSION,
        "mt5_input_order_contract_version": MT5_INPUT_ORDER_CONTRACT_VERSION,
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
    }


def _fixture_candidate(
    frame: pd.DataFrame,
    *,
    fixture_type: str,
    description: str,
    selector: pd.Series,
) -> dict[str, Any]:
    selected = frame.loc[selector].sort_values("timestamp")
    if selected.empty:
        raise RuntimeError(f"No Stage 06 fixture candidate found for {fixture_type}.")
    row = selected.iloc[0]
    return {
        "fixture_id": f"{fixture_type}_{pd.Timestamp(row['timestamp']).strftime('%Y%m%d_%H%M')}",
        "fixture_type": fixture_type,
        "description": description,
        "timestamp": pd.Timestamp(row["timestamp"]),
        "row_index": int(row.name),
    }


def select_fixture_set(frame: pd.DataFrame) -> list[dict[str, Any]]:
    work = frame.copy()
    work["timestamp"] = pd.to_datetime(work["timestamp"], utc=True)
    work = work.reset_index(drop=True)
    minutes = work["minutes_from_cash_open"].astype("float64")
    ts = work["timestamp"]
    finite_features = np.isfinite(work.loc[:, FEATURE_ORDER].to_numpy(dtype="float64")).all(axis=1)

    fixtures = [
        _fixture_candidate(
            work,
            fixture_type="regular_cash_session",
            description="US100 cash-session flow(US100 정규장 흐름) 안의 normal closed bar(정상 확정봉)",
            selector=(ts >= pd.Timestamp("2025-03-03T00:00:00Z")) & minutes.between(120.0, 180.0) & finite_features,
        ),
        _fixture_candidate(
            work,
            fixture_type="session_boundary_cash_open",
            description="cash-open boundary row(정규장 시작 경계 행)이며 session flags(세션 플래그)를 검증",
            selector=(ts >= pd.Timestamp("2024-06-01T00:00:00Z")) & minutes.eq(5.0) & finite_features,
        ),
        _fixture_candidate(
            work,
            fixture_type="dst_sensitive",
            description="New York DST transition week(뉴욕 서머타임 전환 주간) 이후 row(행)",
            selector=(
                (ts >= pd.Timestamp("2024-03-11T00:00:00Z"))
                & (ts <= pd.Timestamp("2024-03-15T23:59:59Z"))
                & minutes.between(30.0, 90.0)
                & finite_features
            ),
        ),
        _fixture_candidate(
            work,
            fixture_type="external_alignment",
            description="required external-symbol features(필수 외부 심볼 피처)를 모두 가진 row(행)",
            selector=(
                (ts >= pd.Timestamp("2025-01-02T00:00:00Z"))
                & minutes.between(60.0, 120.0)
                & finite_features
            ),
        ),
    ]

    negative_source = _fixture_candidate(
        work,
        fixture_type="negative_required_missing_input",
        description="synthetic required-missing-input fixture(합성 필수 입력 누락 표본); VIX 제거; row_ready(행 준비 상태)는 false(거짓)",
        selector=(ts >= pd.Timestamp("2025-01-02T00:00:00Z")) & minutes.between(60.0, 120.0) & finite_features,
    )
    negative_source["synthetic_missing_input"] = "VIX"
    negative_source["claim_scope"] = "validator_behavior_only_until_mt5_runtime_snapshot_exists"
    fixtures.append(negative_source)
    return fixtures


def build_python_snapshot_rows(frame: pd.DataFrame, fixtures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    identity = _base_identity()
    rows: list[dict[str, Any]] = []
    for fixture in fixtures:
        row = frame.iloc[int(fixture["row_index"])]
        timestamp = pd.Timestamp(row["timestamp"])
        event_payload = _event_time_payload(timestamp)
        feature_values = {feature: float(row[feature]) for feature in FEATURE_ORDER}
        is_negative = fixture["fixture_type"] == "negative_required_missing_input"
        if is_negative:
            feature_values = {feature: None for feature in FEATURE_ORDER}
            feature_ready_count = 0
            row_ready = False
            skip_reason = "required_missing_input:VIX"
            feature_vector_sha256 = None
        else:
            feature_ready_count = len(FEATURE_ORDER)
            row_ready = True
            skip_reason = ""
            feature_vector_sha256 = _feature_vector_hash(float(row[feature]) for feature in FEATURE_ORDER)

        rows.append(
            {
                **identity,
                "source_dataset_id": SOURCE_DATASET_ID,
                "snapshot_runtime": "python",
                "fixture_id": fixture["fixture_id"],
                "fixture_type": fixture["fixture_type"],
                "fixture_description": fixture["description"],
                **event_payload,
                "symbol": str(row.get("symbol", "US100")),
                "timeframe": "PERIOD_M5",
                "feature_count": len(FEATURE_ORDER),
                "feature_ready_count": feature_ready_count,
                "row_ready": row_ready,
                "skip_reason": skip_reason,
                "feature_vector_sha256": feature_vector_sha256,
                "synthetic_missing_input": fixture.get("synthetic_missing_input"),
                "features": feature_values,
            }
        )
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [json.dumps(_json_ready(row), sort_keys=True) for row in rows]
    write_text(path, "\n".join(lines) + "\n", encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _feature_map(row: dict[str, Any]) -> dict[str, Any]:
    features = row.get("features", {})
    if isinstance(features, dict):
        return features
    if isinstance(features, list):
        return {feature: value for feature, value in zip(FEATURE_ORDER, features, strict=False)}
    return {}


def compare_snapshot_rows(
    python_rows: list[dict[str, Any]],
    mt5_rows: list[dict[str, Any]],
    *,
    tolerance: float,
) -> dict[str, Any]:
    if not mt5_rows:
        return {
            "status": "blocked",
            "reason": "mt5_snapshot_missing",
            "compared_fixture_count": 0,
            "ready_fixture_count": int(sum(1 for row in python_rows if row["row_ready"])),
            "max_abs_diff": None,
            "failures": ["mt5_snapshot_missing"],
        }

    mt5_by_fixture = {str(row.get("fixture_id", row.get("target_id", ""))): row for row in mt5_rows}
    failures: list[str] = []
    max_abs_diff = 0.0
    max_abs_diff_feature = None
    compared = 0

    for python_row in python_rows:
        fixture_id = str(python_row["fixture_id"])
        mt5_row = mt5_by_fixture.get(fixture_id)
        if mt5_row is None:
            failures.append(f"{fixture_id}:mt5_fixture_missing")
            continue
        compared += 1

        for field in REQUIRED_IDENTITY_FIELDS:
            if str(python_row.get(field)) != str(mt5_row.get(field)):
                failures.append(f"{fixture_id}:{field}_mismatch")

        python_ready = bool(python_row.get("row_ready"))
        mt5_ready = bool(mt5_row.get("row_ready", mt5_row.get("feature_vector_complete", False)))
        if python_ready != mt5_ready:
            failures.append(f"{fixture_id}:row_ready_mismatch")
            continue
        if not python_ready:
            continue

        python_features = _feature_map(python_row)
        mt5_features = _feature_map(mt5_row)
        for feature in FEATURE_ORDER:
            if feature not in mt5_features:
                failures.append(f"{fixture_id}:{feature}_missing_in_mt5")
                continue
            left = float(python_features[feature])
            right = float(mt5_features[feature])
            abs_diff = abs(left - right)
            if abs_diff > max_abs_diff:
                max_abs_diff = abs_diff
                max_abs_diff_feature = feature
            if feature in BINARY_FEATURES:
                if int(round(left)) != int(round(right)):
                    failures.append(f"{fixture_id}:{feature}_binary_mismatch")
            elif abs_diff > tolerance:
                failures.append(f"{fixture_id}:{feature}_abs_diff_over_tolerance")

    return {
        "status": "pass" if not failures else "fail",
        "compared_fixture_count": compared,
        "ready_fixture_count": int(sum(1 for row in python_rows if row["row_ready"])),
        "max_abs_diff": max_abs_diff,
        "max_abs_diff_feature": max_abs_diff_feature,
        "tolerance": tolerance,
        "failures": failures,
    }


def audit_mt5_sources(paths: list[Path]) -> dict[str, Any]:
    items = []
    failures: list[str] = []
    for path in paths:
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        equal_weight_present = "g_top3_equal_weight" in text or "0.333333333333" in text
        current_dataset_present = MODEL_INPUT_DATASET_ID in text
        price_proxy_table_present = "top3_monthly_price_proxy_weights_fpmarkets_v2.csv" in text
        stale = exists and (equal_weight_present or not current_dataset_present or not price_proxy_table_present)
        if stale:
            failures.append(f"{path.as_posix()}:stale_price_proxy_surface")
        items.append(
            {
                "path": path.as_posix(),
                "exists": exists,
                "sha256": sha256_file(path) if exists else None,
                "equal_weight_marker_present": equal_weight_present,
                "current_dataset_id_present": current_dataset_present,
                "price_proxy_weight_table_present": price_proxy_table_present,
                "status": "stale_do_not_use_for_runtime_authority" if stale else "current_or_not_applicable",
            }
        )
    return {
        "status": "blocked" if failures else "pass",
        "items": items,
        "failures": failures,
    }


def summarize_compile_logs(paths: list[Path]) -> dict[str, Any]:
    items = []
    failures: list[str] = []
    for path in paths:
        if not path.exists():
            failures.append(f"{path.as_posix()}:compile_log_missing")
            items.append({"path": path.as_posix(), "exists": False, "status": "missing"})
            continue
        text = path.read_text(encoding="utf-16", errors="ignore")
        if len(text.strip()) == 0:
            text = path.read_text(encoding="utf-8", errors="ignore")
        lowered = text.lower()
        has_error = "error" in lowered and "0 error" not in lowered
        if has_error:
            failures.append(f"{path.as_posix()}:compile_error")
        items.append(
            {
                "path": path.as_posix(),
                "exists": True,
                "sha256": sha256_file(path),
                "line_count": len(text.splitlines()),
                "status": "compile_error_or_warning" if has_error else "available",
            }
        )
    return {"status": "pass" if not failures else "blocked", "items": items, "failures": failures}


def build_handoff_package(
    fixtures: list[dict[str, Any]],
    *,
    mt5_snapshot_path: Path,
    python_snapshot_path: Path,
    weights_path: Path,
) -> dict[str, Any]:
    target_windows = [
        pd.Timestamp(fixture["timestamp"]).strftime("%Y.%m.%d %H:%M:%S")
        for fixture in fixtures
        if fixture["fixture_type"] != "negative_required_missing_input"
    ]
    return {
        **_base_identity(),
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "target_windows_raw_broker_clock": target_windows,
        "target_windows_input_string": ";".join(target_windows),
        "negative_fixture": {
            "fixture_id": next(
                fixture["fixture_id"] for fixture in fixtures if fixture["fixture_type"] == "negative_required_missing_input"
            ),
            "required_missing_input": "VIX",
            "expected_row_ready": False,
        },
        "python_snapshot_path": python_snapshot_path.as_posix(),
        "expected_mt5_snapshot_path": mt5_snapshot_path.as_posix(),
        "weights_path": weights_path.as_posix(),
        "mt5_tool_boundary": (
            "Checked-in MT5 audit tools(저장소 MT5 감사 도구)는 MT5 price-proxy monthly top3 weights"
            "(MT5 가격 대리 월별 top3 가중치)를 읽고 이 package(묶음)와 같은 identity fields"
            "(정체성 필드)를 출력하기 전까지 stale(낡음)로 다룬다."
        ),
    }


def build_stage06_audit(
    *,
    model_input_path: Path,
    model_input_summary_path: Path,
    weights_path: Path,
    stage05_audit_path: Path,
    mt5_snapshot_path: Path,
    mt5_source_paths: list[Path],
    compile_log_paths: list[Path],
    run_output_root: Path,
    tolerance: float,
) -> dict[str, Any]:
    frame = pd.read_parquet(model_input_path)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    model_input_summary = read_json(model_input_summary_path)
    stage05_audit = read_json(stage05_audit_path)

    fixtures = select_fixture_set(frame)
    python_rows = build_python_snapshot_rows(frame, fixtures)
    mt5_rows = read_jsonl(mt5_snapshot_path)
    comparison = compare_snapshot_rows(python_rows, mt5_rows, tolerance=tolerance)
    mt5_source_audit = audit_mt5_sources(mt5_source_paths)
    compile_log_audit = summarize_compile_logs(compile_log_paths) if compile_log_paths else {
        "status": "not_attempted",
        "items": [],
        "failures": ["compile_log_not_supplied"],
    }

    external_failures = []
    if comparison["status"] != "pass":
        external_failures.extend(comparison.get("failures", []))
    if mt5_source_audit["status"] != "pass":
        external_failures.extend(mt5_source_audit.get("failures", []))
    if compile_log_audit["status"] in {"blocked", "not_attempted"}:
        external_failures.extend(compile_log_audit.get("failures", []))

    external_verification_status = "completed" if not external_failures else "blocked"
    judgment = (
        "positive_runtime_parity_passed"
        if external_verification_status == "completed"
        else "blocked_runtime_authority_mt5_snapshot_missing_or_stale"
    )
    stage_status = (
        "reviewed_runtime_parity_closed"
        if external_verification_status == "completed"
        else "reviewed_blocked_handoff"
    )

    python_snapshot_path = run_output_root / "python_feature_snapshot.jsonl"
    handoff = build_handoff_package(
        fixtures,
        mt5_snapshot_path=mt5_snapshot_path,
        python_snapshot_path=python_snapshot_path,
        weights_path=weights_path,
    )

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": LANE,
        "secondary_lane": "evidence",
        "materializer_version": MATERIALIZER_VERSION,
        "status": "reviewed",
        "stage_status": stage_status,
        "judgment": judgment,
        "external_verification_status": external_verification_status,
        "hard_gate_applicable": "yes",
        "runtime_state": "runtime_authority" if external_verification_status == "completed" else "runtime_probe_blocked",
        "feature_order_hash": EXPECTED_FEATURE_ORDER_HASH,
        "tolerance": tolerance,
        "source_dataset_id": SOURCE_DATASET_ID,
        "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
        "model_input_rows": int(model_input_summary["rows"]),
        "stage05_judgment": stage05_audit["judgment"],
        "input_hashes": {
            "model_input_dataset_sha256": sha256_file(model_input_path),
            "model_input_summary_sha256": sha256_file(model_input_summary_path),
            "weights_sha256": sha256_file(weights_path),
            "stage05_audit_sha256": sha256_file(stage05_audit_path),
        },
        "fixtures": [
            {
                key: (_iso(value) if key == "timestamp" else value)
                for key, value in fixture.items()
                if key != "row_index"
            }
            for fixture in fixtures
        ],
        "snapshot_counts": {
            "python_rows": len(python_rows),
            "mt5_rows": len(mt5_rows),
        },
        "comparison": comparison,
        "mt5_source_audit": mt5_source_audit,
        "compile_log_audit": compile_log_audit,
        "handoff_package": handoff,
        "evidence_boundary": (
            "Stage 06 run evidence(Stage 06 실행 근거) only(한정). runtime authority(런타임 권위)를 "
            "주장하려면 completed MT5 runtime snapshot(완료된 MT5 런타임 스냅샷)이 필요하다. "
            "blocked(차단) 상태에서는 fixture packet(표본 묶음), Python snapshot(파이썬 스냅샷), "
            "stale MT5 tool audit(낡은 MT5 도구 감사), retry condition(재시도 조건)만 기록한다."
        ),
        "blockers": external_failures,
        "_python_rows": python_rows,
    }


def render_result_summary(audit: dict[str, Any]) -> str:
    closed_text = (
        "닫힘(closed, 닫힘)"
        if audit["external_verification_status"] == "completed"
        else "차단(blocked, 차단)"
    )
    lines = [
        "# Stage 06 Runtime Parity v1",
        "",
        f"- run_id(실행 ID): `{audit['run_id']}`",
        f"- status(상태): `{closed_text}`",
        f"- judgment(판정): `{audit['judgment']}`",
        f"- external_verification_status(외부 검증 상태): `{audit['external_verification_status']}`",
        f"- runtime_state(런타임 상태): `{audit['runtime_state']}`",
        f"- feature_order_hash(피처 순서 해시): `{audit['feature_order_hash']}`",
        "",
        "## Result(결과)",
        "",
    ]
    if audit["external_verification_status"] == "completed":
        lines.append(
            "Python snapshot(파이썬 스냅샷)과 MT5 snapshot(MT5 스냅샷)이 허용오차(tolerance, 허용오차) 안에서 맞았다."
        )
    else:
        lines.append(
            "Python snapshot(파이썬 스냅샷)과 MT5 handoff package(MT5 인계 묶음)는 만들었지만, "
            "현재 MT5 snapshot(MT5 스냅샷)이 없거나 MT5 audit tool(MT5 감사 도구)이 stale(낡음) 상태라 "
            "runtime authority(런타임 권위)는 닫지 않는다."
        )
    lines.extend(
        [
            "",
            "## Fixtures(표본)",
            "",
        ]
    )
    for fixture in audit["fixtures"]:
        lines.append(f"- `{fixture['fixture_id']}`: {fixture['description']}")

    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            (
                "이 실행(run, 실행)은 Stage 06(6단계)의 차단 또는 폐쇄 근거(evidence, 근거)다. "
                "model quality(모델 품질), alpha quality(알파 품질), operating promotion(운영 승격)은 주장하지 않는다."
            ),
        ]
    )
    if audit["blockers"]:
        lines.extend(["", "## Blockers(차단 사유)", ""])
        for blocker in audit["blockers"]:
            lines.append(f"- `{blocker}`")
    return "\n".join(lines) + "\n"


def write_stage06_outputs(audit: dict[str, Any], run_output_root: Path) -> dict[str, str]:
    run_output_root.mkdir(parents=True, exist_ok=True)
    paths = {
        "fixture_set": run_output_root / "fixture_set.json",
        "python_snapshot": run_output_root / "python_feature_snapshot.jsonl",
        "mt5_handoff_package": run_output_root / "mt5_handoff_package.json",
        "runtime_parity_report": run_output_root / "runtime_parity_report.json",
        "run_manifest": run_output_root / "run_manifest.json",
        "kpi_record": run_output_root / "kpi_record.json",
        "result_summary": run_output_root / "result_summary.md",
    }

    write_json(paths["fixture_set"], {"fixture_set_id": FIXTURE_SET_ID, "fixtures": audit["fixtures"]})
    write_jsonl(paths["python_snapshot"], audit["_python_rows"])
    write_json(paths["mt5_handoff_package"], audit["handoff_package"])

    report = {key: value for key, value in audit.items() if key != "_python_rows"}
    write_json(paths["runtime_parity_report"], report)

    run_manifest = {
        "run_id": audit["run_id"],
        "stage_id": audit["stage_id"],
        "lane": audit["lane"],
        "status": audit["status"],
        "command": "python foundation/parity/stage06_runtime_parity.py",
        "inputs": {
            "model_input_dataset_id": audit["model_input_dataset_id"],
            "source_dataset_id": audit["source_dataset_id"],
            "stage05_judgment": audit["stage05_judgment"],
        },
        "outputs": {key: path.as_posix() for key, path in paths.items()},
        "external_check_logs": [
            item["path"] for item in audit["compile_log_audit"].get("items", []) if item.get("exists")
        ],
        "judgment": audit["judgment"],
        "external_verification_status": audit["external_verification_status"],
        "evidence_boundary": audit["evidence_boundary"],
    }
    write_json(paths["run_manifest"], run_manifest)

    kpi_record = {
        "run_id": audit["run_id"],
        "scoreboard": "runtime_parity",
        "measurement_scope": "python_snapshot_mt5_snapshot_identity_feature_vector_parity",
        "judgment": audit["judgment"],
        "runtime_state": audit["runtime_state"],
        "hard_gate_applicable": audit["hard_gate_applicable"],
        "external_verification_status": audit["external_verification_status"],
        "measurement": {
            "fixture_count": len(audit["fixtures"]),
            "python_snapshot_rows": audit["snapshot_counts"]["python_rows"],
            "mt5_snapshot_rows": audit["snapshot_counts"]["mt5_rows"],
            "comparison_status": audit["comparison"]["status"],
            "max_abs_diff": audit["comparison"]["max_abs_diff"],
            "stale_mt5_source_status": audit["mt5_source_audit"]["status"],
            "compile_log_status": audit["compile_log_audit"]["status"],
        },
        "registry_update_required": "yes",
    }
    write_json(paths["kpi_record"], kpi_record)
    write_text(paths["result_summary"], render_result_summary(report), encoding="utf-8-sig")
    return {key: path.as_posix() for key, path in paths.items()}


def main() -> int:
    args = parse_args()
    mt5_source_paths = [Path(path) for path in args.mt5_source_path] if args.mt5_source_path else DEFAULT_MT5_SOURCE_PATHS
    compile_log_paths = [Path(path) for path in args.compile_log_path] if args.compile_log_path else []
    run_output_root = Path(args.run_output_root)
    audit = build_stage06_audit(
        model_input_path=Path(args.model_input_path),
        model_input_summary_path=Path(args.model_input_summary_path),
        weights_path=Path(args.weights_path),
        stage05_audit_path=Path(args.stage05_audit_path),
        mt5_snapshot_path=Path(args.mt5_snapshot_path),
        mt5_source_paths=mt5_source_paths,
        compile_log_paths=compile_log_paths,
        run_output_root=run_output_root,
        tolerance=args.tolerance,
    )
    outputs = write_stage06_outputs(audit, run_output_root)
    payload = {
        "status": "ok",
        "run_id": audit["run_id"],
        "stage_status": audit["stage_status"],
        "judgment": audit["judgment"],
        "external_verification_status": audit["external_verification_status"],
        "outputs": outputs,
        "blockers": audit["blockers"],
    }
    print(json.dumps(_json_ready(payload), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
