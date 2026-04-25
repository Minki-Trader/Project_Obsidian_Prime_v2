from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.features.top3_price_proxy_weights import (  # noqa: E402
    CLOSE_COLUMNS,
    TOP3_SYMBOLS,
    WEIGHT_COLUMNS,
    PriceProxyWeightSpec,
    compute_monthly_price_proxy_weights,
    load_common_close_frame,
)


RUN_ID = "20260425_top3_price_proxy_weights_v1"
STAGE_ID = "04_model_input_readiness__weights_parity_feature_audit"
MATERIALIZER_VERSION = "fpmarkets_v2_stage04_top3_price_proxy_weights_v1"
WEIGHT_TABLE_ID = "top3_monthly_price_proxy_weights_fpmarkets_v2_v1"
WEIGHT_METHOD_ID = "mt5_price_proxy_close_share_v1"
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_WEIGHTS_OUTPUT_PATH = Path("foundation/config/top3_monthly_price_proxy_weights_fpmarkets_v2.csv")
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / "20260425_top3_price_proxy_weights_v1"
WEIGHT_CONTRACT_VERSION = "docs/contracts/top3_price_proxy_weight_contract_fpmarkets_v2.md@2026-04-25"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize MT5 price-proxy monthly top3 weights.")
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--weights-output-path", default=str(DEFAULT_WEIGHTS_OUTPUT_PATH))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--start-month", default="2022-08")
    parser.add_argument("--end-month", default="2026-04")
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _json_ready(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def _summary_payload(
    *,
    raw_root: Path,
    weights_path: Path,
    weights: pd.DataFrame,
    common_close_rows: int,
    spec: PriceProxyWeightSpec,
    weights_sha256: str,
) -> dict[str, object]:
    bootstrap_months = weights.loc[weights["bootstrap_month"].astype(bool), "month"].astype(str).tolist()
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "weight_table_id": WEIGHT_TABLE_ID,
        "weight_method_id": WEIGHT_METHOD_ID,
        "materializer_version": MATERIALIZER_VERSION,
        "weight_contract_version": WEIGHT_CONTRACT_VERSION,
        "raw_root": raw_root.as_posix(),
        "weights_path": weights_path.as_posix(),
        "weights_sha256": weights_sha256,
        "symbols": list(TOP3_SYMBOLS),
        "weight_columns": WEIGHT_COLUMNS,
        "close_columns": CLOSE_COLUMNS,
        "start_month": spec.start_month,
        "end_month": spec.end_month,
        "month_count": int(len(weights)),
        "common_close_rows": int(common_close_rows),
        "bootstrap_months": bootstrap_months,
        "first_source_timestamp": str(weights["source_timestamp"].iloc[0]),
        "last_source_timestamp": str(weights["source_timestamp"].iloc[-1]),
        "weight_sum_min": float(weights["weight_sum"].min()),
        "weight_sum_max": float(weights["weight_sum"].max()),
        "evidence_boundary": (
            "MT5 price-proxy weights only. These weights are reproducible local proxies from MT5 closes; "
            "they are not NDX/QQQ actual index or fund weights."
        ),
        "external_verification_status": "out_of_scope_by_claim",
    }


def render_result_summary(summary: dict[str, object]) -> str:
    bootstrap = ", ".join(summary["bootstrap_months"]) if summary["bootstrap_months"] else "none"
    lines = [
        "# Stage 04 Top3 MT5 Price-Proxy Weights v1",
        "",
        "이 실행(run, 실행)은 로컬 MT5(`MetaTrader 5`, 메타트레이더5) closed-bar prices(닫힌 봉 가격)에서 monthly top3 weights(월별 top3 가중치)를 물질화했다.",
        "",
        "## 핵심 수치(Key Numbers, 핵심 수치)",
        "",
        f"- weight_table_id(가중치 표 ID): `{summary['weight_table_id']}`",
        f"- method(방법): `{summary['weight_method_id']}`",
        f"- months(월 범위): `{summary['start_month']}` through(부터) `{summary['end_month']}`",
        f"- month_count(월 수): `{summary['month_count']}`",
        f"- bootstrap_months(초기값 월): `{bootstrap}`",
        f"- weights_sha256(가중치 SHA256): `{summary['weights_sha256']}`",
        "",
        "## 경계(Boundary, 경계)",
        "",
        "이것은 local MT5 price-proxy evidence(로컬 MT5 가격 대리 근거)다. actual NDX/QQQ weighting(실제 NDX/QQQ 가중치), model training(모델 학습), runtime authority(런타임 권위), operating promotion(운영 승격)을 뜻하지 않는다.",
    ]
    return "\n".join(lines) + "\n"


def materialize_top3_price_proxy_weights(
    *,
    raw_root: Path,
    weights_output_path: Path,
    run_output_root: Path,
    spec: PriceProxyWeightSpec,
) -> dict[str, object]:
    common_close_frame = load_common_close_frame(raw_root)
    weights = compute_monthly_price_proxy_weights(common_close_frame, spec)

    weights_output_path.parent.mkdir(parents=True, exist_ok=True)
    run_output_root.mkdir(parents=True, exist_ok=True)
    weights.to_csv(weights_output_path, index=False)
    weights_sha256 = sha256_file(weights_output_path)

    summary = _summary_payload(
        raw_root=raw_root,
        weights_path=weights_output_path,
        weights=weights,
        common_close_rows=len(common_close_frame),
        spec=spec,
        weights_sha256=weights_sha256,
    )
    summary_path = run_output_root / "summary.json"
    summary_path.write_text(json.dumps(_json_ready(summary), indent=2), encoding="utf-8")

    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "evidence",
        "status": "reviewed",
        "command": "python foundation/pipelines/materialize_top3_price_proxy_weights.py",
        "inputs": [
            raw_root.as_posix(),
            WEIGHT_CONTRACT_VERSION.split("@")[0],
        ],
        "outputs": [
            weights_output_path.as_posix(),
            summary_path.as_posix(),
            (run_output_root / "kpi_record.json").as_posix(),
            (run_output_root / "result_summary.md").as_posix(),
        ],
        "judgment_boundary": summary["evidence_boundary"],
        "external_verification_status": "out_of_scope_by_claim",
    }
    (run_output_root / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")

    kpi_record = {
        "run_id": RUN_ID,
        "scoreboard": "structural_scout",
        "measurement": {
            "weight_table_id": WEIGHT_TABLE_ID,
            "weight_method_id": WEIGHT_METHOD_ID,
            "month_count": summary["month_count"],
            "bootstrap_months": summary["bootstrap_months"],
            "weight_sum_min": summary["weight_sum_min"],
            "weight_sum_max": summary["weight_sum_max"],
            "weights_sha256": weights_sha256,
        },
        "judgment": "positive_price_proxy_weights_materialized",
        "external_verification_status": "out_of_scope_by_claim",
        "evidence_boundary": "reviewed",
    }
    (run_output_root / "kpi_record.json").write_text(json.dumps(_json_ready(kpi_record), indent=2), encoding="utf-8")
    (run_output_root / "result_summary.md").write_text(render_result_summary(summary), encoding="utf-8-sig")

    return {
        "status": "ok",
        "run_id": RUN_ID,
        "weight_table_id": WEIGHT_TABLE_ID,
        "weights_path": weights_output_path.as_posix(),
        "run_output_root": run_output_root.as_posix(),
        "weights_sha256": weights_sha256,
        "month_count": int(len(weights)),
        "bootstrap_months": summary["bootstrap_months"],
    }


def main() -> int:
    args = parse_args()
    payload = materialize_top3_price_proxy_weights(
        raw_root=Path(args.raw_root),
        weights_output_path=Path(args.weights_output_path),
        run_output_root=Path(args.run_output_root),
        spec=PriceProxyWeightSpec(start_month=args.start_month, end_month=args.end_month),
    )
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
