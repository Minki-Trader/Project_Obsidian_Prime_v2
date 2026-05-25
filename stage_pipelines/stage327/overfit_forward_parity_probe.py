from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]

STAGE_ID = "327_onnx_candidate_campaign__cp322a_overfit_forward_parity_robustness"
RUN_ID = "run327A_audit_cp322a_overfit_forward_parity_v1"
RUN_NUMBER = "run327A"
STATUS = "completed_overfit_forward_parity_probe_forward_signal_blocked"
JUDGMENT = "blocked_repair_required_no_goal_achieve"
DECISION = "forward_usability_unresolved_due_signal_contract_and_overfit_risk"
NEXT_STAGE_ID = "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction"
NEXT_ACTION = "run328A_design_frozen_signal_contract_extraction_without_new_data_tuning"
CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

STAGE318_DESIGN = ROOT / "stage_pipelines" / "stage318" / "design_post_non_time_curve_stability_rebuild.py"
STAGE319_REVIEW = ROOT / "stage_pipelines" / "stage319" / "review_curve_pocket_risk_asymmetry_mt5_probe.py"
STAGE321_DESIGN = ROOT / "stage_pipelines" / "stage321" / "design_post_controller_profit_curve_rebuild.py"
STAGE322_REVIEW = ROOT / "stage_pipelines" / "stage322" / "review_cp321b_curve_stability_pressure_mt5_probe.py"
STAGE322_KPI = (
    ROOT
    / "stages"
    / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
    / "02_runs"
    / "run322B"
    / "mt5_kpi_summary.csv"
)
ADAPTER_DIR = (
    ROOT
    / "stages"
    / "323_onnx_candidate_campaign__selected_curve_adapter_package"
    / "02_runs"
    / "run323A"
    / "adapter_package"
)
FEATURE_ORDER_RUNTIME = ADAPTER_DIR / "feature_order_runtime.csv"
ADAPTER_MANIFEST = ADAPTER_DIR / "adapter_package_manifest.json"
ONNX_MODEL = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
    / "models"
    / "cp322a_route_signal_identity.onnx"
)
ONNX_PARITY_RECEIPT = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
    / "onnx_parity_receipt.json"
)
RUNTIME_PARITY_RECEIPT = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
    / "runtime_parity_receipt.json"
)
STAGE326_DATA_RECEIPT = (
    ROOT
    / "stages"
    / "326_forward__cp322a_frozen_forward_gate"
    / "02_runs"
    / "run326A"
    / "forward_data_integrity_receipt.json"
)
STAGE326_DECISION = (
    ROOT
    / "stages"
    / "326_forward__cp322a_frozen_forward_gate"
    / "03_reviews"
    / "final_forward_decision_report.md"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    path.write_text(text, encoding=encoding)


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8-sig")
    return path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    rows: list[dict[str, str]] = []
    fieldnames: list[str]
    if path.exists():
        with path.open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or row.keys())
            rows = list(reader)
    else:
        fieldnames = list(row.keys())
    for name in row:
        if name not in fieldnames:
            fieldnames.append(name)
    row_s = {name: str(row.get(name, "")) for name in fieldnames}
    replaced = False
    for idx, existing in enumerate(rows):
        if existing.get(key) == row_s.get(key):
            rows[idx] = row_s
            replaced = True
            break
    if not replaced:
        rows.append(row_s)
    write_csv(path, fieldnames, rows)


def source_hits(path: Path, patterns: list[str]) -> list[str]:
    hits: list[str] = []
    if not path.exists():
        return hits
    for line_no, line in enumerate(read_text(path).splitlines(), start=1):
        if any(pattern in line for pattern in patterns):
            hits.append(str(line_no))
    return hits


def extract_cp322a_kpi() -> dict[str, Any]:
    wanted: dict[str, dict[str, Any]] = {}
    for row in read_csv(STAGE322_KPI):
        if "run322A_cp322A_cp321b_exact_replay_control" not in row.get("record_view", ""):
            continue
        if row.get("route_role") != "actual_routed_total":
            continue
        split = row.get("split", "")
        metrics = ast.literal_eval(row.get("metrics", "{}"))
        key = "validation" if split == "validation_is" else split
        wanted[key] = {
            "net_profit": float(metrics.get("net_profit", 0.0)),
            "profit_factor": float(metrics.get("profit_factor", 0.0)),
            "trade_count": int(metrics.get("trade_count", 0)),
            "expectancy": float(metrics.get("expectancy", 0.0)),
            "recovery_factor": float(metrics.get("recovery_factor", 0.0)),
            "max_drawdown_percent": float(metrics.get("max_drawdown_percent", 0.0)),
            "feature_ready_count": int(metrics.get("feature_ready_count", 0)),
            "model_fail_count": int(metrics.get("model_fail_count", 0)),
            "no_tier_count": int(metrics.get("no_tier_count", 0)),
            "long_trade_count": int(metrics.get("long_trade_count", 0)),
            "short_trade_count": int(metrics.get("short_trade_count", 0)),
        }
    val = wanted.get("validation", {})
    oos = wanted.get("oos", {})
    ratios = {
        "oos_to_validation_net_ratio": round(oos.get("net_profit", 0.0) / val.get("net_profit", 1.0), 4)
        if val.get("net_profit")
        else "",
        "oos_to_validation_pf_ratio": round(oos.get("profit_factor", 0.0) / val.get("profit_factor", 1.0), 4)
        if val.get("profit_factor")
        else "",
        "oos_to_validation_trade_ratio": round(oos.get("trade_count", 0) / val.get("trade_count", 1), 4)
        if val.get("trade_count")
        else "",
    }
    return {"validation": val, "oos": oos, "ratios": ratios}


def feature_order_rows() -> list[dict[str, str]]:
    return read_csv(FEATURE_ORDER_RUNTIME) if FEATURE_ORDER_RUNTIME.exists() else []


def count_selection_pressure() -> dict[str, Any]:
    rows = read_csv(RUN_REGISTRY)
    selected = []
    attempts_total = 0
    mt5_records_total = 0
    candidate_mentions = 0
    for row in rows:
        stage_id = row.get("stage_id", "")
        match = re.match(r"(\d+)_", stage_id)
        if not match:
            continue
        stage_num = int(match.group(1))
        if not 267 <= stage_num <= 326:
            continue
        selected.append(row)
        notes = row.get("notes", "")
        candidate_mentions += notes.count("candidate") + notes.count("selected_candidate")
        for value in re.findall(r"attempts=(\d+)", notes):
            attempts_total += int(value)
        for value in re.findall(r"mt5_kpi_records=(\d+)", notes):
            mt5_records_total += int(value)
    return {
        "run_registry_rows_stage267_to_326": len(selected),
        "noted_attempts_total": attempts_total,
        "noted_mt5_kpi_records_total": mt5_records_total,
        "candidate_note_mentions": candidate_mentions,
        "interpretation": "high_multiple_testing_pressure(높은 다중 시험 압력)",
    }


def build_static_risk_rows() -> list[dict[str, Any]]:
    return [
        {
            "risk_id": "R1",
            "risk_theme": "identity_onnx_over_precomputed_signal(사전 계산 신호 위 정체성 ONNX)",
            "evidence_path": rel(ONNX_PARITY_RECEIPT),
            "line_numbers": "receipt",
            "observed_pattern": "ONNX input/output parity uses run322b_route_signal as single feature(단일 피처)",
            "risk_level": "high",
            "forward_effect": "새 forward(전진) 구간에서는 route signal(경로 신호)이 없으면 모델이 판단하지 못한다.",
            "required_repair": "live-computable feature(실시간 계산 가능 피처) 모델 또는 frozen signal contract(고정 신호 계약) 필요",
        },
        {
            "risk_id": "R2",
            "risk_theme": "split_local_rank_threshold(분할 내부 순위 임계값)",
            "evidence_path": rel(STAGE321_DESIGN),
            "line_numbers": ",".join(source_hits(STAGE321_DESIGN, ["rank(pct=True)", "score_rank", "candidate_decision_score"])),
            "observed_pattern": "score_rank(점수 순위)를 split(분할) 안에서 계산하고 0.60 rule(규칙)을 쓴다.",
            "risk_level": "high",
            "forward_effect": "forward(전진) 전체 분포를 본 뒤 순위를 만들면 미래 정보 누수(leakage, 누수)가 된다.",
            "required_repair": "historical reference window(과거 기준 창)로 고정된 threshold(임계값)만 허용",
        },
        {
            "risk_id": "R3",
            "risk_theme": "actual_outcome_distillation(실제 결과 증류)",
            "evidence_path": rel(STAGE318_DESIGN),
            "line_numbers": ",".join(source_hits(STAGE318_DESIGN, ["Stage317 actual", "net_profit", "outcome", "positive_trade"])),
            "observed_pattern": "Stage317 actual MT5(실제 MT5) 결과와 net_profit(순수익)을 학습/선별 재료로 쓴다.",
            "risk_level": "high",
            "forward_effect": "성과 좋은 과거 거래 모양을 다시 맞추는 overfit(과적합) 위험이 크다.",
            "required_repair": "outcome-derived feature(결과 유래 피처)를 forward generator(전진 생성기)에서 금지",
        },
        {
            "risk_id": "R4",
            "risk_theme": "actual_mt5_gate_selection_pressure(실제 MT5 관문 선택 압력)",
            "evidence_path": rel(STAGE322_REVIEW),
            "line_numbers": ",".join(source_hits(STAGE322_REVIEW, ["net_profit", "profit_factor", "selected_candidate", "combined"])),
            "observed_pattern": "actual MT5 KPI(실제 MT5 핵심 지표)와 curve gate(곡선 관문)로 selected candidate(선택 후보)를 고른다.",
            "risk_level": "medium_high",
            "forward_effect": "검증/표본외 구간 자체에 selection pressure(선택 압력)가 쌓인다.",
            "required_repair": "새 forward(전진)는 튜닝 금지, 실패도 실패로 기록",
        },
        {
            "risk_id": "R5",
            "risk_theme": "runtime_reproduction_not_forward_authority(런타임 재현은 전진 권위가 아님)",
            "evidence_path": rel(RUNTIME_PARITY_RECEIPT),
            "line_numbers": "receipt",
            "observed_pattern": "runtime parity(런타임 동등성)는 과거 창 재현이고 forward signal(전진 신호)은 없다.",
            "risk_level": "high",
            "forward_effect": "기존 parity pass(동등성 통과)는 최신 forward(전진) 사용 가능성을 증명하지 않는다.",
            "required_repair": "forward handoff(전진 인계)와 MT5 forward reproduction(MT5 전진 재현)을 별도 생성",
        },
    ]


def build_forward_feasibility_rows(data_receipt: dict[str, Any], runtime_features: list[dict[str, str]]) -> list[dict[str, Any]]:
    feature_names = [row.get("feature_name", "") for row in runtime_features]
    required_feature_present = "run322b_route_signal" in feature_names
    data_status = data_receipt.get("blocking_status", "unknown")
    return [
        {
            "item": "forward_market_data(전진 시장 데이터)",
            "status": "available_with_timezone_boundary(시간대 경계 포함 사용 가능)"
            if data_status == "core_data_available"
            else data_status,
            "evidence": rel(STAGE326_DATA_RECEIPT),
            "effect": "US100/VIX/USDX/US10YR forward(전진) 데이터는 핵심 차단이 아니다.",
        },
        {
            "item": "runtime_feature_order(런타임 피처 순서)",
            "status": "single_route_signal_required(단일 경로 신호 필요)"
            if required_feature_present
            else "missing_required_feature(필수 피처 누락)",
            "evidence": rel(FEATURE_ORDER_RUNTIME),
            "effect": "`run322b_route_signal` 없이는 ONNX(온닉스)가 독립 판단을 못 한다.",
        },
        {
            "item": "forward_route_signal_handoff(전진 경로 신호 인계)",
            "status": "blocked_forward_signal_handoff_missing(전진 신호 인계 누락 차단)",
            "evidence": rel(STAGE326_DECISION),
            "effect": "MT5 forward result(MT5 전진 결과)를 아직 만들 수 없다.",
        },
        {
            "item": "naive_signal_generation(순진한 신호 생성)",
            "status": "unsafe(불안전)",
            "evidence": rel(STAGE321_DESIGN),
            "effect": "split-local rank(분할 내부 순위)를 forward(전진)에 그대로 적용하면 leakage(누수)가 된다.",
        },
        {
            "item": "safe_next_probe(안전한 다음 탐침)",
            "status": "stage328_required(328단계 필요)",
            "evidence": NEXT_STAGE_ID,
            "effect": "과거 기준 창에서 얼린 signal contract(신호 계약)만 추출하고 새 데이터 튜닝은 금지한다.",
        },
    ]


def artifact_sources() -> list[dict[str, Any]]:
    paths = [
        STAGE318_DESIGN,
        STAGE319_REVIEW,
        STAGE321_DESIGN,
        STAGE322_REVIEW,
        STAGE322_KPI,
        ADAPTER_MANIFEST,
        FEATURE_ORDER_RUNTIME,
        ONNX_MODEL,
        ONNX_PARITY_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        STAGE326_DATA_RECEIPT,
        STAGE326_DECISION,
    ]
    rows = []
    for path in paths:
        rows.append(
            {
                "path": rel(path),
                "exists": path.exists(),
                "sha256": sha256_file(path) if path.exists() and path.is_file() else "",
            }
        )
    return rows


def write_reports(
    generated_at_utc: str,
    onnx_receipt: dict[str, Any],
    runtime_receipt: dict[str, Any],
    data_receipt: dict[str, Any],
    kpi: dict[str, Any],
    pressure: dict[str, Any],
    risk_rows: list[dict[str, Any]],
    feasibility_rows: list[dict[str, Any]],
) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_md(
            SPEC_DIR / "stage_brief.md",
            f"""
# Stage327 cp322A Overfit/Forward/Parity Probe(327단계 cp322A 과적합/전진/동등성 탐침)

- stage_id(단계 ID): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- objective(목표): 기존 cp322A ONNX(온닉스)가 앞으로도 쓸 수 있는 구조인지 본다.
- fixed_rule(고정 규칙): ONNX(온닉스), adapter(어댑터), feature order(피처 순서), threshold(임계값), D/B surface(D/B 표면), lot/risk logic(랏/위험 로직)은 수정하지 않는다.
- design_effect(설계 효과): 수익 KPI(핵심 지표)를 더 맞추지 않고, signal handoff(신호 인계), overfit(과적합), runtime parity(런타임 동등성)의 막힌 지점을 분리한다.
- stop_condition(중지 조건): forward signal handoff(전진 신호 인계)가 leakage-safe(누수 방지)로 재현되지 않으면 Goal Achieve(목표 달성)는 없다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
        )
    )
    input_lines = [
        "# Stage327 Input Refs(327단계 입력 참조)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at_utc}`",
        "",
    ]
    for item in artifact_sources():
        input_lines.append(
            f"- `{item['path']}`: exists(존재)=`{item['exists']}`, sha256(해시)=`{item['sha256']}`"
        )
    artifacts.append(write_md(INPUTS_DIR / "input_refs.md", "\n".join(input_lines)))

    rows_md = "\n".join(
        f"- {row['risk_id']}: {row['risk_theme']} -> {row['risk_level']} / {row['forward_effect']}"
        for row in risk_rows
    )
    feasibility_md = "\n".join(
        f"- {row['item']}: {row['status']} / Effect(효과): {row['effect']}" for row in feasibility_rows
    )
    val = kpi.get("validation", {})
    oos = kpi.get("oos", {})
    ratios = kpi.get("ratios", {})
    artifacts.append(
        write_md(
            REVIEWS_DIR / "run327A_overfit_forward_parity_probe.md",
            f"""
# run327A Overfit/Forward/Parity Probe(327A 과적합/전진/동등성 탐침)

## Decision(판정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- effect(효과): cp322A는 연구 산출물(research artifact, 연구 산출물)로 보존하지만, forward usability(전진 사용 가능성)과 Goal Achieve(목표 달성)는 주장하지 않는다.

## What Held(유지된 것)

- ONNX parity(온닉스 동등성): `{onnx_receipt.get('passed')}`; mismatch(불일치)=`{onnx_receipt.get('decision_parity', {}).get('decision_mismatch_count')}`
- Runtime parity(런타임 동등성): `{runtime_receipt.get('passed')}`; compared rows(비교 행)=`{runtime_receipt.get('parity_check', {}).get('compared_rows')}`
- Forward data(전진 데이터): `{data_receipt.get('blocking_status')}`

## What Did Not Hold(유지되지 않은 것)

- ONNX model(온닉스 모델)은 live-computable feature model(실시간 계산 피처 모델)이 아니라 `run322b_route_signal` identity surface(정체성 표면)다.
- Stage326(326단계) 기준 최신 forward(전진) 구간에는 `run322b_route_signal` handoff(인계)가 없다.
- naive forward signal generation(순진한 전진 신호 생성)은 split rank(분할 순위)와 outcome distillation(결과 증류) 위험 때문에 금지한다.

## KPI Context(핵심 지표 문맥)

- validation net/PF/trades(검증 순수익/수익 팩터/거래수): `{val.get('net_profit')}` / `{val.get('profit_factor')}` / `{val.get('trade_count')}`
- OOS net/PF/trades(표본외 순수익/수익 팩터/거래수): `{oos.get('net_profit')}` / `{oos.get('profit_factor')}` / `{oos.get('trade_count')}`
- OOS/validation ratio(OOS/검증 비율): net=`{ratios.get('oos_to_validation_net_ratio')}`, PF=`{ratios.get('oos_to_validation_pf_ratio')}`, trades=`{ratios.get('oos_to_validation_trade_ratio')}`
- effect(효과): 숫자는 참고 문맥일 뿐이고, 이번 판정은 forward handoff(전진 인계)와 overfit risk(과적합 위험)를 우선한다.

## Risk Matrix(위험 행렬)

{rows_md}

## Forward Feasibility(전진 가능성)

{feasibility_md}

## Selection Pressure(선택 압력)

- run_registry rows(실행 등록부 행): `{pressure['run_registry_rows_stage267_to_326']}`
- noted attempts(기록된 시도): `{pressure['noted_attempts_total']}`
- noted MT5 KPI records(기록된 MT5 핵심 지표): `{pressure['noted_mt5_kpi_records_total']}`
- interpretation(해석): `{pressure['interpretation']}`

## Next(다음)

Stage328(328단계)는 frozen signal contract extraction(고정 신호 계약 추출)을 설계한다. Effect(효과): 새 forward(전진) 데이터로 threshold(임계값)를 맞추지 않고, 과거 기준으로 얼린 규칙만 전진에 적용 가능한지 검증한다.
""",
        )
    )
    artifacts.append(
        write_md(
            REVIEWS_DIR / "final_stage327_decision_report.md",
            f"""
# Stage327 Final Decision(327단계 최종 판정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- goal_achieve(목표 달성): `not_claimed`
- selected_candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface` preserved as research artifact(연구 산출물로 보존)
- effect(효과): cp322A의 old-window parity(과거 창 동등성)는 유지됐지만 forward signal handoff(전진 신호 인계)와 overfit leakage risk(과적합 누수 위험)가 해결되지 않아 운영 주장은 금지한다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
        )
    )
    artifacts.append(
        write_md(
            SELECTED_DIR / "selection_status.md",
            f"""
# Stage327 Selection Status(327단계 선택 상태)

- selected_candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface`
- package_status(패키지 상태): `research_artifact_preserved`
- forward_usability(전진 사용 가능성): `unresolved`
- overfit_parity_status(과적합/동등성 상태): `{JUDGMENT}`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): 후보를 버리거나 튜닝하지 않고, 다음 stage(단계)에서 signal contract(신호 계약)를 누수 없이 재현 가능한지 먼저 검증한다.
""",
        )
    )
    return artifacts


def write_receipts(
    generated_at_utc: str,
    onnx_receipt: dict[str, Any],
    runtime_receipt: dict[str, Any],
    data_receipt: dict[str, Any],
    kpi: dict[str, Any],
    pressure: dict[str, Any],
    risk_rows: list[dict[str, Any]],
    feasibility_rows: list[dict[str, Any]],
) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "generated_at_utc": generated_at_utc,
                "objective": "cp322A overfit/forward/parity robustness audit(과적합/전진/동등성 강건성 감사)",
                "frozen_items": [
                    "onnx_model(온닉스 모델)",
                    "adapter_package(어댑터 패키지)",
                    "feature_order(피처 순서)",
                    "decision_thresholds(판단 임계값)",
                    "risk_lot_logic(위험/랏 로직)",
                ],
                "success_condition": "leakage-safe forward signal handoff or standalone live-computable ONNX path identified(누수 방지 전진 신호 인계 또는 독립 ONNX 경로 식별)",
                "forbidden": ["new_data_tuning(새 데이터 튜닝)", "threshold_refit(임계값 재맞춤)", "candidate_reselection(후보 재선택)"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "generated_at_utc": generated_at_utc,
                "judgment": JUDGMENT,
                "onnx_parity_passed": bool(onnx_receipt.get("passed")),
                "onnx_model_sha256": onnx_receipt.get("onnx_model_sha256"),
                "kpi_context": kpi,
                "overfit_risks": risk_rows,
                "effect": "old-window parity is not forward usability(과거 창 동등성은 전진 사용 가능성이 아님)",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "generated_at_utc": generated_at_utc,
                "source_receipt": rel(RUNTIME_PARITY_RECEIPT),
                "source_passed": bool(runtime_receipt.get("passed")),
                "feature_order": runtime_receipt.get("shared_contract", {}).get("feature_order"),
                "forward_runtime_status": "blocked_forward_signal_handoff_missing(전진 신호 인계 누락 차단)",
                "effect": "runtime reproduction(런타임 재현)은 통과했지만 forward runtime authority(전진 런타임 권위)는 없다.",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "generated_at_utc": generated_at_utc,
                "source_receipt": rel(STAGE326_DATA_RECEIPT),
                "forward_data_status": data_receipt.get("blocking_status"),
                "timezone_status": "broker_timezone_boundary_unresolved_but_data_blocker_cleared(브로커 시간대 경계 미해결이나 데이터 차단 해소)",
                "forward_signal_status": "missing(누락)",
                "effect": "market data(시장 데이터)와 signal handoff(신호 인계)를 분리해 차단 원인을 좁혔다.",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "generated_at_utc": generated_at_utc,
                "sources": artifact_sources(),
                "effect": "input hash(입력 해시)를 고정해 다음 stage(단계)가 같은 근거에서 출발한다.",
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_stage_id": NEXT_STAGE_ID,
                "next_action": NEXT_ACTION,
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "overfit_risk_matrix.csv",
            [
                "risk_id",
                "risk_theme",
                "evidence_path",
                "line_numbers",
                "observed_pattern",
                "risk_level",
                "forward_effect",
                "required_repair",
            ],
            risk_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "forward_signal_handoff_feasibility.csv",
            ["item", "status", "evidence", "effect"],
            feasibility_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "selection_pressure_audit.csv",
            ["metric", "value", "effect"],
            [
                {
                    "metric": key,
                    "value": value,
                    "effect": "selection pressure(선택 압력)과 multiple testing(다중 시험)을 보수적으로 본다.",
                }
                for key, value in pressure.items()
            ],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate_name", "status", "evidence_path", "effect"],
            [
                {
                    "gate_name": "experiment_design(실험 설계)",
                    "status": "passed",
                    "evidence_path": rel(RUN_DIR / "experiment_design_receipt.json"),
                    "effect": "수정 금지와 판단 경계를 고정했다.",
                },
                {
                    "gate_name": "model_validation(모델 검증)",
                    "status": "blocked_repair_required",
                    "evidence_path": rel(RUN_DIR / "model_validation_receipt.json"),
                    "effect": "ONNX(온닉스)가 precomputed route signal(사전 계산 경로 신호)에 의존함을 확인했다.",
                },
                {
                    "gate_name": "runtime_parity(런타임 동등성)",
                    "status": "old_window_pass_forward_blocked",
                    "evidence_path": rel(RUN_DIR / "runtime_parity_receipt.json"),
                    "effect": "과거 재현과 전진 권위를 분리했다.",
                },
                {
                    "gate_name": "data_integrity(데이터 무결성)",
                    "status": "data_available_signal_missing",
                    "evidence_path": rel(RUN_DIR / "data_integrity_receipt.json"),
                    "effect": "market data(시장 데이터) 문제보다 handoff(인계) 문제가 남았다.",
                },
                {
                    "gate_name": "result_judgment(결과 판정)",
                    "status": "passed_no_goal_achieve",
                    "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
                    "effect": "Goal Achieve(목표 달성)를 주장하지 않는다.",
                },
            ],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "selected_candidate",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "selected_candidate": "cp322A_cp321b_exact_replay_control_surface",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_ACTION,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_csv(
            REVIEWS_DIR / "stage_run_ledger.csv",
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
            [
                {
                    "row_id": f"{RUN_ID}__overfit_forward_parity_probe",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "view": "overfit_forward_parity_probe(과적합 전진 동등성 탐침)",
                    "tier_scope": "Tier A/B source evidence plus forward blocked handoff(티어 A/B 원천 근거와 전진 인계 차단)",
                    "scoreboard": "not_profit_selection(수익 선택 아님)",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "evidence_boundary": CLAIM_BOUNDARY,
                    "report_path": rel(REVIEWS_DIR / "run327A_overfit_forward_parity_probe.md"),
                    "notes": "forward_signal_missing;overfit_risk_high;goal_achieve_not_claimed.",
                }
            ],
        )
    )
    return artifacts


def update_registers(generated_at_utc: str, artifacts: list[Path]) -> None:
    upsert_csv(
        RUN_REGISTRY,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run327A_overfit_forward_parity_probe.md"),
            "notes": "cp322A preserved;forward_signal_missing;identity_onnx_over_route_signal;goal_achieve_not_claimed;next_action=run328A.",
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__overfit_forward_parity_probe",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": "run326A_cp322a_frozen_forward_robustness_gate_v1",
            "record_view": "overfit_forward_parity_probe",
            "tier_scope": "Tier A/B source evidence plus forward blocked handoff",
            "kpi_scope": "overfit_forward_parity_not_profit_selection",
            "scoreboard_lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run327A_overfit_forward_parity_probe.md"),
            "primary_kpi": "forward_signal_missing",
            "guardrail_kpi": "goal_achieve_not_claimed;no_live_readiness;no_deployment",
            "external_verification_status": "stage326_forward_data_checked_mt5_forward_not_run_due_signal_blocker",
            "notes": f"next_action={NEXT_ACTION}.",
        },
    )
    for artifact in artifacts:
        if not artifact.exists() or artifact.is_dir():
            continue
        upsert_csv(
            ARTIFACT_REGISTRY,
            "artifact_id",
            {
                "artifact_id": f"{RUN_ID}__{artifact.stem}".replace("-", "_"),
                "artifact_type": artifact.suffix.lstrip(".") or "file",
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": STATUS,
            },
        )


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def update_current_truth() -> Path:
    workspace = ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text, had_bom = read_text_lossless(workspace)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", "updated_on: '2026-05-26'")
    text = replace_prefix_line(text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        "  Stage327(327단계) run327A(327A 실행) cp322A overfit/forward/parity probe(과적합/전진/동등성 탐침)를 닫았다. "
        "Effect(효과): ONNX parity(온닉스 동등성)는 과거 창에서 유지됐지만 `run322b_route_signal` forward handoff(전진 인계)가 없고 split rank/outcome pressure(분할 순위/결과 압력) 위험이 커서 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage327(327단계) run327A(327A 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_preserving(workspace, text, had_bom)

    current = ROOT / "docs" / "context" / "current_working_state.md"
    text, had_bom = read_text_lossless(current)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": "- source_stage(원천 단계): `325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a`",
        "- target_surface(": "- target_surface(목표 표면): `cp322A_cp321b_exact_replay_control_surface`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, new_line in replacements.items():
        text = replace_prefix_line(text, prefix, new_line)
    summary = (
        f"- run327A_summary(327A 요약): cp322A(322A 후보) overfit/forward/parity probe(과적합/전진/동등성 탐침)를 `{STATUS}`로 닫았다. "
        "Effect(효과): old-window parity(과거 창 동등성)는 유지됐지만 identity ONNX(정체성 온닉스)가 `run322b_route_signal`을 요구하고, forward signal handoff(전진 신호 인계)가 없어 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run327A_summary(327A 요약)" not in text:
        text = text.replace(f"- decision(판정): `{JUDGMENT}`\n", f"- decision(판정): `{JUDGMENT}`\n{summary}\n", 1)
    write_text_preserving(current, text, had_bom)

    changelog = ROOT / "docs" / "workspace" / "changelog.md"
    text, had_bom = read_text_lossless(changelog)
    entry = f"""

## 2026-05-26 - Stage327 cp322A Overfit/Forward/Parity Probe(327단계 cp322A 과적합/전진/동등성 탐침)

- run327A(327A 실행): cp322A(322A 후보)의 ONNX parity(온닉스 동등성), runtime parity(런타임 동등성), forward handoff(전진 인계), overfit risk(과적합 위험)를 함께 감사했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): forward signal handoff(전진 신호 인계)와 leakage-safe signal contract(누수 방지 신호 계약)가 해결되지 않아 Goal Achieve(목표 달성), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격)을 주장하지 않는다.
"""
    if "## 2026-05-26 - Stage327 cp322A Overfit/Forward/Parity Probe" not in text:
        write_text_preserving(changelog, text.rstrip() + entry + "\n", had_bom)

    decision_doc = ROOT / "docs" / "decisions" / "2026-05-26_stage327_cp322a_overfit_forward_parity_probe.md"
    return write_md(
        decision_doc,
        f"""
# Stage327 cp322A Overfit/Forward/Parity Decision(327단계 cp322A 과적합/전진/동등성 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): cp322A(322A 후보)는 research artifact(연구 산출물)로 보존하지만, forward usability(전진 사용 가능성)과 Goal Achieve(목표 달성)는 보류한다.
- next_action(다음 행동): `{NEXT_ACTION}`
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
    )


def main() -> None:
    generated_at_utc = utc_now()
    for directory in (SPEC_DIR, INPUTS_DIR, RUN_DIR, REVIEWS_DIR, SELECTED_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    onnx_receipt = read_json(ONNX_PARITY_RECEIPT)
    runtime_receipt = read_json(RUNTIME_PARITY_RECEIPT)
    data_receipt = read_json(STAGE326_DATA_RECEIPT)
    runtime_features = feature_order_rows()
    kpi = extract_cp322a_kpi()
    pressure = count_selection_pressure()
    risk_rows = build_static_risk_rows()
    feasibility_rows = build_forward_feasibility_rows(data_receipt, runtime_features)

    artifacts: list[Path] = []
    artifacts.extend(
        write_reports(generated_at_utc, onnx_receipt, runtime_receipt, data_receipt, kpi, pressure, risk_rows, feasibility_rows)
    )
    artifacts.extend(
        write_receipts(generated_at_utc, onnx_receipt, runtime_receipt, data_receipt, kpi, pressure, risk_rows, feasibility_rows)
    )
    artifacts.append(update_current_truth())
    update_registers(generated_at_utc, artifacts)

    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
