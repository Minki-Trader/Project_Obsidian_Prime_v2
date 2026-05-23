from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
STAGE272_ID = "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
STAGE273_ID = "273_onnx_candidate_campaign__time_risk_router_stability_validation"
RUN_ID = "run272E_close_stage272_open_stage273_stability_validation_v1"
STAGE273_OPEN_ID = "stage273_time_risk_router_stability_validation_open_v1"
SOURCE_RUN_ID = "run272D_review_time_risk_router_mt5_probe_v1"
STATUS = "completed_stage272_closeout_stage273_stability_validation_open_no_candidate_selection"
JUDGMENT = "stage272_pressure_survivor_handoff_stage273_opened_no_candidate_selection"
NEXT_ACTION = "run273A_design_time_risk_router_stability_validation_packet"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE272 = ROOT / "stages" / STAGE272_ID
STAGE273 = ROOT / "stages" / STAGE273_ID
RUN272E = STAGE272 / "02_runs" / "run272E"
REVIEWS272 = STAGE272 / "03_reviews"
REVIEWS273 = STAGE273 / "03_reviews"
SELECTED272 = STAGE272 / "04_selected" / "selection_status.md"
SELECTED273 = STAGE273 / "04_selected" / "selection_status.md"

SOURCE_SURVIVOR_QUEUE = STAGE272 / "02_runs" / "run272D" / "stage273_stability_queue.csv"
SOURCE_REVIEW = STAGE272 / "02_runs" / "run272D" / "pressure_survivor_review.csv"
SOURCE_FAILURE_MEMORY = STAGE272 / "02_runs" / "run272D" / "pressure_failure_memory.csv"
SOURCE_RUN272D_MANIFEST = STAGE272 / "02_runs" / "run272D" / "run_manifest.json"
SOURCE_RUN272D_LINEAGE = STAGE272 / "02_runs" / "run272D" / "artifact_lineage_receipt.json"
SOURCE_RUN272D_REPORT = REVIEWS272 / "run272D_report.md"
SOURCE_RUN272C_KPI = STAGE272 / "02_runs" / "run272C" / "mt5_kpi_summary.csv"

HANDOFF_MANIFEST = RUN272E / "stage273_handoff_manifest.json"
RUN_MANIFEST = RUN272E / "run_manifest.json"
LINEAGE_RECEIPT = RUN272E / "artifact_lineage_receipt.json"
STAGE272_CLOSEOUT = REVIEWS272 / "stage272_closeout_stage273_stability_validation_handoff.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-23_stage272_closeout_stage273_stability_validation_open.md"

STAGE273_BRIEF = STAGE273 / "00_spec" / "stage_brief.md"
STAGE273_INPUTS = STAGE273 / "01_inputs" / "input_refs.md"
STAGE273_REVIEW_INDEX = REVIEWS273 / "review_index.md"
STAGE273_LEDGER = REVIEWS273 / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"

RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
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
]
STAGE_LEDGER_COLUMNS = [
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
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    raw = io_path(path).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    with io_path(temp_path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: "" if row.get(column) is None else row.get(column) for column in columns})
    io_path(temp_path).replace(io_path(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> None:
    existing = read_csv_rows(path)
    new_keys = {str(row[key]) for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, merged, columns)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def remove_focus_items(text: str, marker: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("current_focus:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith((" ", "-")):
            end = index
            break
    focus_lines = lines[start + 1:end]
    kept: list[str] = []
    index = 0
    while index < len(focus_lines):
        line = focus_lines[index]
        if not line.startswith("- >-"):
            kept.append(line)
            index += 1
            continue
        block_end = index + 1
        while block_end < len(focus_lines) and not focus_lines[block_end].startswith("- >-"):
            block_end += 1
        block = focus_lines[index:block_end]
        if not any(marker in block_line for block_line in block):
            kept.extend(block)
        index = block_end
    return "\n".join([*lines[: start + 1], *kept, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def source_paths() -> list[Path]:
    return [
        SOURCE_SURVIVOR_QUEUE,
        SOURCE_REVIEW,
        SOURCE_FAILURE_MEMORY,
        SOURCE_RUN272D_MANIFEST,
        SOURCE_RUN272D_LINEAGE,
        SOURCE_RUN272D_REPORT,
        SOURCE_RUN272C_KPI,
    ]


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("; ".join(missing))


def load_survivors() -> list[dict[str, str]]:
    rows = read_csv_rows(SOURCE_SURVIVOR_QUEUE)
    if not rows:
        raise ValueError("Stage273 stability queue is empty.")
    return rows


def write_stage273_docs(survivors: Sequence[Mapping[str, str]]) -> None:
    survivor_lines = "\n".join(
        f"- `{row['variant_id']}` `{row['tier_scope']}`: PF_min(최소 수익 팩터) `{row['profit_factor_min']}`, net_sum(순수익 합) `{row['net_profit_sum']}`, DD_max(최대 손실폭) `{row['max_drawdown_percent_max']}`"
        for row in survivors
    )
    write_md(
        STAGE273_BRIEF,
        f"""# {STAGE273_ID}

Stage273(273단계)는 q04 time-risk router(시간 위험 라우터) pressure survivor(압박 생존 분기)의 stability validation(안정성 검증) 단계다.
효과(effect, 효과): Stage272(272단계)의 좋은 MT5(`MetaTrader 5`, 메타트레이더5) 숫자를 곧바로 candidate package(후보 패키지)로 부르지 않고, 약한 월/세션/구간/곡선/거래 품질을 다시 압박한다.

## Bounded Question(경계 질문)

q04 weak-clock throttle router(4번 약한 시계 제한 라우터)가 validation/OOS(검증/표본외) 양쪽에서 balance/equity curve(잔액/평가금 곡선), drawdown(손실폭), weak slice(약한 구간), trade quality(거래 품질)를 견디는가?
효과(effect, 효과): 좋은 PF(profit factor, 수익 팩터)와 순수익만 보고 ONNX-worthy candidate(온엑스화 가치 후보)로 과장하지 않는다.

## Stability Seed(안정성 씨앗)

{survivor_lines}

## Required Evidence(필수 근거)

- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산) 또는 out_of_scope_by_claim(주장 범위 밖)
- balance/equity curve(잔액/평가금 곡선) 전체와 확대 구간
- month/session/chron slice(월/세션/시간 순서 구간)
- trade count/net/PF/DD/recovery/expectancy(거래 수/순수익/수익 팩터/손실폭/회복/기대값)
- Adapter identity precheck(어댑터 정체성 사전 점검)
- no selected candidate claim(선택 후보 주장 없음)

## Exit Conditions(종료 조건)

- q04(4번 분기)가 안정성 압박을 견디면 Adapter package(어댑터 패키지) 준비 단계로 넘긴다.
- 약한 월/세션, 확대 곡선, 거래 품질에서 무너지면 failure memory(실패 기억)로 닫는다.
- selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 이 단계 개방만으로 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        STAGE273_INPUTS,
        f"""# Stage273 Input References(273단계 입력 참조)

## Source Inputs(원천 입력)

- Stage272 closeout(272단계 종료): `{rel(STAGE272_CLOSEOUT)}`
- run272D report(272D 보고): `{rel(SOURCE_RUN272D_REPORT)}`
- run272D stability queue(272D 안정성 대기열): `{rel(SOURCE_SURVIVOR_QUEUE)}`
- run272D failure memory(272D 실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- run272C KPI summary(272C KPI 요약): `{rel(SOURCE_RUN272C_KPI)}`

## Consumed Seed(소비할 씨앗)

`run272A_q04_weak_clock_throttle_router`만 stability validation seed(안정성 검증 씨앗)로 소비한다.
효과(effect, 효과): q01~q03(1~3번 분기)을 후보처럼 되살리지 않는다.

## Not Allowed(금지)

- selected candidate(선택 후보)
- selected research baseline(선택 연구 기준선)
- ONNX readiness(온엑스 준비)
- runtime authority(런타임 권위)
- operating promotion(운영 승격)
- production baseline(운영 기준선)
""",
    )
    write_md(
        SELECTED273,
        f"""# Stage273 Selection Status(273단계 선택 상태)

- stage_status(단계 상태): `opened_time_risk_router_stability_validation_no_candidate_selection`
- current_packet(현재 작업 묶음): `stage273_time_risk_router_stability_validation_v1`
- current_run(현재 실행): `{STAGE273_OPEN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE272_ID}`
- stability_seed(안정성 씨앗): `run272A_q04_weak_clock_throttle_router`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

Stage273(273단계)는 q04(4번 분기)의 stability validation(안정성 검증)을 위해 열렸다.
효과(effect, 효과): q04(4번 분기)를 후보로 고르지 않고, 곡선/구간/거래 품질 압박을 먼저 진행한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        STAGE273_REVIEW_INDEX,
        f"""# Stage273 Review Index(273단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE273_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE273_INPUTS)}`
- selection_status(선택 상태): `{rel(SELECTED273)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE273_LEDGER)}`
- source_stage272_closeout(원천 272단계 종료): `{rel(STAGE272_CLOSEOUT)}`
- source_stability_queue(원천 안정성 대기열): `{rel(SOURCE_SURVIVOR_QUEUE)}`
""",
    )
    write_csv(
        STAGE273_LEDGER,
        [
            {
                "row_id": f"{STAGE273_OPEN_ID}__stage_open",
                "stage_id": STAGE273_ID,
                "run_id": STAGE273_OPEN_ID,
                "view": "stage_open_stability_validation",
                "tier_scope": "Tier A+B stability validation seed",
                "scoreboard": "stage_open",
                "status": "opened_time_risk_router_stability_validation_no_candidate_selection",
                "judgment": "stage_open_no_candidate_selection",
                "evidence_boundary": "stage_open_only",
                "report_path": rel(STAGE273_BRIEF),
                "notes": f"source_run={RUN_ID};next_action={NEXT_ACTION}.",
            }
        ],
        STAGE_LEDGER_COLUMNS,
    )


def write_handoff_docs(survivors: Sequence[Mapping[str, str]], created_at: str) -> None:
    survivor_lines = "\n".join(
        f"- `{row['variant_id']}` `{row['tier_scope']}`: PF_min `{row['profit_factor_min']}`, expectancy_min `{row['expectancy_min']}`, DD_max `{row['max_drawdown_percent_max']}`"
        for row in survivors
    )
    handoff = {
        "run_id": RUN_ID,
        "stage_id": STAGE272_ID,
        "target_stage_id": STAGE273_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "survivor_count": len(survivors),
        "survivors": list(survivors),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(HANDOFF_MANIFEST, handoff)
    write_md(
        STAGE272_CLOSEOUT,
        f"""# Stage272 Closeout and Stage273 Handoff(272단계 종료와 273단계 인계)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- target_stage(대상 단계): `{STAGE273_ID}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

Stage272(272단계)는 q04(4번 분기)를 pressure survivor(압박 생존 분기)로 남기고 닫는다.
효과(effect, 효과): Stage273(273단계)는 이 survivor(생존 분기)를 stability validation(안정성 검증) 질문으로만 받아, 후보 선택이나 ONNX(온엑스) 준비를 아직 주장하지 않는다.

## Handoff Survivors(인계 생존 분기)

{survivor_lines}

## Failure Boundary(실패 경계)

q01(1번 분기)은 reference control(참고 대조), q02~q03(2~3번 분기)은 PF/DD(수익 팩터/손실폭) 품질 부족으로 failure memory(실패 기억)에 남긴다.
효과(effect, 효과): Stage273(273단계)가 모든 분기를 다시 살리는 repair loop(수리 반복)가 되지 않게 한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        DECISION_DOC,
        f"""# Decision: Stage272 Closeout and Stage273 Open(결정: 272단계 종료와 273단계 개방)

- date(날짜): `2026-05-23`
- decision(결정): Stage272(272단계)를 pressure probe evidence(압박 탐침 근거)로 닫고 Stage273(273단계) stability validation(안정성 검증)을 연다.
- source_run(원천 실행): `{RUN_ID}`
- target_stage(대상 단계): `{STAGE273_ID}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`

효과(effect, 효과): q04(4번 분기)의 좋은 런타임 숫자를 후보로 과장하지 않고, 다음 큰 질문인 안정성 검증으로 분리한다.

Boundary(경계): `{BOUNDARY}`
""",
    )


def write_manifests(created_at: str) -> None:
    artifacts = [
        HANDOFF_MANIFEST,
        STAGE272_CLOSEOUT,
        DECISION_DOC,
        STAGE273_BRIEF,
        STAGE273_INPUTS,
        SELECTED273,
        STAGE273_REVIEW_INDEX,
        STAGE273_LEDGER,
    ]
    sources = source_paths()
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE272_ID,
        "target_stage_id": STAGE273_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "producer": "stage_pipelines/stage272/closeout_stage272_open_stage273.py",
        "entry_command": "python stage_pipelines/stage272/closeout_stage272_open_stage273.py",
        "source_inputs": [rel(path) for path in sources],
        "input_hashes": {rel(path): sha256_file(path) for path in sources if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    lineage = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [STAGE273_ID, NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": [rel(path) for path in [*artifacts, RUN_MANIFEST, LINEAGE_RECEIPT] if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in [*artifacts, RUN_MANIFEST] if path_exists(path)},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE272 / "03_reviews" / "stage_run_ledger.csv"), rel(STAGE273_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, lineage)


def update_registries(created_at: str) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE272_ID,
                "lane": "stage_closeout_stage_open_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE272_CLOSEOUT),
                "notes": f"Stage272 closed; Stage273 opened; selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
            {
                "run_id": STAGE273_OPEN_ID,
                "stage_id": STAGE273_ID,
                "lane": "stage_open_stability_validation",
                "status": "opened_time_risk_router_stability_validation_no_candidate_selection",
                "judgment": "stage_open_no_candidate_selection",
                "path": rel(STAGE273_BRIEF),
                "notes": f"Opened from {RUN_ID}; selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage_handoff",
                "stage_id": STAGE272_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage_handoff",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Stage272 closeout Stage273 open(272단계 종료 273단계 개방)",
                "tier_scope": "Tier A+B pressure survivor handoff",
                "kpi_scope": "stage_transition_no_trading_kpi",
                "scoreboard_lane": "stage_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE272_CLOSEOUT),
                "primary_kpi": "survivor=q04;selected_candidate=none",
                "guardrail_kpi": "onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "completed_from_run272C",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE272 / "03_reviews" / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage_handoff",
                "stage_id": STAGE272_ID,
                "run_id": RUN_ID,
                "view": "stage_closeout_stage273_open",
                "tier_scope": "Tier A+B pressure survivor handoff",
                "scoreboard": "stage_handoff",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "stage_transition_no_candidate",
                "report_path": rel(STAGE272_CLOSEOUT),
                "notes": f"target_stage={STAGE273_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_paths = [
        HANDOFF_MANIFEST,
        RUN_MANIFEST,
        LINEAGE_RECEIPT,
        STAGE272_CLOSEOUT,
        DECISION_DOC,
        STAGE273_BRIEF,
        STAGE273_INPUTS,
        SELECTED273,
        STAGE273_REVIEW_INDEX,
        STAGE273_LEDGER,
    ]
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "stage272_closeout_stage273_open_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE272_ID if STAGE272_ID in rel(path) else STAGE273_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Stage272 closeout and Stage273 open artifact.",
        }
        for path in artifact_paths
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs() -> None:
    selection272 = SELECTED272.read_text(encoding="utf-8-sig")
    selection272 = replace_line_prefix(selection272, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection272 = replace_line_prefix(selection272, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection272 = replace_line_prefix(selection272, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection272 = replace_line_prefix(selection272, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection272 = append_once(selection272, "stage272_closeout_stage273_stability_validation_handoff", f"- stage272_closeout_stage273_stability_validation_handoff(272단계 종료 273단계 인계): `{rel(STAGE272_CLOSEOUT)}`")
    write_md(SELECTED272, selection272)

    current = CURRENT_STATE.read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(", "- current_packet(현재 작업 묶음): `stage273_time_risk_router_stability_validation_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{STAGE273_OPEN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE273_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE272_ID}`")
    current = replace_line_prefix(current, "- status(", "- status(상태): `opened_time_risk_router_stability_validation_no_candidate_selection`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "stage273_open_summary",
        f"- stage273_open_summary(273단계 개방 요약): Stage273(273단계)는 q04(4번 분기) stability validation(안정성 검증)으로 열렸다. Effect(효과): Stage272(272단계)의 pressure survivor(압박 생존 분기)를 후보로 확정하지 않고, 곡선/구간/거래품질 압박으로 넘긴다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = WORKSPACE_STATE.read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {STAGE273_OPEN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE273_ID}")
    focus = (
        "- >-\n"
        f"  Stage273(273단계) time-risk router stability validation(시간 위험 라우터 안정성 검증) `{STAGE273_OPEN_ID}`. "
        "Effect(효과): q04(4번 분기)를 selected candidate(선택 후보)가 아니라 stability validation seed(안정성 검증 씨앗)로 받아, 다음 run273A(273A 실행)에서 곡선/약한 구간/거래 품질을 압박한다.\n"
    )
    workspace = remove_focus_items(workspace, STAGE273_OPEN_ID)
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = CHANGELOG.read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 Stage272 closeout Stage273 open(272단계 종료 273단계 개방)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): q04(4번 분기)를 Stage273(273단계) stability validation(안정성 검증) seed(씨앗)로 넘겼다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def execute() -> dict[str, Any]:
    must_exist(source_paths())
    created_at = utc_now()
    survivors = load_survivors()
    for path in [RUN272E, STAGE273 / "00_spec", STAGE273 / "01_inputs", REVIEWS273, STAGE273 / "04_selected"]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_stage273_docs(survivors)
    write_handoff_docs(survivors, created_at)
    write_manifests(created_at)
    update_registries(created_at)
    update_state_docs()
    write_manifests(created_at)
    update_registries(created_at)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE272_ID,
        "target_stage_id": STAGE273_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "survivor_count": len(survivors),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "stage273_brief": rel(STAGE273_BRIEF),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
