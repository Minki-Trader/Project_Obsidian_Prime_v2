from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

STAGE_ID = "326_forward__cp322a_frozen_forward_gate"
RUN_ID = "run326A_cp322a_frozen_forward_robustness_gate_v1"
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / "run326A"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"

RAW_DIR = INPUTS_DIR / "raw_m5"
RAW_SUMMARY = RAW_DIR / "stage01_raw_export_summary.json"

ADAPTER_DIR = (
    ROOT
    / "stages"
    / "323_onnx_candidate_campaign__selected_curve_adapter_package"
    / "02_runs"
    / "run323A"
    / "adapter_package"
)
ONNX_MODEL = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
    / "models"
    / "cp322a_route_signal_identity.onnx"
)
SOURCE_FEATURE_DIR = (
    ROOT
    / "stages"
    / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
    / "02_runs"
    / "run322B"
    / "features"
)
SOURCE_PAYLOAD = (
    ROOT
    / "stages"
    / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
    / "02_runs"
    / "run322A"
    / "payloads"
    / "run322A_cp322A_cp321b_exact_replay_control_payload.parquet"
)

FORWARD_START_UTC = "2026-04-14T00:00:00Z"
REQUIRED_REGIME_SYMBOLS = ("VIX", "USDX", "US10YR")
REQUIRED_FORWARD_FEATURE = "run322b_route_signal"
DECISION = "Forward Blocked"
CLAIM_BOUNDARY = (
    "forward robustness only; no live readiness, deployment, operating promotion, "
    "runtime authority, or operating reference"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def unix_to_iso(value: int | str | None) -> str | None:
    if value in (None, ""):
        return None
    return datetime.fromtimestamp(int(value), timezone.utc).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    encoding = "utf-8-sig" if has_bom else "utf-8"
    return raw.decode(encoding), has_bom


def detect_newline(text: str) -> str:
    return "\r\n" if text.count("\r\n") > text.count("\n") / 2 else "\n"


def write_text_preserving_bom(path: Path, text: str, had_bom: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    path.write_bytes(text.encode(encoding))


def lines_with_newline(text: str, newline: str) -> str:
    return newline.join(text.splitlines()) + newline


def csv_row_count_and_time_stats(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False}
    count = 0
    duplicates = 0
    non_monotonic = 0
    largest_gap_seconds = 0
    previous: int | None = None
    seen: set[int] = set()
    first_ts: int | None = None
    last_ts: int | None = None
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            count += 1
            ts = int(row["time_open_unix"])
            if first_ts is None:
                first_ts = ts
            last_ts = ts
            if ts in seen:
                duplicates += 1
            seen.add(ts)
            if previous is not None:
                if ts <= previous:
                    non_monotonic += 1
                largest_gap_seconds = max(largest_gap_seconds, ts - previous)
            previous = ts
    return {
        "exists": True,
        "csv_row_count": count,
        "first_open_utc": unix_to_iso(first_ts),
        "last_open_utc": unix_to_iso(last_ts),
        "duplicate_open_times": duplicates,
        "non_monotonic_steps": non_monotonic,
        "largest_gap_seconds": largest_gap_seconds,
    }


def compute_status(data_receipt: dict[str, Any], gap: dict[str, Any]) -> str:
    data_blocked = data_receipt["blocking_status"] == "blocked_forward_data_missing"
    signal_blocked = gap["blocking_status"] == "blocked_forward_signal_handoff_missing"
    if data_blocked and signal_blocked:
        return "blocked_forward_data_missing_and_signal_handoff_missing"
    if data_blocked:
        return "blocked_forward_data_missing"
    if signal_blocked:
        return "blocked_forward_signal_handoff_missing"
    return "blocked_forward_unknown"


def build_blocked_reasons(data_receipt: dict[str, Any], gap: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if data_receipt["blocking_status"] == "blocked_forward_data_missing":
        missing = ", ".join(data_receipt["required_incomplete_symbols"]) or "unknown"
        reasons.append(
            f"`blocked_forward_data_missing`(전진 데이터 누락/불완전): required regime data(필수 국면 데이터) 중 {missing}이 forward end(전진 종료)에 닿지 못했다."
        )
    if gap["blocking_status"] == "blocked_forward_signal_handoff_missing":
        reasons.append(
            "`blocked_forward_signal_handoff_missing`(전진 신호 인계 누락): frozen ONNX(고정 오닉스)가 요구하는 `run322b_route_signal` forward CSV(전진 씨에스브이)가 없다."
        )
    return reasons


def analyze_forward_data(generated_at_utc: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    summary = read_json(RAW_SUMMARY)
    requested_to_unix = int(
        datetime.fromisoformat(summary["requested_to_utc"].replace("Z", "+00:00")).timestamp()
    )
    rows: list[dict[str, Any]] = []
    for item in summary["exported_symbols"]:
        symbol = item["contract_symbol"]
        csv_path = Path(item["csv_path"])
        manifest_path = Path(item["manifest_path"])
        manifest = read_json(manifest_path)
        stats = csv_row_count_and_time_stats(csv_path)
        last_open = int(item["last_open_unix"]) if item.get("last_open_unix") else None
        end_gap_seconds = requested_to_unix - last_open if last_open else None
        required = symbol in ("US100", *REQUIRED_REGIME_SYMBOLS)
        complete_to_requested_end = bool(end_gap_seconds is not None and end_gap_seconds <= 24 * 60 * 60)
        rows.append(
            {
                "symbol": symbol,
                "broker_symbol": item.get("broker_symbol"),
                "required_for_forward_gate": "yes" if required else "supporting_context",
                "row_count": item.get("row_count"),
                "csv_row_count": stats.get("csv_row_count"),
                "first_open_utc": unix_to_iso(item.get("first_open_unix")),
                "last_open_utc": unix_to_iso(item.get("last_open_unix")),
                "requested_to_utc": summary["requested_to_utc"],
                "end_gap_hours": round((end_gap_seconds or 0) / 3600, 2) if end_gap_seconds is not None else "",
                "complete_to_requested_end": "yes" if complete_to_requested_end else "no",
                "duplicate_open_times": stats.get("duplicate_open_times", ""),
                "non_monotonic_steps": stats.get("non_monotonic_steps", ""),
                "largest_gap_seconds": stats.get("largest_gap_seconds", ""),
                "timezone_status": manifest.get("timezone_status"),
                "csv_path": rel(csv_path),
                "manifest_path": rel(manifest_path),
            }
        )
    required_incomplete = [
        row["symbol"]
        for row in rows
        if row["required_for_forward_gate"] == "yes" and row["complete_to_requested_end"] != "yes"
    ]
    core_us100 = next(row for row in rows if row["symbol"] == "US100")
    receipt = {
        "receipt_id": "run326A_forward_data_integrity_receipt",
        "generated_at_utc": generated_at_utc,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "requested_from_utc": summary["requested_from_utc"],
        "requested_to_utc": summary["requested_to_utc"],
        "core_us100_status": "present_for_forward_window" if core_us100["complete_to_requested_end"] == "yes" else "incomplete",
        "required_regime_symbols": list(REQUIRED_REGIME_SYMBOLS),
        "required_incomplete_symbols": required_incomplete,
        "blocking_status": "blocked_forward_data_missing" if required_incomplete else "core_data_available",
        "note": (
            "US100 forward bars are present, but required regime slices cannot be called complete "
            "because at least one required regime symbol does not cover the requested forward end."
        )
        if required_incomplete
        else "Required forward data coverage is present.",
        "symbol_rows": rows,
    }
    return receipt, rows


def audit_frozen_contract(generated_at_utc: str) -> tuple[dict[str, Any], dict[str, Any]]:
    runtime_feature_order = ADAPTER_DIR / "feature_order_runtime.csv"
    decision_surface = ADAPTER_DIR / "decision_surface.json"
    risk_logic = ADAPTER_DIR / "risk_logic.json"
    handoff_manifest = ADAPTER_DIR / "runtime_handoff_manifest.json"
    source_route_signal_files = sorted(SOURCE_FEATURE_DIR.glob("*route_signal.csv"))
    forward_route_signal_files = sorted(STAGE_DIR.glob("**/*route_signal*.csv"))
    runtime_feature_text = runtime_feature_order.read_text(encoding="utf-8-sig")
    feature_order_locked = REQUIRED_FORWARD_FEATURE in runtime_feature_text
    contract = {
        "receipt_id": "run326A_frozen_contract_receipt",
        "generated_at_utc": generated_at_utc,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "selected_candidate": "cp322A_cp321b_exact_replay_control_surface",
        "frozen_package": "cp322A_cp321b_exact_replay_control_surface",
        "onnx_model_path": rel(ONNX_MODEL),
        "onnx_model_sha256": sha256_file(ONNX_MODEL) if ONNX_MODEL.exists() else None,
        "adapter_package_path": rel(ADAPTER_DIR),
        "adapter_manifest_path": rel(handoff_manifest),
        "adapter_manifest_sha256": sha256_file(handoff_manifest) if handoff_manifest.exists() else None,
        "runtime_feature_order_path": rel(runtime_feature_order),
        "runtime_feature_order_sha256": sha256_file(runtime_feature_order),
        "decision_surface_path": rel(decision_surface),
        "decision_surface_sha256": sha256_file(decision_surface),
        "risk_logic_path": rel(risk_logic),
        "risk_logic_sha256": sha256_file(risk_logic),
        "feature_order_locked": feature_order_locked,
        "required_runtime_feature": REQUIRED_FORWARD_FEATURE,
        "source_payload_path": rel(SOURCE_PAYLOAD),
        "source_payload_sha256": sha256_file(SOURCE_PAYLOAD) if SOURCE_PAYLOAD.exists() else None,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gap = {
        "receipt_id": "run326A_runtime_handoff_gap_receipt",
        "generated_at_utc": generated_at_utc,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "required_runtime_feature": REQUIRED_FORWARD_FEATURE,
        "existing_source_route_signal_files": [rel(p) for p in source_route_signal_files],
        "forward_route_signal_files_found": [rel(p) for p in forward_route_signal_files],
        "forward_route_signal_available": bool(forward_route_signal_files),
        "mt5_forward_run_allowed": False,
        "blocking_status": "blocked_forward_signal_handoff_missing",
        "reason": (
            "The frozen ONNX model consumes the already materialized route signal. "
            "No frozen forward route-signal producer or forward feature CSV exists for the 2026-04-14+ window."
        ),
        "forbidden_repairs_in_this_gate": [
            "new_data_retraining",
            "score_threshold_refit",
            "D_or_B_rule_change",
            "lot_optimization",
            "risk_logic_change",
        ],
    }
    return contract, gap


def upsert_csv(path: Path, key_columns: list[str], row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    had_bom = False
    if path.exists():
        had_bom = path.read_bytes().startswith(b"\xef\xbb\xbf")
        with path.open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or row.keys())
            rows = list(reader)
    else:
        fieldnames = list(row.keys())
        rows = []
    for key in row:
        if key not in fieldnames:
            fieldnames.append(key)
    rows = [
        existing
        for existing in rows
        if not all(existing.get(col) == str(row.get(col, "")) for col in key_columns)
    ]
    rows.append({k: str(row.get(k, "")) for k in fieldnames})
    encoding = "utf-8-sig" if had_bom else "utf-8"
    with path.open("w", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_reports(
    generated_at_utc: str,
    data_receipt: dict[str, Any],
    data_rows: list[dict[str, Any]],
    contract: dict[str, Any],
    gap: dict[str, Any],
) -> list[Path]:
    status = compute_status(data_receipt, gap)
    blocked_reasons = build_blocked_reasons(data_receipt, gap)
    blocked_reason_text = chr(10).join(f"- {reason}" for reason in blocked_reasons)
    data_missing = data_receipt["blocking_status"] == "blocked_forward_data_missing"
    if data_missing:
        regime_status = "`blocked_forward_data_missing`(전진 데이터 누락/불완전)"
        regime_body = """
- VIX(VIX 변동성 지수), USDX(달러 지수), US10YR(미국 10년물) are required regime slices(필수 국면 구간) for this gate(게이트).
- At least one required regime symbol(필수 국면 심볼)이 requested forward end(요청 전진 종료)에 닿지 못했다.
- effect(효과): session/hour/month/volatility/ADX/VIX/USD/rate regime slices(세션/시간/월/변동성/ADX/VIX/달러/금리 국면 구간)를 성공 판정 근거로 사용할 수 없다.
"""
        regime_repair = """
1. US10YR/VIX/USDX forward M5(5분봉)를 US100(나스닥100) 종료 시점까지 확보한다.
2. timestamp/timezone binding(타임스탬프/시간대 묶음)을 명시한다.
3. 그 다음 frozen signal handoff(고정 신호 인계)를 먼저 만든다.
"""
    else:
        regime_status = "`coverage_available_with_timezone_boundary`(범위 확보, 시간대 경계 남음)"
        regime_body = """
- VIX(VIX 변동성 지수), USDX(달러 지수), US10YR(미국 10년물) required regime data(필수 국면 데이터)는 requested forward end(요청 전진 종료)에 닿았다.
- timezone status(시간대 상태)는 raw manifest(원천 목록)에서 `UNRESOLVED_REQUIRES_MANUAL_BINDING`로 남아 있다.
- effect(효과): 1번 data missing blocker(데이터 누락 차단)는 해소됐지만, positive forward judgment(긍정 전진 판정)에는 frozen signal handoff(고정 신호 인계)와 시간대 묶음 확인이 여전히 필요하다.
"""
        regime_repair = """
1. timestamp/timezone binding(타임스탬프/시간대 묶음)을 명시한다.
2. frozen route-signal handoff(고정 경로 신호 인계)를 만든다.
3. 그 다음 MT5 forward run(MT5 전진 실행)을 수행한다.
"""
    common_boundary = (
        "Boundary(경계): 이 판단은 forward robustness(전진 견고성) 게이트만 다룬다. "
        "live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), "
        "runtime authority(런타임 권위), operating reference(운영 기준)는 주장하지 않는다."
    )
    paths: list[Path] = []

    stage_brief = f"""
# Stage326 cp322A Frozen Forward Robustness Gate(326단계 cp322A 고정 전진 견고성 게이트)

- run(실행): `{RUN_ID}`
- selected candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface`
- frozen package(고정 패키지): `cp322A_cp321b_exact_replay_control_surface`
- forward window(전진 구간): `{FORWARD_START_UTC}` 이후부터 latest available MT5 broker data(최신 확보 가능 MT5 브로커 데이터)
- decision(판정): `{DECISION}`(전진 차단)
- status(상태): `{status}`
- effect(효과): 후보를 고치지 않고, forward 판단을 막는 데이터/인계 공백을 근거로 고정한다.

{common_boundary}
"""
    path = SPEC_DIR / "stage_brief.md"
    write_md(path, stage_brief)
    paths.append(path)

    input_refs = f"""
# run326A Input References(입력 참조)

- raw export summary(원천 내보내기 요약): `{rel(RAW_SUMMARY)}`
- adapter package(어댑터 패키지): `{rel(ADAPTER_DIR)}`
- ONNX model(오닉스 모델): `{rel(ONNX_MODEL)}`
- source route signal directory(원천 경로 신호 폴더): `{rel(SOURCE_FEATURE_DIR)}`
- action/effect(행동/효과): 입력 경로를 고정해, 후보 수정 없이 forward(전진) 실행 가능성을 확인했다.
"""
    path = INPUTS_DIR / "input_refs.md"
    write_md(path, input_refs)
    paths.append(path)

    frozen_mt5_report = f"""
# Frozen Forward MT5 Report(고정 전진 MT5 보고서)

## Decision(판정)

`{DECISION}`(전진 차단). MT5 forward run(MT5 전진 실행)은 수행하지 않았다.

## Why(이유)

{blocked_reason_text}

## Data read(데이터 판독)

- US100(나스닥100 브로커 심볼) forward bars(전진 봉): `{data_receipt['core_us100_status']}`
- required incomplete symbols(필수 불완전 심볼): `{', '.join(data_receipt['required_incomplete_symbols']) or 'none'}`
- effect(효과): net profit(순수익), PF(수익 팩터), trades/day(일 거래수), DD(drawdown, 손실폭), recovery(회복), expectancy(기대값)는 계산하지 않았다. 계산하면 frozen input(고정 입력) 없이 만든 숫자가 되어 판정 근거가 오염된다.

{common_boundary}
"""
    path = REVIEWS_DIR / "frozen_forward_mt5_report.md"
    write_md(path, frozen_mt5_report)
    paths.append(path)

    regime_report = f"""
# Regime Attribution Report(국면 귀속 보고서)

## Status(상태)

{regime_status}.

## Evidence(근거)

{regime_body.strip()}

## Required repair(필수 수정)

{regime_repair.strip()}
"""
    path = REVIEWS_DIR / "regime_attribution_report.md"
    write_md(path, regime_report)
    paths.append(path)

    db_report = f"""
# D/B Attribution Report(D/B 귀속 보고서)

## Status(상태)

`blocked_forward_signal_handoff_missing`(전진 신호 인계 누락).

## Evidence(근거)

- frozen ONNX(고정 오닉스) input(입력): `{REQUIRED_FORWARD_FEATURE}`
- source feature files(원천 피처 파일): `{len(gap['existing_source_route_signal_files'])}` old validation/OOS(과거 검증/표본외) files only.
- forward route signal files(전진 경로 신호 파일): `{len(gap['forward_route_signal_files_found'])}`
- effect(효과): D source(D 원천), B source(B 원천), D+B attribution(D+B 귀속), long/short attribution(롱/숏 귀속)을 forward window(전진 구간)에서 계산하지 않았다.

## Boundary(경계)

새 데이터로 score threshold(점수 임계값), D/B rule(D/B 규칙), source priority(원천 우선순위)를 다시 맞추지 않았다.
"""
    path = REVIEWS_DIR / "d_b_attribution_report.md"
    write_md(path, db_report)
    paths.append(path)

    lot_report = f"""
# Lot-Normalized Report(로트 정규화 보고서)

## Status(상태)

Not computed(계산 안 함).

## Reason(이유)

MT5 forward trades(MT5 전진 거래)가 없어서 lot-normalized net(로트 정규화 순손익), expectancy(기대값), DD(drawdown, 손실폭)를 만들 수 없다.

effect(효과): fixed lot(고정 로트), model risk sizing(모델 위험 크기), ATR SL/TP(ATR 손절/익절)을 바꾸지 않았고, lot optimization(로트 최적화)도 하지 않았다.
"""
    path = REVIEWS_DIR / "lot_normalized_report.md"
    write_md(path, lot_report)
    paths.append(path)

    stress_report = f"""
# Cost Stress Report(비용 압박 보고서)

## Status(상태)

Not computed(계산 안 함).

## Reason(이유)

forward MT5 trade list(전진 MT5 거래 목록)가 없으므로 spread/slippage stress(스프레드/슬리피지 압박)를 수행할 수 없다.

effect(효과): 비용 압박을 생략한 positive judgment(긍정 판정)를 만들지 않는다.
"""
    path = REVIEWS_DIR / "cost_stress_report.md"
    write_md(path, stress_report)
    paths.append(path)

    curve_report = f"""
# Curve Pocket Report(곡선 포켓 보고서)

## Status(상태)

Not computed(계산 안 함).

## Reason(이유)

forward equity curve(전진 평가금 곡선)가 없어서 worst chunk(최악 구간), underwater stretch(수중 구간), curve pocket(곡선 포켓)을 판정하지 않는다.

effect(효과): 곡선 근거 없이 `Forward Passed`(전진 통과)를 주장하지 않는다.
"""
    path = REVIEWS_DIR / "curve_pocket_report.md"
    write_md(path, curve_report)
    paths.append(path)

    final_report = f"""
# Final Forward Decision Report(최종 전진 판정 보고서)

## Decision(판정)

`{DECISION}`(전진 차단)

## Status(상태)

`{status}`

## Blocking facts(차단 사실)

{blocked_reason_text}

## What was not changed(변경하지 않은 것)

- selected candidate(선택 후보)
- ONNX model(오닉스 모델)
- Adapter package(어댑터 패키지)
- feature order(피처 순서)
- D/B decision surface(D/B 판단 표면)
- score threshold(점수 임계값)
- risk logic(위험 로직)
- lot logic(로트 로직)
- ATR SL/TP(ATR 손절/익절)
- runtime handoff(런타임 인계)

## Judgment boundary(판정 경계)

cp322A(322A 후보)는 ONNX research artifact(오닉스 연구 산출물)로 보존한다. Forward Passed(전진 통과), Forward Failed(전진 실패), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위)는 주장하지 않는다.

## Next exact repair(다음 정확한 수정)

1. Create a frozen forward route-signal handoff(고정 전진 경로 신호 인계)를 만든다. 이때 score threshold(점수 임계값)와 D/B rule(D/B 규칙)을 새 데이터에 맞추지 않는다.
2. Confirm timestamp/timezone binding(타임스탬프/시간대 묶음 확인)을 한다.
3. Then run MT5 forward(그 다음 MT5 전진 실행)를 수행하고, net/PF/DD/curve pocket(순손익/수익 팩터/손실폭/곡선 포켓)을 다시 판정한다.

effect(효과): 현재 작업은 success(성공)가 아니라 blocked(차단)로 닫아, 후보 과대 주장과 데이터 누락 판정을 분리한다.
"""
    path = REVIEWS_DIR / "final_forward_decision_report.md"
    write_md(path, final_report)
    paths.append(path)

    review_index = f"""
# Stage326 Review Index(검토 색인)

- frozen forward MT5 report(고정 전진 MT5 보고서): `{rel(REVIEWS_DIR / 'frozen_forward_mt5_report.md')}`
- regime attribution report(국면 귀속 보고서): `{rel(REVIEWS_DIR / 'regime_attribution_report.md')}`
- D/B attribution report(D/B 귀속 보고서): `{rel(REVIEWS_DIR / 'd_b_attribution_report.md')}`
- lot-normalized report(로트 정규화 보고서): `{rel(REVIEWS_DIR / 'lot_normalized_report.md')}`
- cost stress report(비용 압박 보고서): `{rel(REVIEWS_DIR / 'cost_stress_report.md')}`
- curve pocket report(곡선 포켓 보고서): `{rel(REVIEWS_DIR / 'curve_pocket_report.md')}`
- final forward decision report(최종 전진 판정 보고서): `{rel(REVIEWS_DIR / 'final_forward_decision_report.md')}`
"""
    path = REVIEWS_DIR / "review_index.md"
    write_md(path, review_index)
    paths.append(path)

    selection_status = f"""
# cp322A Selection Status After Stage326(Stage326 이후 cp322A 선택 상태)

- selected candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface`
- package status(패키지 상태): ONNX research artifact preserved(오닉스 연구 산출물 보존)
- forward decision(전진 판정): `{DECISION}`(전진 차단)
- blocker(차단 사유): `{status}`
- operating status(운영 상태): no live readiness(실거래 준비 없음), no deployment(배포 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no operating reference(운영 기준 없음)
- effect(효과): cp322A(322A 후보)는 폐기하지 않고 보존하지만, forward robustness(전진 견고성) 통과 후보로도 올리지 않는다.
"""
    path = SELECTED_DIR / "selection_status.md"
    write_md(path, selection_status)
    paths.append(path)

    data_audit = STAGE_DIR / "02_runs" / "run326A" / "forward_data_symbol_coverage.csv"
    write_csv(
        data_audit,
        [
            "symbol",
            "broker_symbol",
            "required_for_forward_gate",
            "row_count",
            "csv_row_count",
            "first_open_utc",
            "last_open_utc",
            "requested_to_utc",
            "end_gap_hours",
            "complete_to_requested_end",
            "duplicate_open_times",
            "non_monotonic_steps",
            "largest_gap_seconds",
            "timezone_status",
            "csv_path",
            "manifest_path",
        ],
        data_rows,
    )
    paths.append(data_audit)

    return paths


def write_receipts(generated_at_utc: str, data_receipt: dict[str, Any], contract: dict[str, Any], gap: dict[str, Any]) -> list[Path]:
    status = compute_status(data_receipt, gap)
    paths: list[Path] = []
    for name, payload in [
        ("forward_data_integrity_receipt.json", data_receipt),
        ("frozen_contract_receipt.json", contract),
        ("runtime_handoff_gap_receipt.json", gap),
    ]:
        path = RUN_DIR / name
        write_json(path, payload)
        paths.append(path)

    run_manifest = {
        "manifest_id": "run326A_cp322a_frozen_forward_robustness_gate_manifest",
        "generated_at_utc": generated_at_utc,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "decision": DECISION,
        "status": status,
        "forward_window_start_utc": FORWARD_START_UTC,
        "mt5_forward_run_attempted": False,
        "mt5_forward_run_blocked_reason": status,
        "selected_candidate": "cp322A_cp321b_exact_replay_control_surface",
        "claim_boundary": CLAIM_BOUNDARY,
        "receipts": [
            rel(RUN_DIR / "forward_data_integrity_receipt.json"),
            rel(RUN_DIR / "frozen_contract_receipt.json"),
            rel(RUN_DIR / "runtime_handoff_gap_receipt.json"),
        ],
        "reports": [
            rel(REVIEWS_DIR / "frozen_forward_mt5_report.md"),
            rel(REVIEWS_DIR / "regime_attribution_report.md"),
            rel(REVIEWS_DIR / "d_b_attribution_report.md"),
            rel(REVIEWS_DIR / "lot_normalized_report.md"),
            rel(REVIEWS_DIR / "cost_stress_report.md"),
            rel(REVIEWS_DIR / "curve_pocket_report.md"),
            rel(REVIEWS_DIR / "final_forward_decision_report.md"),
        ],
    }
    path = RUN_DIR / "run_manifest.json"
    write_json(path, run_manifest)
    paths.append(path)

    result_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "decision": DECISION,
            "status": status,
            "mt5_forward_run_attempted": "no",
            "forward_data_status": data_receipt["blocking_status"],
            "runtime_handoff_status": gap["blocking_status"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_action": "complete_forward_data_and_frozen_route_signal_handoff_before_mt5_forward",
        }
    ]
    path = RUN_DIR / "result_judgment.csv"
    write_csv(
        path,
        [
            "run_id",
            "stage_id",
            "decision",
            "status",
            "mt5_forward_run_attempted",
            "forward_data_status",
            "runtime_handoff_status",
            "claim_boundary",
            "next_action",
        ],
        result_rows,
    )
    paths.append(path)

    gate_rows = [
        {
            "gate": "data_integrity",
            "status": "failed" if data_receipt["blocking_status"] == "blocked_forward_data_missing" else "completed",
            "evidence": rel(RUN_DIR / "forward_data_integrity_receipt.json"),
            "claim_supported": "Forward Blocked" if data_receipt["blocking_status"] == "blocked_forward_data_missing" else "data_blocker_removed",
            "notes": data_receipt["blocking_status"],
        },
        {
            "gate": "runtime_parity",
            "status": "failed",
            "evidence": rel(RUN_DIR / "runtime_handoff_gap_receipt.json"),
            "claim_supported": "Forward Blocked",
            "notes": "blocked_forward_signal_handoff_missing",
        },
        {
            "gate": "backtest_forensics",
            "status": "not_run",
            "evidence": rel(REVIEWS_DIR / "frozen_forward_mt5_report.md"),
            "claim_supported": "no_forward_pass_or_fail",
            "notes": "MT5 run not allowed without frozen forward input.",
        },
        {
            "gate": "result_judgment",
            "status": "completed",
            "evidence": rel(REVIEWS_DIR / "final_forward_decision_report.md"),
            "claim_supported": "Forward Blocked",
            "notes": status,
        },
    ]
    path = RUN_DIR / "required_gate_coverage_audit.csv"
    write_csv(path, ["gate", "status", "evidence", "claim_supported", "notes"], gate_rows)
    paths.append(path)

    lineage = {
        "receipt_id": "run326A_artifact_lineage_receipt",
        "generated_at_utc": generated_at_utc,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "inputs": {
            "raw_export_summary": rel(RAW_SUMMARY),
            "adapter_package": rel(ADAPTER_DIR),
            "onnx_model": rel(ONNX_MODEL),
            "source_route_signal_dir": rel(SOURCE_FEATURE_DIR),
        },
        "outputs": [
            rel(RUN_DIR / "forward_data_integrity_receipt.json"),
            rel(RUN_DIR / "frozen_contract_receipt.json"),
            rel(RUN_DIR / "runtime_handoff_gap_receipt.json"),
            rel(REVIEWS_DIR / "final_forward_decision_report.md"),
            rel(SELECTED_DIR / "selection_status.md"),
        ],
        "decision": DECISION,
        "status": status,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    path = RUN_DIR / "artifact_lineage_receipt.json"
    write_json(path, lineage)
    paths.append(path)
    return paths


def write_stage_ledger(status: str, data_receipt: dict[str, Any]) -> Path:
    notes = "frozen forward route signal missing; MT5 forward run not performed."
    if data_receipt["blocking_status"] == "blocked_forward_data_missing":
        notes = "US10YR regime data incomplete; " + notes
    else:
        notes = "required regime data coverage repaired; " + notes
    path = REVIEWS_DIR / "stage_run_ledger.csv"
    rows = [
        {
            "row_id": f"{RUN_ID}__forward_blocked",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "view": "frozen_forward_gate",
            "tier_scope": "Tier A used/Tier B fallback/actual routed total not available",
            "scoreboard": "forward_robustness",
            "status": status,
            "judgment": DECISION,
            "evidence_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REVIEWS_DIR / "final_forward_decision_report.md"),
            "notes": notes,
        }
    ]
    write_csv(
        path,
        [
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
        ],
        rows,
    )
    return path


def update_registers(generated_at_utc: str, artifacts: list[Path], status: str, data_receipt: dict[str, Any]) -> None:
    data_note = "data_blocker=blocked_forward_data_missing" if data_receipt["blocking_status"] == "blocked_forward_data_missing" else "data_blocker=resolved"
    guardrail_note = "US10YR regime data incomplete; forward route signal missing"
    if data_receipt["blocking_status"] != "blocked_forward_data_missing":
        guardrail_note = "forward route signal missing; regime data coverage available with timezone boundary"
    upsert_csv(
        ROOT / "docs" / "registers" / "run_registry.csv",
        ["run_id"],
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "runtime_backtest",
            "status": status,
            "judgment": DECISION,
            "path": rel(REVIEWS_DIR / "final_forward_decision_report.md"),
            "notes": f"selected_candidate=cp322A_cp321b_exact_replay_control_surface;mt5_forward_run=blocked;{data_note};handoff_blocker=blocked_forward_signal_handoff_missing;no_operating_claims.",
        },
    )
    upsert_csv(
        ROOT / "docs" / "registers" / "alpha_run_ledger.csv",
        ["ledger_row_id"],
        {
            "ledger_row_id": f"{RUN_ID}__forward_blocked",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "run326A_forward_blocked_total",
            "parent_run_id": "",
            "record_view": "frozen_forward_gate",
            "tier_scope": "Tier A used/Tier B fallback/actual routed total unavailable",
            "kpi_scope": "forward_robustness",
            "scoreboard_lane": "runtime_backtest",
            "status": status,
            "judgment": DECISION,
            "path": rel(REVIEWS_DIR / "final_forward_decision_report.md"),
            "primary_kpi": "not_available_no_forward_mt5_run",
            "guardrail_kpi": guardrail_note,
            "external_verification_status": "data_export_attempted_mt5_not_run_due_blocker",
            "notes": "No Forward Passed/Forward Failed decision; no live readiness/deployment/operating claims.",
        },
    )
    for artifact in artifacts:
        if not artifact.exists() or artifact.is_dir():
            continue
        artifact_id = f"{RUN_ID}__{artifact.stem}".replace("-", "_")
        upsert_csv(
            ROOT / "docs" / "registers" / "artifact_registry.csv",
            ["artifact_id"],
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact.suffix.lstrip(".") or "file",
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": status,
            },
        )


def update_current_truth(status: str, data_receipt: dict[str, Any]) -> None:
    data_clause = (
        "US10YR(미국 10년물) regime data(국면 데이터)가 forward end(전진 종료)에 닿지 않았고, "
        if data_receipt["blocking_status"] == "blocked_forward_data_missing"
        else "US10YR(미국 10년물) regime data(국면 데이터)는 재수집으로 forward end(전진 종료)에 닿았지만, "
    )
    workspace_state = ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text, had_bom = read_text_lossless(workspace_state)
    newline = detect_newline(text)
    lines = text.splitlines()
    output: list[str] = []
    inserted_focus = "Stage326(326단계) run326A(326A 실행) cp322A frozen forward robustness gate" in text
    for line in lines:
        if line.startswith("current_run_id:"):
            output.append(f"current_run_id: {RUN_ID}")
            continue
        if line.startswith("updated_on:"):
            output.append("updated_on: '2026-05-26'")
            continue
        if line.startswith("active_stage:"):
            output.append(f"active_stage: {STAGE_ID}")
            continue
        if "Stage326(326단계) run326A(326A 실행) cp322A frozen forward robustness gate" in line:
            output.append(
                "  Stage326(326단계) run326A(326A 실행) cp322A frozen forward robustness gate(고정 전진 견고성 게이트)는 "
                f"`Forward Blocked`(전진 차단)로 닫혔다. Effect(효과): {data_clause}frozen ONNX(고정 오닉스)가 요구하는 `run322b_route_signal` "
                "forward handoff(전진 인계)가 없어 MT5 forward result(MT5 전진 결과)를 만들지 않는다."
            )
            inserted_focus = True
            continue
        output.append(line)
        if line == "current_focus:" and not inserted_focus:
            output.append("- >-")
            output.append(
                "  Stage326(326단계) run326A(326A 실행) cp322A frozen forward robustness gate(고정 전진 견고성 게이트)는 "
                f"`Forward Blocked`(전진 차단)로 닫혔다. Effect(효과): {data_clause}frozen ONNX(고정 오닉스)가 요구하는 `run322b_route_signal` "
                "forward handoff(전진 인계)가 없어 MT5 forward result(MT5 전진 결과)를 만들지 않는다."
            )
            inserted_focus = True
    write_text_preserving_bom(workspace_state, newline.join(output) + newline, had_bom)

    current_working_state = ROOT / "docs" / "context" / "current_working_state.md"
    existing, had_bom = read_text_lossless(current_working_state)
    newline = detect_newline(existing)
    updated_lines: list[str] = []
    inserted_summary = "run326A_summary(326A 요약)" in existing
    for line in existing.splitlines():
        if line.startswith("- current_packet(현재 작업 묶음):"):
            updated_lines.append(f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
            continue
        if line.startswith("- current_run(현재 실행):"):
            updated_lines.append(f"- current_run(현재 실행): `{RUN_ID}`")
            continue
        if line.startswith("- active_stage(활성 단계):"):
            updated_lines.append(f"- active_stage(활성 단계): `{STAGE_ID}`")
            continue
        if line.startswith("- source_stage(원천 단계):"):
            updated_lines.append("- source_stage(원천 단계): `325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a`")
            continue
        if line.startswith("- target_surface(목표 표면):"):
            updated_lines.append("- target_surface(목표 표면): `cp322A_cp321b_exact_replay_control_surface`")
            continue
        if line.startswith("- status(상태):"):
            updated_lines.append(f"- status(상태): `{status}`")
            if not inserted_summary:
                updated_lines.append(f"- decision(판정): `{DECISION}`(전진 차단)")
                updated_lines.append(
                    "- run326A_summary(326A 요약): cp322A(322A 후보) frozen forward robustness gate(고정 전진 견고성 게이트)는 "
                    f"`Forward Blocked`(전진 차단)로 닫혔다. Effect(효과): {data_clause}frozen ONNX(고정 오닉스)의 `run322b_route_signal` "
                    "forward handoff(전진 인계)가 없어 MT5 forward result(MT5 전진 결과)를 만들지 않는다."
                )
                inserted_summary = True
            continue
        if line.startswith("- run326A_summary(326A 요약):"):
            updated_lines.append(
                "- run326A_summary(326A 요약): cp322A(322A 후보) frozen forward robustness gate(고정 전진 견고성 게이트)는 "
                f"`Forward Blocked`(전진 차단)로 닫혔다. Effect(효과): {data_clause}frozen ONNX(고정 오닉스)의 `run322b_route_signal` "
                "forward handoff(전진 인계)가 없어 MT5 forward result(MT5 전진 결과)를 만들지 않는다."
            )
            inserted_summary = True
            continue
        if line.startswith("- next_action(다음 행동):"):
            updated_lines.append("- next_action(다음 행동): `complete_forward_data_and_frozen_route_signal_handoff_before_mt5_forward`")
            continue
        if line.startswith("- claim_boundary(주장 경계):"):
            updated_lines.append(f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
            continue
        updated_lines.append(line)
    write_text_preserving_bom(current_working_state, newline.join(updated_lines) + newline, had_bom)

    changelog = ROOT / "docs" / "workspace" / "changelog.md"
    changelog_text, had_bom = read_text_lossless(changelog)
    newline = detect_newline(changelog_text)
    entry = f"""

## 2026-05-26 - Stage326 cp322A Frozen Forward Gate(326단계 cp322A 고정 전진 게이트)

- run326A(326A 실행): cp322A(322A 후보) frozen forward robustness gate(고정 전진 견고성 게이트)를 `Forward Blocked`(전진 차단)로 닫았다.
- status(상태): `{status}`
- effect(효과): {data_clause}frozen route signal handoff(고정 경로 신호 인계)가 부족해 MT5 forward result(MT5 전진 결과)를 만들지 않았고, live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위)는 주장하지 않는다.
"""
    if "## 2026-05-26 - Stage326 cp322A Frozen Forward Gate" not in changelog_text:
        entry = lines_with_newline(entry, newline)
        write_text_preserving_bom(changelog, changelog_text.rstrip() + entry, had_bom)
    elif "## 2026-05-26 - Stage326 US10YR Data Retry" not in changelog_text and data_receipt["blocking_status"] != "blocked_forward_data_missing":
        retry_entry = f"""

## 2026-05-26 - Stage326 US10YR Data Retry(326단계 US10YR 데이터 재시도)

- run326A(326A 실행): MT5(메타트레이더5) export(내보내기)를 다시 실행해 US10YR(미국 10년물) M5(5분봉)를 `2026-05-25T19:55:00Z`까지 확보했다.
- status(상태): `{status}`
- effect(효과): `blocked_forward_data_missing`(전진 데이터 누락 차단)은 해소됐고, 남은 차단은 `blocked_forward_signal_handoff_missing`(전진 신호 인계 누락)이다.
"""
        retry_entry = lines_with_newline(retry_entry, newline)
        write_text_preserving_bom(changelog, changelog_text.rstrip() + retry_entry, had_bom)

    decision_doc = ROOT / "docs" / "decisions" / "2026-05-26_stage326_cp322a_frozen_forward_blocked.md"
    write_md(
        decision_doc,
        f"""
# Stage326 cp322A Frozen Forward Blocked(326단계 cp322A 고정 전진 차단)

- decision(판정): `{DECISION}`(전진 차단)
- status(상태): `{status}`
- evidence(근거): `{rel(REVIEWS_DIR / 'final_forward_decision_report.md')}`
- effect(효과): cp322A(322A 후보)를 ONNX research artifact(오닉스 연구 산출물)로 보존하지만 forward pass(전진 통과), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위)를 주장하지 않는다.
""",
    )


def main() -> None:
    generated_at_utc = utc_now()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
    SELECTED_DIR.mkdir(parents=True, exist_ok=True)
    SPEC_DIR.mkdir(parents=True, exist_ok=True)

    data_receipt, data_rows = analyze_forward_data(generated_at_utc)
    contract, gap = audit_frozen_contract(generated_at_utc)
    status = compute_status(data_receipt, gap)
    artifacts: list[Path] = []
    artifacts.extend(write_reports(generated_at_utc, data_receipt, data_rows, contract, gap))
    artifacts.extend(write_receipts(generated_at_utc, data_receipt, contract, gap))
    artifacts.append(write_stage_ledger(status, data_receipt))
    update_registers(generated_at_utc, artifacts, status, data_receipt)
    update_current_truth(status, data_receipt)

    print(json.dumps({"stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "status": status}, ensure_ascii=False))


if __name__ == "__main__":
    main()
