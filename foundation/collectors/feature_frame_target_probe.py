from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.pipelines.materialize_fpmarkets_v2_dataset import (  # noqa: E402
    PRACTICAL_MODELING_START_UTC,
    build_feature_frame,
)


RUN_ID = "20260424_feature_frame_target_probe"
SELECTED_TARGET_ID = "practical_start_full_cash_day_valid_rows_only"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Probe the first clean feature-frame target for Stage 01."
    )
    parser.add_argument(
        "--raw-root",
        default="data/raw/mt5_bars/m5",
        help="Repo-relative raw M5 root.",
    )
    parser.add_argument(
        "--output-dir",
        default=f"stages/01_data_foundation__raw_m5_inventory/02_runs/{RUN_ID}",
        help="Repo-relative output directory for the probe artifacts.",
    )
    return parser.parse_args()


def _iso(value: pd.Timestamp | None) -> str | None:
    if value is None or pd.isna(value):
        return None
    return pd.Timestamp(value).isoformat()


def _candidate_payload(
    *,
    target_id: str,
    label: str,
    start_utc: pd.Timestamp,
    day_scope: str,
    session_scope: str,
    row_scope: str,
    rows: int,
    ny_day_count: int,
) -> dict[str, object]:
    return {
        "target_id": target_id,
        "label": label,
        "start_utc": start_utc.isoformat(),
        "day_scope": day_scope,
        "session_scope": session_scope,
        "row_scope": row_scope,
        "rows": rows,
        "ny_day_count": ny_day_count,
    }


def analyze_feature_frame_target(raw_root: Path) -> dict[str, object]:
    frame, counts = build_feature_frame(raw_root)
    frame = frame.copy()
    frame["date_ny"] = frame["timestamp_ny"].dt.strftime("%Y-%m-%d")
    frame["cash_open"] = frame["is_us_cash_open"].fillna(0).astype(bool)
    frame["valid_int"] = frame["valid_row"].astype(int)
    frame["is_practical"] = frame["timestamp"] >= PRACTICAL_MODELING_START_UTC

    cash = frame.loc[frame["cash_open"]].copy()
    per_day = cash.groupby("date_ny").agg(
        cash_rows=("cash_open", "size"),
        valid_rows=("valid_int", "sum"),
        first_timestamp=("timestamp", "min"),
        last_timestamp=("timestamp", "max"),
    )
    per_day["is_full_cash_day"] = per_day["cash_rows"] == 78
    per_day["valid_ratio"] = per_day["valid_rows"] / per_day["cash_rows"]

    cash = cash.merge(
        per_day[["is_full_cash_day", "cash_rows", "valid_ratio"]],
        left_on="date_ny",
        right_index=True,
        how="left",
    )

    full_window_valid = frame.loc[frame["valid_row"]]
    practical_valid = frame.loc[frame["is_practical"] & frame["valid_row"]]
    practical_cash_valid = cash.loc[cash["is_practical"] & cash["valid_row"]]
    practical_full_cash_valid = cash.loc[
        cash["is_practical"] & cash["is_full_cash_day"] & cash["valid_row"]
    ]

    candidates = [
        _candidate_payload(
            target_id="full_window_valid_rows_only",
            label="full shared window valid rows only",
            start_utc=pd.Timestamp(frame["timestamp"].min()),
            day_scope="all_days",
            session_scope="all_rows",
            row_scope="valid_row_only",
            rows=int(len(full_window_valid)),
            ny_day_count=int(full_window_valid["date_ny"].nunique()),
        ),
        _candidate_payload(
            target_id="practical_start_valid_rows_only",
            label="practical start valid rows only",
            start_utc=PRACTICAL_MODELING_START_UTC,
            day_scope="all_days",
            session_scope="all_rows",
            row_scope="valid_row_only",
            rows=int(len(practical_valid)),
            ny_day_count=int(practical_valid["date_ny"].nunique()),
        ),
        _candidate_payload(
            target_id="practical_start_cash_open_valid_rows_only",
            label="practical start cash-open valid rows only",
            start_utc=PRACTICAL_MODELING_START_UTC,
            day_scope="cash_open_rows",
            session_scope="cash_open_rows_only",
            row_scope="valid_row_only",
            rows=int(len(practical_cash_valid)),
            ny_day_count=int(practical_cash_valid["date_ny"].nunique()),
        ),
        _candidate_payload(
            target_id=SELECTED_TARGET_ID,
            label="practical start full-cash-session-day valid rows only",
            start_utc=PRACTICAL_MODELING_START_UTC,
            day_scope="full_cash_session_days_only",
            session_scope="cash_open_rows_only",
            row_scope="valid_row_only",
            rows=int(len(practical_full_cash_valid)),
            ny_day_count=int(practical_full_cash_valid["date_ny"].nunique()),
        ),
    ]

    selected_target = next(
        candidate for candidate in candidates if candidate["target_id"] == SELECTED_TARGET_ID
    ).copy()
    selected_target.update(
        {
            "practical_modeling_start": PRACTICAL_MODELING_START_UTC.isoformat(),
            "first_valid_timestamp": _iso(practical_full_cash_valid["timestamp"].min()),
            "last_valid_timestamp": _iso(practical_full_cash_valid["timestamp"].max()),
            "excluded_partial_cash_days": int((~per_day["is_full_cash_day"]).sum()),
            "excluded_partial_day_valid_rows": int(
                len(practical_cash_valid) - len(practical_full_cash_valid)
            ),
            "full_cash_day_count": int(
                cash.loc[cash["is_practical"] & cash["is_full_cash_day"], "date_ny"].nunique()
            ),
        }
    )

    worst_partial_days = per_day.loc[~per_day["is_full_cash_day"]].sort_values(
        ["valid_ratio", "cash_rows", "first_timestamp"]
    )
    worst_partial_payload = []
    for date_ny, row in worst_partial_days.head(20).iterrows():
        worst_partial_payload.append(
            {
                "date_ny": date_ny,
                "cash_rows": int(row["cash_rows"]),
                "valid_rows": int(row["valid_rows"]),
                "valid_ratio": float(row["valid_ratio"]),
                "first_timestamp": _iso(row["first_timestamp"]),
                "last_timestamp": _iso(row["last_timestamp"]),
            }
        )

    payload = {
        "probe_version": "FPMARKETS_V2_STAGE01_FEATURE_FRAME_TARGET_PROBE_V1",
        "run_id": RUN_ID,
        "measurement_scope": "feature-frame target evidence only",
        "management_state": "run artifacts tracked under Stage 01 02_runs",
        "judgment_class": "positive",
        "scoreboard": "diagnostic_special",
        "parity_level": "P1_dataset_feature_aligned",
        "wfo_status": "not_applicable",
        "registry_update_required": "yes",
        "negative_memory_required": "no",
        "hard_gate_applicable": "no",
        "evidence_boundary": "reviewed",
        "external_verification_status": "not_applicable",
        "raw_rows": int(counts["raw_rows"]),
        "valid_rows": int(counts["valid_rows"]),
        "invalid_rows": int(counts["invalid_rows"]),
        "practical_modeling_start": PRACTICAL_MODELING_START_UTC.isoformat(),
        "cash_open_rows_total": int(len(cash)),
        "cash_open_valid_rows_total": int(cash["valid_int"].sum()),
        "cash_open_valid_ratio_total": float(cash["valid_int"].mean()),
        "full_cash_days_total": int(per_day["is_full_cash_day"].sum()),
        "partial_cash_days_total": int((~per_day["is_full_cash_day"]).sum()),
        "selected_target": selected_target,
        "candidate_targets": candidates,
        "worst_partial_days": worst_partial_payload,
        "rationale": [
            "keep the existing practical modeling start instead of reopening the earlier warmup period",
            "use parser-level valid_row rows only so the first target matches the current contract surface",
            "exclude partial cash-session days so the first freeze keeps a uniform NY core session day boundary",
            "do not mark broader valid-row scopes dead; leave them as later candidates after the first clean freeze exists",
        ],
    }
    return payload


def render_markdown(payload: dict[str, object]) -> str:
    selected = payload["selected_target"]
    candidates = payload["candidate_targets"]
    partial_days = payload["worst_partial_days"]
    lines = [
        "# Feature Frame Target Probe Review(피처 프레임 목표 탐침 검토)",
        "",
        "## 판정(Judgment, 판정)",
        "",
        f"`{payload['run_id']}` 실행(run, 실행)은 `positive(긍정)`로 본다.",
        "",
        "쉽게 말하면 첫 clean feature frame target(첫 깨끗한 피처 프레임 목표)은 "
        "practical modeling start(실용 모델링 시작) 이후 `valid_row(유효행)`만 쓰고, "
        "partial cash session(부분 정규장) 일자를 빼는 범위가 가장 깔끔하다.",
        "",
        "## 선택된 목표(Selected Target, 선택된 목표)",
        "",
        f"- target_id(목표 ID): `{selected['target_id']}`",
        f"- start_utc(시작 UTC): `{selected['start_utc']}`",
        f"- row_scope(행 범위): `{selected['row_scope']}`",
        f"- session_scope(세션 범위): `{selected['session_scope']}`",
        f"- day_scope(일 범위): `{selected['day_scope']}`",
        f"- valid rows(유효행 수): `{selected['rows']}`",
        f"- NY days(뉴욕 일수): `{selected['ny_day_count']}`",
        f"- excluded partial cash days(제외된 부분 정규장 일수): `{selected['excluded_partial_cash_days']}`",
        f"- excluded partial-day valid rows(제외된 부분 정규장 유효행 수): `{selected['excluded_partial_day_valid_rows']}`",
        f"- first valid timestamp(첫 유효 타임스탬프): `{selected['first_valid_timestamp']}`",
        f"- last valid timestamp(마지막 유효 타임스탬프): `{selected['last_valid_timestamp']}`",
        "",
        "## 후보 비교(Candidate Comparison, 후보 비교)",
        "",
        "| target_id | rows | ny_day_count | session_scope | day_scope |",
        "|---|---:|---:|---|---|",
    ]
    for candidate in candidates:
        lines.append(
            f"| `{candidate['target_id']}` | `{candidate['rows']}` | `{candidate['ny_day_count']}` | `{candidate['session_scope']}` | `{candidate['day_scope']}` |"
        )

    lines.extend(
        [
            "",
            "## 이유(Why, 이유)",
            "",
            f"- cash-open valid ratio(정규장 유효 비율): `{payload['cash_open_valid_ratio_total']:.6f}`",
            f"- full cash days(완전 정규장 일수): `{payload['full_cash_days_total']}`",
            f"- partial cash days(부분 정규장 일수): `{payload['partial_cash_days_total']}`",
            "- partial cash session(부분 정규장) 일자는 holiday(휴일) 전후나 early close(조기 종료)처럼 "
            "행 형태(row shape, 행 형태)가 흔들리는 경우가 많다.",
            "- 첫 freeze(첫 동결)를 가능한 한 균일한 NY core session day boundary(뉴욕 핵심 정규장 일 경계)로 묶는 편이 "
            "다음 단계의 artifact identity(산출물 정체성)를 더 단순하게 만든다.",
            "",
            "## 부분 정규장 예시(Worst Partial-Day Examples, 부분 정규장 예시)",
            "",
            "| date_ny | cash_rows | valid_rows | valid_ratio |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in partial_days[:10]:
        lines.append(
            f"| `{row['date_ny']}` | `{row['cash_rows']}` | `{row['valid_rows']}` | `{row['valid_ratio']:.6f}` |"
        )

    lines.extend(
        [
            "",
            "## 효과(Effect, 효과)",
            "",
            "Stage 01(1단계)은 이제 첫 feature frame target(피처 프레임 목표)을 분명하게 갖고 있다.",
            "다음 단계(next stage, 다음 단계)는 이 목표를 실제 shared freeze(공유 동결 산출물)로 물질화하는 일이다.",
            "",
            "## 경계(Boundary, 경계)",
            "",
            "이 검토(review, 검토)는 첫 clean target(깨끗한 목표)을 고르는 근거다.",
            "더 넓은 valid-row scope(유효행 범위)가 무효라는 뜻은 아니다. "
            "model readiness(모델 준비), runtime authority(런타임 권위), "
            "operating promotion(운영 승격)을 주장하지도 않는다.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(output_dir: Path, payload: dict[str, object]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "feature_frame_target_probe.json"
    md_path = output_dir / "feature_frame_target_probe.md"
    manifest_path = output_dir / "run_manifest.json"

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8-sig")
    manifest_path.write_text(
        json.dumps(
            {
                "run_id": RUN_ID,
                "lane": "evidence",
                "stage_id": "01_data_foundation__raw_m5_inventory",
                "command": (
                    "python foundation/collectors/feature_frame_target_probe.py "
                    "--raw-root data/raw/mt5_bars/m5 "
                    "--output-dir stages/01_data_foundation__raw_m5_inventory/02_runs/"
                    f"{RUN_ID}"
                ),
                "outputs": [
                    str(json_path.as_posix()),
                    str(md_path.as_posix()),
                ],
                "judgment_boundary": (
                    "Evidence run only. This selects the first clean feature-frame target; "
                    "it does not materialize the freeze, model readiness, runtime authority, "
                    "or operating promotion."
                ),
                "external_verification_status": "not_applicable",
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    raw_root = Path(args.raw_root)
    output_dir = Path(args.output_dir)
    payload = analyze_feature_frame_target(raw_root)
    write_outputs(output_dir, payload)
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
