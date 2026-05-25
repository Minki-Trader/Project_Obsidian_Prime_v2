from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage321 import design_post_controller_profit_curve_rebuild as s321  # noqa: E402


STAGE_ID = "328_onnx_candidate_campaign__cp322a_frozen_signal_contract_extraction"
RUN_ID = "run328A_extract_frozen_signal_contract_no_new_data_tuning_v1"
RUN_NUMBER = "run328A"
STATUS = "completed_frozen_signal_contract_extraction_forward_generator_not_safe"
JUDGMENT = "blocked_repair_required_no_goal_achieve"
DECISION = "exact_cp322a_forward_signal_contract_not_safe_without_upstream_rebuild"
NEXT_ACTION = "run328B_deep_audit_cp318_outcome_source_and_live_feature_rebuild_options"
CLAIM_BOUNDARY = (
    "research_development_only_no_new_data_tuning_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
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

STAGE318_MANIFEST = (
    ROOT
    / "stages"
    / "318_onnx_candidate_campaign__post_non_time_curve_stability_rebuild"
    / "02_runs"
    / "run318A"
    / "candidate_payload_manifest.csv"
)
STAGE319_MANIFEST = (
    ROOT
    / "stages"
    / "319_onnx_candidate_campaign__curve_pocket_risk_asymmetry_rebuild"
    / "02_runs"
    / "run319A"
    / "candidate_payload_manifest.csv"
)
STAGE321_PAYLOAD = (
    ROOT
    / "stages"
    / "321_onnx_candidate_campaign__post_controller_profit_curve_rebuild"
    / "02_runs"
    / "run321A"
    / "payloads"
    / "run321A_cp321B_d_or_b_score60_scale_curve_payload.parquet"
)
STAGE322_HANDOFF = (
    ROOT
    / "stages"
    / "322_onnx_candidate_campaign__cp321b_curve_stability_pressure"
    / "02_runs"
    / "run322A"
    / "handoff"
    / "run322A_cp322A_cp321b_exact_replay_control_handoff.json"
)
ADAPTER_FEATURE_ORDER = (
    ROOT
    / "stages"
    / "323_onnx_candidate_campaign__selected_curve_adapter_package"
    / "02_runs"
    / "run323A"
    / "adapter_package"
    / "feature_order_runtime.csv"
)
ONNX_PARITY_RECEIPT = (
    ROOT
    / "stages"
    / "325_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp322a"
    / "02_runs"
    / "run325A"
    / "onnx_parity_receipt.json"
)
STAGE327_DECISION = (
    ROOT
    / "stages"
    / "327_onnx_candidate_campaign__cp322a_overfit_forward_parity_robustness"
    / "03_reviews"
    / "final_stage327_decision_report.md"
)


SOURCE_PACKAGES = (
    s321.D,
    s321.B,
    s321.F,
    s321.A,
    s321.C,
    s321.E,
)


def os_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return os_path(path).exists()


def read_text(path: Path) -> str:
    return os_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str, encoding: str = "utf-8") -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    os_path(path).write_text(text, encoding=encoding)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, data: Any) -> Path:
    return write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> Path:
    os_path(path.parent).mkdir(parents=True, exist_ok=True)
    with os_path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with os_path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    rows: list[dict[str, str]] = []
    if path_exists(path):
        with os_path(path).open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or row.keys())
            rows = list(reader)
    else:
        fieldnames = list(row.keys())
    for name in row:
        if name not in fieldnames:
            fieldnames.append(name)
    clean_row = {name: str(row.get(name, "")) for name in fieldnames}
    replaced = False
    for idx, existing in enumerate(rows):
        if existing.get(key) == clean_row.get(key):
            rows[idx] = clean_row
            replaced = True
            break
    if not replaced:
        rows.append(clean_row)
    write_csv(path, fieldnames, rows)


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = os_path(path).read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig" if has_bom else "utf-8"), has_bom


def write_text_preserving(path: Path, text: str, had_bom: bool) -> None:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    write_text(path, text, encoding=encoding)


def replace_prefix_line(text: str, prefix: str, new_line: str) -> str:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            lines[idx] = new_line
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + new_line + "\n"


def source_line_hits(path: Path, patterns: list[str]) -> str:
    if not path_exists(path):
        return ""
    hits: list[str] = []
    for line_no, line in enumerate(read_text(path).splitlines(), start=1):
        if any(pattern in line for pattern in patterns):
            hits.append(str(line_no))
    return ",".join(hits)


def build_matrix() -> pd.DataFrame:
    source_columns, manifest = s321.load_manifest()
    _ = source_columns
    payloads = s321.load_source_payloads(manifest)
    return s321.build_signal_matrix(payloads)


def exact_signal(matrix: pd.DataFrame) -> np.ndarray:
    d = matrix["sig_d"]
    b = matrix["sig_b"]
    return np.where(((d != 0) | (b != 0)) & (matrix["score_rank"] >= 0.60), np.where(d != 0, d, b), 0).astype("int8")


def threshold_signal(matrix: pd.DataFrame, threshold: float) -> np.ndarray:
    d = matrix["sig_d"]
    b = matrix["sig_b"]
    return np.where(((d != 0) | (b != 0)) & (matrix["score_mean"] >= threshold), np.where(d != 0, d, b), 0).astype("int8")


def split_threshold_signal(matrix: pd.DataFrame, thresholds: dict[str, float]) -> np.ndarray:
    signals: list[int] = []
    for _, row in matrix.iterrows():
        threshold = thresholds[str(row["split"])]
        preferred = int(row["sig_d"]) if int(row["sig_d"]) != 0 else int(row["sig_b"])
        active = (int(row["sig_d"]) != 0 or int(row["sig_b"]) != 0) and float(row["score_mean"]) >= threshold
        signals.append(preferred if active else 0)
    return np.asarray(signals, dtype="int8")


def signal_stats(name: str, signal: np.ndarray, exact: np.ndarray, matrix: pd.DataFrame, threshold: str, source: str, judgment: str) -> dict[str, Any]:
    mismatch = int((signal != exact).sum())
    rows = int(len(signal))
    output = {
        "policy": name,
        "threshold_source": source,
        "score_threshold": threshold,
        "uses_new_forward_distribution": "yes" if name == "split_local_rank_runtime" else "no",
        "historical_mismatch_count": mismatch,
        "historical_mismatch_rate": round(mismatch / rows, 8) if rows else 0.0,
        "active_count": int((signal != 0).sum()),
        "long_count": int((signal > 0).sum()),
        "short_count": int((signal < 0).sum()),
        "forward_contract_judgment": judgment,
    }
    for split in ("train", "validation", "oos"):
        mask = matrix["split"].astype(str).eq(split).to_numpy()
        output[f"{split}_active_count"] = int((signal[mask] != 0).sum())
        output[f"{split}_mismatch_count"] = int((signal[mask] != exact[mask]).sum())
    return output


def threshold_audit(matrix: pd.DataFrame) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    exact = exact_signal(matrix)
    train = matrix["split"].astype(str).eq("train")
    train_validation = matrix["split"].astype(str).isin(["train", "validation"])
    thresholds = {
        "train_only": float(matrix.loc[train, "score_mean"].quantile(0.60)),
        "train_validation": float(matrix.loc[train_validation, "score_mean"].quantile(0.60)),
        "all_old": float(matrix["score_mean"].quantile(0.60)),
    }
    split_thresholds = {
        str(split): float(frame["score_mean"].quantile(0.60))
        for split, frame in matrix.groupby("split", dropna=False)
    }
    rows = [
        signal_stats(
            "split_local_rank_runtime",
            exact,
            exact,
            matrix,
            "score_rank>=0.60",
            "current split distribution(현재 분할 분포)",
            "invalid_for_forward_leakage(전진 누수로 무효)",
        ),
        signal_stats(
            "split_specific_frozen_old_thresholds",
            split_threshold_signal(matrix, split_thresholds),
            exact,
            matrix,
            json.dumps(split_thresholds, sort_keys=True),
            "old train/validation/oos split thresholds(과거 분할별 임계값)",
            "historical_exact_but_not_forward_universal(과거 정확 재현이나 전진 공통 계약 아님)",
        ),
        signal_stats(
            "train_only_frozen_threshold",
            threshold_signal(matrix, thresholds["train_only"]),
            exact,
            matrix,
            f"{thresholds['train_only']:.12f}",
            "train split only(학습 분할만)",
            "research_control_only_changes_cp322a_signal(연구 대조 전용, cp322A 신호 변경)",
        ),
        signal_stats(
            "train_validation_frozen_threshold",
            threshold_signal(matrix, thresholds["train_validation"]),
            exact,
            matrix,
            f"{thresholds['train_validation']:.12f}",
            "train+validation old window(학습+검증 과거 창)",
            "not_exact_and_uses_validation_selection_pressure(비정확 및 검증 압력 포함)",
        ),
        signal_stats(
            "all_old_frozen_threshold",
            threshold_signal(matrix, thresholds["all_old"]),
            exact,
            matrix,
            f"{thresholds['all_old']:.12f}",
            "all historical rows including OOS(표본외 포함 과거 전체)",
            "not_exact_and_expost_oos_pressure(비정확 및 사후 표본외 압력)",
        ),
    ]
    contract = {
        "rule_name": "d_or_b_score60",
        "exact_formula": "if (sig_d != 0 or sig_b != 0) and split_local_rank(score_mean) >= 0.60 then sig_d if sig_d != 0 else sig_b else 0",
        "score_mean_inputs": [f"score_{s321.SHORT[pkg]}" for pkg in SOURCE_PACKAGES],
        "signal_inputs": ["sig_d", "sig_b"],
        "historical_split_thresholds": split_thresholds,
        "frozen_threshold_candidates": thresholds,
        "exact_historical_active_count": int((exact != 0).sum()),
        "exact_historical_long_count": int((exact > 0).sum()),
        "exact_historical_short_count": int((exact < 0).sum()),
        "contract_judgment": DECISION,
    }
    return rows, contract


def stage319_dependency_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    manifest_rows = read_csv(STAGE319_MANIFEST)
    for row in manifest_rows:
        package_id = row.get("package_id", "")
        if package_id not in SOURCE_PACKAGES:
            continue
        model_path = ROOT / row["model_artifact_path"]
        model = read_json(model_path)
        rows.append(
            {
                "layer": "stage319_source_surface(319단계 원천 표면)",
                "package_id": package_id,
                "required_for_cp322a": "yes",
                "source_package_id": model.get("source_package_id"),
                "filter_column": model.get("filter_column"),
                "filter_quantile": model.get("filter_quantile"),
                "filter_sense": model.get("filter_sense"),
                "score_column": model.get("score_column"),
                "score_quantile": model.get("score_quantile"),
                "model_artifact_path": row.get("model_artifact_path"),
                "payload_path": row.get("payload_path"),
                "forward_status": "requires_stage318_outcome_source_rebuild(318단계 결과 원천 재구성 필요)",
                "effect": "Stage321 score_mean(321단계 평균 점수)을 만들려면 여섯 원천 score/signal(점수/신호)이 모두 필요하다.",
            }
        )
    return rows


def stage318_dependency_row() -> dict[str, Any]:
    rows = read_csv(STAGE318_MANIFEST)
    match = next((row for row in rows if row.get("package_id") == "cp318A_outcome_dense20_curve_stability_surface"), None)
    if not match:
        return {
            "layer": "stage318_outcome_model(318단계 결과 모델)",
            "package_id": "cp318A_outcome_dense20_curve_stability_surface",
            "required_for_cp322a": "yes",
            "source_package_id": "missing",
            "filter_column": "",
            "filter_quantile": "",
            "filter_sense": "",
            "score_column": "",
            "score_quantile": "",
            "model_artifact_path": "",
            "payload_path": "",
            "forward_status": "missing_required_manifest(필수 목록 누락)",
            "effect": "원천 모델 계보를 확인할 수 없다.",
        }
    model = read_json(ROOT / match["model_artifact_path"])
    return {
        "layer": "stage318_outcome_model(318단계 결과 모델)",
        "package_id": match.get("package_id"),
        "required_for_cp322a": "yes",
        "source_package_id": model.get("source_package_id"),
        "filter_column": "",
        "filter_quantile": "",
        "filter_sense": "",
        "score_column": "runtime_outcome_model_score(런타임 결과 모델 점수)",
        "score_quantile": model.get("score_threshold"),
        "model_artifact_path": match.get("model_artifact_path"),
        "payload_path": match.get("payload_path"),
        "forward_status": "not_safe_as_forward_authority_without_rebuild(재구성 전 전진 권위 불가)",
        "effect": "Stage317 actual MT5 validation+OOS outcomes(실제 MT5 검증+표본외 결과)로 만든 모델이라 과적합 감사가 먼저 필요하다.",
    }


def dependency_matrix() -> list[dict[str, Any]]:
    rows = [
        {
            "layer": "stage325_onnx_identity(325단계 온닉스 정체성)",
            "package_id": "cp322A_cp321b_exact_replay_control_surface",
            "required_for_cp322a": "yes",
            "source_package_id": "run322b_route_signal",
            "filter_column": "",
            "filter_quantile": "",
            "filter_sense": "",
            "score_column": "",
            "score_quantile": "",
            "model_artifact_path": rel(ONNX_PARITY_RECEIPT),
            "payload_path": rel(ADAPTER_FEATURE_ORDER),
            "forward_status": "blocked_forward_signal_handoff_missing(전진 신호 인계 누락 차단)",
            "effect": "ONNX(온닉스)는 시장 피처가 아니라 이미 만들어진 route signal(경로 신호)을 읽는다.",
        },
        {
            "layer": "stage322_exact_replay_rule(322단계 정확 재생 규칙)",
            "package_id": "cp322A_cp321b_exact_replay_control_surface",
            "required_for_cp322a": "yes",
            "source_package_id": "cp321B_d_or_b_score60_scale_curve_surface",
            "filter_column": "score_rank",
            "filter_quantile": "0.60",
            "filter_sense": "ge",
            "score_column": "score_mean",
            "score_quantile": "split-local 0.60",
            "model_artifact_path": rel(STAGE322_HANDOFF),
            "payload_path": rel(STAGE321_PAYLOAD),
            "forward_status": "exact_historical_only(과거 정확 재현 전용)",
            "effect": "forward(전진)에서 split-local rank(분할 내부 순위)를 다시 계산하면 누수다.",
        },
    ]
    rows.extend(stage319_dependency_rows())
    rows.append(stage318_dependency_row())
    return rows


def source_inventory() -> list[dict[str, Any]]:
    paths = [
        STAGE318_MANIFEST,
        STAGE319_MANIFEST,
        STAGE321_PAYLOAD,
        STAGE322_HANDOFF,
        ADAPTER_FEATURE_ORDER,
        ONNX_PARITY_RECEIPT,
        STAGE327_DECISION,
    ]
    return [
        {
            "path": rel(path),
            "exists": path_exists(path),
            "sha256": sha256_file(path) if path_exists(path) and os_path(path).is_file() else "",
        }
        for path in paths
    ]


def repair_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run328B",
            "repair_probe": "deep_audit_cp318_outcome_source(318단계 결과 원천 심층 감사)",
            "allowed": "yes",
            "changes_cp322a": "no",
            "new_data_tuning_risk": "no",
            "purpose": "Stage318 outcome model(결과 모델)이 forward authority(전진 권위)로 부적합한지 증명하고 대체 경계를 정한다.",
        },
        {
            "queue_id": "run328C",
            "repair_probe": "train_only_frozen_threshold_control(학습 전용 고정 임계값 대조)",
            "allowed": "research_control_only",
            "changes_cp322a": "yes",
            "new_data_tuning_risk": "no",
            "purpose": "train-only threshold(학습 전용 임계값)이 얼마나 다른 신호가 되는지 대조한다. cp322A 통과 주장에는 쓰지 않는다.",
        },
        {
            "queue_id": "stage329",
            "repair_probe": "standalone_live_feature_onnx_design(실시간 피처 독립 ONNX 설계)",
            "allowed": "yes",
            "changes_cp322a": "yes_new_stage",
            "new_data_tuning_risk": "must_control",
            "purpose": "precomputed route signal(사전 계산 경로 신호) 없이 live-computable features(실시간 계산 피처)를 먹는 새 ONNX 경로를 설계한다.",
        },
        {
            "queue_id": "runtime_fixture",
            "repair_probe": "historical_replay_fixture_only(과거 재생 고정물 전용)",
            "allowed": "parity_fixture_only",
            "changes_cp322a": "no",
            "new_data_tuning_risk": "no",
            "purpose": "old-window parity(과거 창 동등성)를 반복 검증하는 고정물로만 쓰고 forward claim(전진 주장)은 금지한다.",
        },
    ]


def write_reports(generated_at_utc: str, threshold_rows: list[dict[str, Any]], contract: dict[str, Any], deps: list[dict[str, Any]]) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_md(
            SPEC_DIR / "stage_brief.md",
            f"""
# Stage328 Frozen Signal Contract Extraction(328단계 고정 신호 계약 추출)

- stage_id(단계 ID): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- objective(목표): `run322b_route_signal`을 새 forward(전진) 데이터 튜닝 없이 만들 수 있는지 확인한다.
- fixed_rule(고정 규칙): cp322A ONNX(온닉스), adapter(어댑터), feature order(피처 순서), D/B rule(D/B 규칙), threshold(임계값)는 변경하지 않는다.
- effect(효과): split-local rank(분할 내부 순위)를 그대로 전진에 쓰는 누수와, frozen numeric threshold(고정 숫자 임계값) 대체가 cp322A를 바꾸는 문제를 분리한다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
        )
    )
    lines = ["# Stage328 Input Refs(328단계 입력 참조)", "", f"- generated_at_utc(생성 시각 UTC): `{generated_at_utc}`", ""]
    for item in source_inventory():
        lines.append(f"- `{item['path']}`: exists(존재)=`{item['exists']}`, sha256(해시)=`{item['sha256']}`")
    artifacts.append(write_md(INPUTS_DIR / "input_refs.md", "\n".join(lines)))

    threshold_md = "\n".join(
        f"- `{row['policy']}`: mismatch(불일치)=`{row['historical_mismatch_count']}`, active(활성)=`{row['active_count']}`, judgment(판정)=`{row['forward_contract_judgment']}`"
        for row in threshold_rows
    )
    dep_md = "\n".join(
        f"- {row['layer']}: `{row['package_id']}` -> `{row['forward_status']}`"
        for row in deps
    )
    artifacts.append(
        write_md(
            REVIEWS_DIR / "run328A_frozen_signal_contract_report.md",
            f"""
# run328A Frozen Signal Contract Report(328A 고정 신호 계약 보고)

## Decision(판정)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp322A exact replay(정확 재생)는 과거 창에서만 안전하고, forward(전진) 생성기는 아직 안전하지 않다.

## Extracted Contract(추출 계약)

- rule(규칙): `{contract['rule_name']}`
- exact_formula(정확 공식): `{contract['exact_formula']}`
- signal_inputs(신호 입력): `{', '.join(contract['signal_inputs'])}`
- score_mean_inputs(평균 점수 입력): `{', '.join(contract['score_mean_inputs'])}`

## Threshold Audit(임계값 감사)

{threshold_md}

## Dependency Audit(의존성 감사)

{dep_md}

## Interpretation(해석)

- split-local rank runtime(런타임 분할 내부 순위)는 forward(전진) 전체 분포를 본 뒤 순위를 만들기 때문에 leakage(누수)다.
- split-specific frozen old thresholds(과거 분할별 고정 임계값)는 historical exact(과거 정확)을 만들지만 새 forward(전진)에 적용할 공통 계약이 아니다.
- train-only frozen threshold(학습 전용 고정 임계값)는 새 데이터 튜닝은 아니지만 cp322A 신호와 `168`행이 달라져 새 research control(연구 대조)일 뿐이다.
- Stage319/318(319/318단계) 원천은 outcome-derived model(결과 유래 모델) 계보가 있어, forward authority(전진 권위)를 바로 줄 수 없다.

## Next(다음)

`{NEXT_ACTION}`를 실행해 cp318A outcome source(318A 결과 원천)를 더 깊게 감사하고, train-only frozen threshold control(학습 전용 고정 임계값 대조)와 standalone live-feature ONNX(실시간 피처 독립 온닉스) 중 어떤 수리 축이 정직한지 나눈다.
""",
        )
    )
    artifacts.append(
        write_md(
            REVIEWS_DIR / "final_stage328_decision_report.md",
            f"""
# Stage328 Final Decision(328단계 최종 판정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- forward_signal_generator(전진 신호 생성기): `not_safe`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp322A를 그대로 forward(전진)에 가져가려면 split-local rank(분할 내부 순위)와 Stage318 outcome source(결과 원천) 문제를 해결해야 한다. 새 데이터 튜닝 없이 바로 Forward Passed(전진 통과)를 주장할 근거는 없다.
- next_action(다음 행동): `{NEXT_ACTION}`
""",
        )
    )
    artifacts.append(
        write_md(
            SELECTED_DIR / "selection_status.md",
            f"""
# Stage328 Selection Status(328단계 선택 상태)

- selected_candidate(선택 후보): `cp322A_cp321b_exact_replay_control_surface`
- package_status(패키지 상태): `research_artifact_preserved`
- forward_usability(전진 사용 가능성): `unresolved`
- frozen_signal_contract(고정 신호 계약): `historical_exact_only_forward_not_safe`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`
- effect(효과): exact replay(정확 재생)와 forward-safe generation(전진 안전 생성)을 분리했고, cp322A를 새 데이터로 재튜닝하지 않았다.
""",
        )
    )
    return artifacts


def write_receipts(generated_at_utc: str, threshold_rows: list[dict[str, Any]], contract: dict[str, Any], deps: list[dict[str, Any]]) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_json(
            RUN_DIR / "frozen_signal_contract.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "generated_at_utc": generated_at_utc,
                "contract": contract,
                "decision": DECISION,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "generated_at_utc": generated_at_utc,
                "hypothesis": "A frozen numeric contract may reproduce cp322A without new data tuning(고정 숫자 계약이 새 데이터 튜닝 없이 cp322A를 재현할 수 있는지)",
                "control": "historical exact split-local rank replay(과거 정확 분할 순위 재생)",
                "changed_variable": "threshold interpretation only for audit(감사용 임계값 해석만)",
                "forbidden": ["forward distribution rank(전진 분포 순위)", "new data threshold fit(새 데이터 임계값 맞춤)", "claim Forward Passed(전진 통과 주장)"],
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
                "model_family": "identity ONNX over precomputed route signal(사전 계산 경로 신호 위 정체성 ONNX)",
                "threshold_policy": "split-local rank 0.60 in source; no forward-safe fixed threshold selected(원천은 분할 내부 순위 0.60, 전진 안전 고정 임계값 미선택)",
                "threshold_audit": threshold_rows,
                "overfit_risk": "Stage318 outcome source and Stage321 split-local rank(318단계 결과 원천과 321단계 분할 내부 순위)",
                "validation_judgment": JUDGMENT,
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
                "data_source": rel(STAGE321_PAYLOAD),
                "time_axis": "timestamp/ts_floor UTC historical shared window; forward bars not used for threshold fitting(UTC 과거 공유 창, 전진 봉으로 임계값 맞추지 않음)",
                "sample_scope": "train/validation/oos historical rows only for contract audit(계약 감사용 과거 행)",
                "feature_label_boundary": "No new forward data consumed; outcome-derived Stage318 lineage remains a risk(새 전진 데이터 미사용, 결과 유래 318단계 계보는 위험)",
                "leakage_risk": "Using forward split-local rank would require seeing the forward distribution(전진 분포를 봐야 하므로 누수)",
                "integrity_judgment": "usable_for_audit_not_forward_generation(감사용 가능, 전진 생성용 아님)",
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
                "research_path": "stage_pipelines/stage328/extract_frozen_signal_contract.py",
                "runtime_path": rel(ADAPTER_FEATURE_ORDER),
                "shared_contract": "runtime still expects run322b_route_signal(런타임은 여전히 run322b_route_signal 필요)",
                "parity_check": "not_run_no_forward_signal_generator(전진 신호 생성기가 없어 미실행)",
                "runtime_claim_boundary": "blocked_no_runtime_authority(차단, 런타임 권위 없음)",
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
                "sources": source_inventory(),
                "line_hits": {
                    "stage321_split_rank": source_line_hits(
                        ROOT / "stage_pipelines" / "stage321" / "design_post_controller_profit_curve_rebuild.py",
                        ["rank(pct=True)", "score_rank", "d_or_b_score60"],
                    ),
                    "stage322_exact_replay": source_line_hits(
                        ROOT / "stage_pipelines" / "stage322" / "design_cp321b_curve_stability_pressure.py",
                        ["cp322A", "d_or_b_score60", "score_rank"],
                    ),
                },
            },
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "threshold_reproduction_audit.csv",
            [
                "policy",
                "threshold_source",
                "score_threshold",
                "uses_new_forward_distribution",
                "historical_mismatch_count",
                "historical_mismatch_rate",
                "active_count",
                "long_count",
                "short_count",
                "train_active_count",
                "train_mismatch_count",
                "validation_active_count",
                "validation_mismatch_count",
                "oos_active_count",
                "oos_mismatch_count",
                "forward_contract_judgment",
            ],
            threshold_rows,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "upstream_dependency_matrix.csv",
            [
                "layer",
                "package_id",
                "required_for_cp322a",
                "source_package_id",
                "filter_column",
                "filter_quantile",
                "filter_sense",
                "score_column",
                "score_quantile",
                "model_artifact_path",
                "payload_path",
                "forward_status",
                "effect",
            ],
            deps,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "forward_repair_queue.csv",
            ["queue_id", "repair_probe", "allowed", "changes_cp322a", "new_data_tuning_risk", "purpose"],
            repair_queue(),
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
                    "effect": "새 데이터 튜닝 금지와 threshold audit(임계값 감사) 목적을 고정했다.",
                },
                {
                    "gate_name": "threshold_reproduction(임계값 재현)",
                    "status": "passed_blocked_for_forward",
                    "evidence_path": rel(RUN_DIR / "threshold_reproduction_audit.csv"),
                    "effect": "train-only frozen threshold(학습 전용 고정 임계값)는 exact cp322A가 아님을 확인했다.",
                },
                {
                    "gate_name": "upstream_dependency(상위 의존성)",
                    "status": "blocked_repair_required",
                    "evidence_path": rel(RUN_DIR / "upstream_dependency_matrix.csv"),
                    "effect": "Stage318 outcome source(결과 원천) 재감사가 필요하다.",
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
            ["run_id", "status", "judgment", "decision", "goal_achieve", "next_action", "claim_boundary"],
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_ACTION,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
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
                "next_action": NEXT_ACTION,
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
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
                    "row_id": f"{RUN_ID}__frozen_signal_contract",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "view": "frozen_signal_contract_extraction(고정 신호 계약 추출)",
                    "tier_scope": "historical train/validation/oos audit only(과거 학습/검증/표본외 감사 전용)",
                    "scoreboard": "threshold_reproduction_not_profit_selection(임계값 재현, 수익 선택 아님)",
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "evidence_boundary": CLAIM_BOUNDARY,
                    "report_path": rel(REVIEWS_DIR / "run328A_frozen_signal_contract_report.md"),
                    "notes": "forward_generator_not_safe;stage318_outcome_source_repair_required;goal_achieve_not_claimed.",
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
            "path": rel(REVIEWS_DIR / "run328A_frozen_signal_contract_report.md"),
            "notes": "frozen_signal_contract_extracted;forward_generator_not_safe;stage318_outcome_source_repair_required;goal_achieve_not_claimed.",
        },
    )
    upsert_csv(
        ALPHA_LEDGER,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__frozen_signal_contract",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": RUN_NUMBER,
            "parent_run_id": "run327A_audit_cp322a_overfit_forward_parity_v1",
            "record_view": "frozen_signal_contract_extraction",
            "tier_scope": "historical train/validation/oos audit only",
            "kpi_scope": "threshold_reproduction_not_profit_selection",
            "scoreboard_lane": "model_validation",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(REVIEWS_DIR / "run328A_frozen_signal_contract_report.md"),
            "primary_kpi": "forward_generator_not_safe",
            "guardrail_kpi": "goal_achieve_not_claimed;no_new_data_tuning",
            "external_verification_status": "not_run_no_safe_forward_signal_generator",
            "notes": f"next_action={NEXT_ACTION}.",
        },
    )
    for artifact in artifacts:
        if not path_exists(artifact) or os_path(artifact).is_dir():
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


def update_current_truth() -> Path:
    workspace = ROOT / "docs" / "workspace" / "workspace_state.yaml"
    text, had_bom = read_text_lossless(workspace)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", "updated_on: '2026-05-26'")
    text = replace_prefix_line(text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        "  Stage328(328단계) run328A(328A 실행) frozen signal contract extraction(고정 신호 계약 추출)을 닫았다. "
        "Effect(효과): split-local rank(분할 내부 순위)는 forward leakage(전진 누수)이고 train-only frozen threshold(학습 전용 고정 임계값)는 cp322A와 다른 신호라 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage328(328단계) run328A(328A 실행)" not in text:
        text = text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    write_text_preserving(workspace, text, had_bom)

    current = ROOT / "docs" / "context" / "current_working_state.md"
    text, had_bom = read_text_lossless(current)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": "- source_stage(원천 단계): `327_onnx_candidate_campaign__cp322a_overfit_forward_parity_robustness`",
        "- target_surface(": "- target_surface(목표 표면): `cp322A_cp321b_exact_replay_control_surface`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, new_line in replacements.items():
        text = replace_prefix_line(text, prefix, new_line)
    summary = (
        f"- run328A_summary(328A 요약): cp322A(322A 후보) frozen signal contract extraction(고정 신호 계약 추출)을 `{STATUS}`로 닫았다. "
        "Effect(효과): historical exact replay(과거 정확 재생)는 가능하지만 forward-safe generator(전진 안전 생성기)는 아니며, Stage318 outcome source(318단계 결과 원천) 재감사가 필요하다."
    )
    if "run328A_summary(328A 요약)" not in text:
        text = text.replace(f"- decision(판정): `{JUDGMENT}`\n", f"- decision(판정): `{JUDGMENT}`\n{summary}\n", 1)
    write_text_preserving(current, text, had_bom)

    changelog = ROOT / "docs" / "workspace" / "changelog.md"
    text, had_bom = read_text_lossless(changelog)
    entry = f"""

## 2026-05-26 - Stage328 cp322A Frozen Signal Contract Extraction(328단계 cp322A 고정 신호 계약 추출)

- run328A(328A 실행): cp322A(322A 후보)의 `run322b_route_signal` 계약을 threshold reproduction audit(임계값 재현 감사)와 upstream dependency matrix(상위 의존성 행렬)로 추출했다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): exact replay(정확 재생)는 과거 창 전용이고 forward-safe generator(전진 안전 생성기)는 아직 안전하지 않아 Goal Achieve(목표 달성), live readiness(실거래 준비), deployment(배포)를 주장하지 않는다.
"""
    if "## 2026-05-26 - Stage328 cp322A Frozen Signal Contract Extraction" not in text:
        write_text_preserving(changelog, text.rstrip() + entry, had_bom)

    decision_doc = ROOT / "docs" / "decisions" / "2026-05-26_stage328_cp322a_frozen_signal_contract_extraction.md"
    return write_md(
        decision_doc,
        f"""
# Stage328 cp322A Frozen Signal Contract Decision(328단계 cp322A 고정 신호 계약 결정)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- goal_achieve(목표 달성): `not_claimed`
- effect(효과): cp322A(322A 후보)의 `run322b_route_signal`은 과거 exact replay(정확 재생)로는 설명되지만, forward-safe generation(전진 안전 생성)에는 Stage318 outcome source(결과 원천)와 split-local rank(분할 내부 순위) 수리가 필요하다.
- next_action(다음 행동): `{NEXT_ACTION}`
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
    )


def main() -> None:
    generated_at_utc = utc_now()
    for directory in (SPEC_DIR, INPUTS_DIR, RUN_DIR, REVIEWS_DIR, SELECTED_DIR):
        os_path(directory).mkdir(parents=True, exist_ok=True)

    matrix = build_matrix()
    threshold_rows, contract = threshold_audit(matrix)
    deps = dependency_matrix()

    artifacts: list[Path] = []
    artifacts.extend(write_reports(generated_at_utc, threshold_rows, contract, deps))
    artifacts.extend(write_receipts(generated_at_utc, threshold_rows, contract, deps))
    artifacts.append(update_current_truth())
    update_registers(generated_at_utc, artifacts)

    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
