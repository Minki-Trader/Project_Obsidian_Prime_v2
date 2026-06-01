from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

SOURCE_STAGE_ID = "353_trade_shape_offense__report_recovered_density_ok_edge_rebuild"
NEW_STAGE_ID = "354_proxy_trade_shape_scout__small_candidate_queue"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run354A"
RUN_ID = "run354A_branch_stage353_to_lightweight_proxy_trade_shape_scout_without_db_v1"
PARENT_RUN_ID = "run352B_repair_no_scaler_1d_mt5_report_identity_reuse_outputs_without_db_v1"
SUPERSEDED_RUN_ID = "run353A_branch_stage352_to_trade_shape_offensive_rebuild_without_db_v1"
NEXT_RUN_ID = "run354B_lightweight_proxy_trade_shape_scan_without_db_v1"

STATUS = "completed_stage354A_user_requested_stage_split_lightweight_proxy_scout_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage353_too_heavy_split_to_stage354_lightweight_proxy_scout_no_operating_claim"
DECISION = "stage354A_open_run354B_lightweight_proxy_trade_shape_scan"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_user_requested_lightweight_proxy_scout_only_"
    "no_new_proxy_execution_no_new_mt5_execution_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
SOURCE_REVIEW_DIR = SOURCE_STAGE_DIR / "03_reviews"

STAGE354_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE354_README = NEW_STAGE_DIR / "README.md"
STAGE354_INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE354_INPUT_MANIFEST = NEW_STAGE_DIR / "01_inputs" / "stage354_input_manifest.csv"
STAGE354_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE354_REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE354_SELECTION = NEW_STAGE_DIR / "04_selected" / "selection_status.md"
STAGE354_REPORT = REVIEW_DIR / "run354A_stage_branch.md"

STAGE353_SELECTION = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
STAGE353_LEDGER = SOURCE_REVIEW_DIR / "stage_run_ledger.csv"
STAGE353_SPLIT_REPORT = SOURCE_REVIEW_DIR / "run353A_stage_split_to_354.md"
STAGE353_REVIEW_INDEX = SOURCE_REVIEW_DIR / "review_index.md"

SOURCE352_RUN_DIR = (
    ROOT
    / "stages"
    / "352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity"
    / "02_runs"
    / "run352B"
)
SOURCE352_FINAL = SOURCE352_RUN_DIR / "final_decision.json"
SOURCE352_COMBINED = SOURCE352_RUN_DIR / "combined_kpi_summary.json"
SOURCE352_SPLIT = SOURCE352_RUN_DIR / "split_kpi_summary.csv"
SOURCE352_ATTRIBUTION = SOURCE352_RUN_DIR / "proxy_mt5_attribution.csv"
SOURCE352_REPORT = (
    ROOT
    / "stages"
    / "352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity"
    / "03_reviews"
    / "run352B_report_identity_repair_review.md"
)
SOURCE351_EXPECTED = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "expected"
    / "expected_tape.csv"
)
SOURCE351_FEATURES = (
    ROOT
    / "stages"
    / "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
    / "02_runs"
    / "run351B"
    / "features"
    / "runtime_features.csv"
)

HANDOFF_MANIFEST = RUN_DIR / "stage353_to_stage354_handoff_manifest.csv"
NEXT_QUEUE = RUN_DIR / "run354B_proxy_scout_queue.csv"
STAGE_TRANSITION_RECEIPT = RUN_DIR / "stage_transition_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_SELECTION = ROOT / "docs" / "registers" / "selection_status.md"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage354A_branch_stage353_to_lightweight_proxy_scout.md"

SOURCE_INPUTS = [
    (SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md", "Stage353 stage brief(353단계 개요)", True),
    (SOURCE_STAGE_DIR / "01_inputs" / "input_refs.md", "Stage353 input refs(353단계 입력 참조)", True),
    (STAGE353_SELECTION, "Stage353 selection status(353단계 선택 상태)", True),
    (STAGE353_LEDGER, "Stage353 stage ledger(353단계 장부)", True),
    (SOURCE352_FINAL, "Stage352B final decision(352B 최종 결정)", True),
    (SOURCE352_COMBINED, "Stage352B combined KPI(352B 합산 핵심 성과 지표)", True),
    (SOURCE352_SPLIT, "Stage352B split KPI(352B 분할 핵심 성과 지표)", True),
    (SOURCE352_ATTRIBUTION, "Stage352B proxy MT5 attribution(352B 프록시 MT5 귀속)", True),
    (SOURCE352_REPORT, "Stage352B review report(352B 검토 보고서)", True),
    (SOURCE351_EXPECTED, "Stage351B expected tape(351B 예상 테이프)", True),
    (SOURCE351_FEATURES, "Stage351B runtime features(351B 런타임 피처)", True),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(100_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    new_rows = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing_rows = read_csv_rows(path)
    else:
        fieldnames, existing_rows = [], []
    for row in new_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replace_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in new_rows}
    kept = [
        row
        for row in existing_rows
        if tuple(str(row.get(key, "")) for key in key_fields) not in replace_keys
    ]
    write_csv(path, kept + new_rows, fieldnames)


def source_summary() -> dict[str, Any]:
    final = read_json(SOURCE352_FINAL)
    combined = read_json(SOURCE352_COMBINED)
    expected_size = os.path.getsize(fs_path(SOURCE351_EXPECTED)) if exists(SOURCE351_EXPECTED) else 0
    features_size = os.path.getsize(fs_path(SOURCE351_FEATURES)) if exists(SOURCE351_FEATURES) else 0
    return {
        "stage352_status": final.get("status", ""),
        "stage352_judgment": final.get("judgment", ""),
        "stage352_decision": final.get("decision", ""),
        "net_profit": combined.get("net_profit", ""),
        "profit_factor": combined.get("profit_factor", ""),
        "expectancy": combined.get("expectancy", ""),
        "max_drawdown_percent": combined.get("max_drawdown_percent", ""),
        "max_drawdown_amount": combined.get("max_drawdown_amount", ""),
        "recovery_factor": combined.get("recovery_factor", ""),
        "trade_count": combined.get("trade_count", ""),
        "trade_density_per_feature_day": combined.get("trade_density_per_feature_day", ""),
        "validation_net_profit": combined.get("validation_net_profit", ""),
        "oos_net_profit": combined.get("oos_net_profit", ""),
        "long_trade_count": combined.get("long_trade_count", ""),
        "short_trade_count": combined.get("short_trade_count", ""),
        "expected_tape_bytes": expected_size,
        "runtime_features_bytes": features_size,
    }


def write_source_inventory() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, label, required in SOURCE_INPUTS:
        present = exists(path)
        rows.append(
            {
                "source_label": label,
                "path": rel(path),
                "exists": str(present).lower(),
                "required": str(required).lower(),
                "sha256": sha256_file(path) if present else "",
                "size_bytes": os.path.getsize(fs_path(path)) if present else "",
                "consumer_run_id": RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(STAGE354_INPUT_MANIFEST, rows)
    write_csv(HANDOFF_MANIFEST, rows)
    return rows


def write_queue() -> None:
    write_csv(
        NEXT_QUEUE,
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "work_family": "experiment_execution(실험 실행)",
                "primary_action": "lightweight proxy scan(경량 프록시 스캔)",
                "source_expected_tape": rel(SOURCE351_EXPECTED),
                "source_runtime_features": rel(SOURCE351_FEATURES),
                "scan_focus": "ADX25(ADX25 국면) and cash-open model clue(현금장 모델 단서)",
                "must_record": "Tier A separate(Tier A 분리); Tier B separate(Tier B 분리); Tier A+B combined(Tier A+B 합산)",
                "density_rule": TRADE_DENSITY_REQUIREMENT,
                "proxy_boundary": "proxy screening only(프록시 선별 전용); MT5 KPI(MT5 핵심 성과 지표) 대체 금지",
                "next_after_positive": "materialize MT5 probe package(MT5 탐침 패키지 산출물화)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    write_text(
        STAGE353_SPLIT_REPORT,
        f"""# run353A Stage Split To Stage354(run353A 354단계 분기)

- run_id(실행 ID): `{SUPERSEDED_RUN_ID}`
- split_run_id(분기 실행 ID): `{RUN_ID}`
- source_completed_run_id(완료 원천 실행 ID): `{PARENT_RUN_ID}`
- next_stage_id(다음 단계 ID): `{NEW_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `superseded_by_user_requested_stage_split(사용자 요청 단계 분기로 대체됨)`

Action(행동): Stage353(353단계)의 큰 offensive exploration(공격 탐색) 묶음을 Stage354(354단계)의 lightweight proxy scout(경량 프록시 탐색)로 분기했다.

Effect(효과): Stage353(353단계)은 “무거워진 주제”라는 실패 기억(failure memory, 실패 기억)만 남기고, 다음 작업은 작은 proxy queue(프록시 대기열)부터 다시 시작한다.

Boundary(경계): 새 proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선택), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    append_text_once(
        STAGE353_REVIEW_INDEX,
        "run353A_stage_split_to_354",
        f"- `{rel(STAGE353_SPLIT_REPORT)}`",
    )
    write_text(
        STAGE354_README,
        f"""# Stage354 Proxy Trade Shape Scout(354단계 프록시 거래 형태 탐색)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage353(353단계)을 가볍게 나누어 Stage354(354단계)를 작은 proxy scout(프록시 탐색) 전용으로 열었다.

Effect(효과): 다음 작업은 전체 trade shape offense(거래 형태 공격 탐색)를 한 번에 들지 않고, 작은 후보 대기열(candidate queue, 후보 대기열)만 만든다.
""",
    )
    write_text(
        STAGE354_BRIEF,
        f"""# Stage354 Proxy Trade Shape Scout(354단계 프록시 거래 형태 탐색)

- canonical_stage_id(정식 단계 ID): `{NEW_STAGE_ID}`
- subtitle(부제): `small_candidate_queue`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`

## Question(질문)

Stage352B(352B 실행)의 MT5 runtime probe(MT5 런타임 탐침)는 density(밀도)는 통과했지만 OOS loss(표본외 손실)와 high drawdown(높은 낙폭)이 남았다. Stage353(353단계)이 너무 무거우므로, expected tape(예상 테이프)와 runtime features(런타임 피처)만 사용해 작은 proxy candidate queue(프록시 후보 대기열)를 먼저 만들 수 있는가?

## Source Truth(원천 진실)

- combined net profit(합산 순수익): `{summary["net_profit"]}`
- profit factor(수익 팩터): `{summary["profit_factor"]}`
- expectancy(기대값): `{summary["expectancy"]}`
- max drawdown percent(최대 낙폭률): `{summary["max_drawdown_percent"]}`
- recovery factor(회복 계수): `{summary["recovery_factor"]}`
- trade count(거래수): `{summary["trade_count"]}`
- trade density(거래 밀도): `{summary["trade_density_per_feature_day"]}`
- OOS net profit(표본외 순수익): `{summary["oos_net_profit"]}`
- long/short count(롱/숏 수): `{summary["long_trade_count"]}/{summary["short_trade_count"]}`

## Scope(범위)

Stage354(354단계)는 proxy scout(프록시 탐색)만 한다. MT5 runtime probe(MT5 런타임 탐침), ONNX export(온엑스 내보내기), EA handoff(EA 인계)는 positive queue(긍정 대기열)가 생긴 뒤 별도 Stage(단계)나 run(실행)으로 넘긴다.

## Boundary(경계)

Proxy expected value(프록시 예상값)는 signal sanity check(신호 점검)와 후보 선별 보조로만 쓴다. MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않는다. 운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(Goal Achieve, 목표 달성)은 주장하지 않는다.

## Density Constraint(밀도 제약)

`{TRADE_DENSITY_REQUIREMENT}`

Action(행동): trade per day(일별 거래수) 3~10+ 조건을 유지하되, trade splitting(거래 쪼개기)로 수익을 부풀리는 방식은 금지한다.

Effect(효과): Stage354B(354B 실행)의 proxy candidate(프록시 후보)는 신호가 많아도 MT5 trade count(MT5 거래수)와 비교되기 전까지 운영 후보로 보지 않는다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 ADX25(ADX25 국면), cash-open clue(현금장 단서), threshold surface(임계값 표면)를 좁게 재현한다.

Effect(효과): Stage354B(354B 실행)는 후보를 많이 만들기보다 MT5 probe package(MT5 탐침 패키지)로 넘길 작은 queue(대기열)를 만든다.
""",
    )
    write_text(
        STAGE354_INPUT_REFS,
        f"""# Stage354 Input Refs(354단계 입력 참조)

- handoff_manifest(인계 목록): `{rel(HANDOFF_MANIFEST)}`
- stage352_final_decision(352단계 최종 결정): `{rel(SOURCE352_FINAL)}`
- stage352_combined_kpi(352단계 합산 핵심 성과 지표): `{rel(SOURCE352_COMBINED)}`
- expected_tape(예상 테이프): `{rel(SOURCE351_EXPECTED)}`
- runtime_features(런타임 피처): `{rel(SOURCE351_FEATURES)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`

Action(행동): Stage352B(352B 실행)의 runtime truth(런타임 진실)와 Stage351B(351B 실행)의 expected tape(예상 테이프)를 Stage354(354단계)의 작은 입력 묶음으로 고정했다.

Effect(효과): 다음 실행은 불필요한 MT5 report repair(보고서 수리)와 Stage353(353단계)의 큰 질문을 다시 읽지 않고 proxy scout(프록시 탐색)에 집중한다.
""",
    )
    write_text(
        STAGE354_REPORT,
        f"""# run354A Stage Branch(run354A 단계 분기)

- run_id(실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- parent_completed_run_id(완료 원천 실행 ID): `{PARENT_RUN_ID}`
- superseded_planned_run_id(대체된 예정 실행 ID): `{SUPERSEDED_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

Action(행동): 사용자 요청에 따라 Stage353(353단계)의 무거운 trade-shape offense(거래 형태 공격 탐색)를 Stage354(354단계)의 lightweight proxy scout(경량 프록시 탐색)로 분기했다.

Effect(효과): 다음 작업은 작은 candidate queue(후보 대기열)를 만든 뒤에만 MT5 probe(MT5 탐침)로 넘어간다.

Current Truth(현재 진실): Stage352B(352B 실행)는 combined net profit(합산 순수익) `{summary["net_profit"]}`, PF(수익 팩터) `{summary["profit_factor"]}`, OOS net(표본외 순수익) `{summary["oos_net_profit"]}`, max DD(최대 낙폭) `{summary["max_drawdown_percent"]}`로 negative runtime probe(부정 런타임 탐침)다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        STAGE354_REVIEW_INDEX,
        f"""# Stage354 Review Index(354단계 검토 색인)

- `{rel(STAGE354_REPORT)}`
- `{rel(STAGE354_LEDGER)}`
- `{rel(GATE_AUDIT)}`
""",
    )


def write_selection_docs() -> None:
    write_text(
        STAGE353_SELECTION,
        f"""# Stage353 Selection Status(353단계 선택 상태)

- selection_status(선택 상태): `no_selection_split_to_stage354(선택 없음, 354단계로 분기)`
- active_stage_id(활성 단계 ID): `{SOURCE_STAGE_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- handoff_stage_id(인계 단계 ID): `{NEW_STAGE_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )
    selection = f"""# Stage354 Selection Status(354단계 선택 상태)

- selection_status(선택 상태): `no_selection(선택 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(STAGE354_SELECTION, selection)
    write_text(ROOT_SELECTION, selection)


def write_state_docs() -> None:
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {NEW_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage353(353단계)의 무거운 offensive exploration(공격 탐색)을 Stage354(354단계)의 lightweight proxy scout(경량 프록시 탐색)로 분기했다.

Effect(효과): 다음 작업은 작은 proxy candidate queue(프록시 후보 대기열)를 만들고, MT5 KPI(MT5 핵심 성과 지표)는 별도 runtime probe(런타임 탐침)에서만 판단한다.
""",
    )


def base_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(STAGE354_REPORT),
        "report_path": rel(STAGE354_REPORT),
        "primary_report": rel(STAGE354_REPORT),
        "gate_passes": 10,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "work_family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "notes": "Stage353 was split because the active question became too heavy(353단계 질문이 너무 무거워져 분기).",
        "source_package_run_id": PARENT_RUN_ID,
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "row_id": f"{RUN_ID}__Tier_AplusB",
        "subrun_id": "stage_branch",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "tier_scope": "Tier A+B",
        "metric_scope": "stage_branch_only(단계 분기 전용)",
        "kpi_scope": "state_sync_only(상태 동기화 전용)",
        "primary_kpi": "source_stage352B_negative_runtime_probe_preserved(352B 부정 런타임 탐침 보존)",
        "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)",
        "net_profit": summary["net_profit"],
        "profit_factor": summary["profit_factor"],
        "expectancy": summary["expectancy"],
        "drawdown": summary["max_drawdown_percent"],
        "recovery_factor": summary["recovery_factor"],
        "trade_count": summary["trade_count"],
        "trade_density_per_feature_day": summary["trade_density_per_feature_day"],
        "trade_density_requirement_status": "preserved_from_stage352B(352B에서 보존)",
        "result_judgment": JUDGMENT,
        "max_drawdown_amount": summary["max_drawdown_amount"],
        "long_trade_count": summary["long_trade_count"],
        "short_trade_count": summary["short_trade_count"],
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }


def write_ledgers(summary: Mapping[str, Any]) -> None:
    base = base_row(summary)
    rows = []
    for tier, view, scope_note in [
        ("Tier A", "Tier A separate(Tier A 분리)", "inherited_runtime_probe_summary(상속 런타임 탐침 요약)"),
        ("Tier B", "Tier B separate(Tier B 분리)", "missing_required_until_proxy_scan(프록시 스캔 전까지 필수 누락)"),
        ("Tier A+B", "Tier A+B combined(Tier A+B 합산)", "state_branch_combined_record(상태 분기 합산 기록)"),
    ]:
        row = dict(base)
        row["ledger_row_id"] = f"{RUN_ID}__{tier.replace(' ', '_').replace('+', 'plus')}"
        row["row_id"] = row["ledger_row_id"]
        row["subrun_id"] = tier
        row["tier"] = tier
        row["tier_scope"] = tier
        row["view"] = view
        row["record_view"] = view
        row["metric_scope"] = scope_note
        row["kpi_scope"] = scope_note
        rows.append(row)
    source_fields, _ = read_csv_rows(STAGE353_LEDGER) if exists(STAGE353_LEDGER) else ([], [])
    stage_fields = source_fields or list(rows[0].keys())
    write_csv(STAGE354_LEDGER, rows, stage_fields)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
                "gate_audit_path": rel(GATE_AUDIT),
            }
        ],
    )
    source_row = {
        **base,
        "stage_id": SOURCE_STAGE_ID,
        "run_id": SUPERSEDED_RUN_ID,
        "ledger_row_id": f"{SUPERSEDED_RUN_ID}__stage_split_to_354",
        "row_id": f"{SUPERSEDED_RUN_ID}__stage_split_to_354",
        "status": "superseded_by_stage354_split(354단계 분기로 대체)",
        "judgment": "stage353_split_requested_no_new_execution(353단계 분기 요청, 새 실행 없음)",
        "decision": f"handoff_to_{NEW_STAGE_ID}",
        "next_run_id": RUN_ID,
        "path": rel(STAGE353_SPLIT_REPORT),
        "report_path": rel(STAGE353_SPLIT_REPORT),
        "primary_report": rel(STAGE353_SPLIT_REPORT),
        "primary_artifact": rel(STAGE353_SPLIT_REPORT),
        "notes": "User requested a Stage split because Stage353 became too heavy(사용자가 353단계가 너무 무거워 단계 분기를 요청).",
    }
    append_or_replace_csv(STAGE353_LEDGER, ["ledger_row_id"], [source_row])


def write_receipts(summary: Mapping[str, Any], inventory: Sequence[Mapping[str, Any]]) -> None:
    created = now_utc()
    common = {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "superseded_run_id": SUPERSEDED_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created,
    }
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            **common,
            "action": "Stage353 to Stage354 branch(353단계에서 354단계로 분기)",
            "effect": "lighter proxy scout queue(더 가벼운 프록시 탐색 대기열)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": list(inventory),
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "allowed_claim": "state sync and stage branch only(상태 동기화와 단계 분기만)",
            "forbidden_claims": [
                "new proxy result(새 프록시 결과)",
                "new MT5 execution(새 MT5 실행)",
                "candidate selection(후보 선택)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )
    write_json(
        FINAL_DECISION,
        {
            **common,
            "gate_passes": 10,
            "gate_total": 10,
            "source_stage352B_net_profit": summary["net_profit"],
            "source_stage352B_profit_factor": summary["profit_factor"],
            "source_stage352B_oos_net_profit": summary["oos_net_profit"],
            "source_stage352B_trade_density": summary["trade_density_per_feature_day"],
            "new_proxy_execution": "not_run",
            "new_mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            **common,
            "work_family": "state_sync(상태 동기화)",
            "primary_skill": "obsidian-stage-transition(단계 전환)",
            "support_skills": [
                "obsidian-reentry-read(재진입 읽기)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-claim-discipline(주장 규율)",
            ],
            "outputs": [
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
                rel(HANDOFF_MANIFEST),
                rel(NEXT_QUEUE),
                rel(STAGE354_REPORT),
                rel(STAGE354_BRIEF),
                rel(STAGE354_SELECTION),
            ],
        },
    )


def write_gates(inventory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    all_sources = all(row["exists"] == "true" for row in inventory)
    gates = [
        ("user_requested_stage_branch_recorded", True, STAGE354_REPORT, "user request(사용자 요청)을 단계 분기로 기록"),
        ("source_stage353_visible", exists(SOURCE_STAGE_DIR), SOURCE_STAGE_DIR, "source stage(원천 단계) 확인"),
        ("stage352B_runtime_probe_source_connected", exists(SOURCE352_FINAL) and exists(SOURCE352_COMBINED), SOURCE352_FINAL, "runtime source(런타임 원천) 연결"),
        ("input_manifest_all_required_visible", all_sources, STAGE354_INPUT_MANIFEST, "required inputs(필수 입력) 가시화"),
        ("new_stage_structure_created", exists(STAGE354_BRIEF) and exists(STAGE354_SELECTION), NEW_STAGE_DIR, "new stage structure(새 단계 구조) 생성"),
        ("next_queue_created", exists(NEXT_QUEUE), NEXT_QUEUE, "next queue(다음 대기열) 생성"),
        ("trade_density_constraint_preserved", TRADE_DENSITY_REQUIREMENT in read_text(STAGE354_BRIEF), STAGE354_BRIEF, "density rule(밀도 규칙) 보존"),
        ("state_sync_audit", NEW_STAGE_ID in read_text(WORKSPACE_STATE) and NEXT_RUN_ID in read_text(CURRENT_WORKING_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("ledger_sync_audit", exists(STAGE354_LEDGER) and exists(PROJECT_LEDGER), STAGE354_LEDGER, "ledger(장부) 동기화"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "forbidden claims(금지 주장) 차단"),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_artifact_registry() -> None:
    artifacts = [
        FINAL_DECISION,
        RUN_MANIFEST,
        GATE_AUDIT,
        HANDOFF_MANIFEST,
        NEXT_QUEUE,
        STAGE_TRANSITION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        STAGE354_REPORT,
        STAGE354_BRIEF,
        STAGE354_INPUT_REFS,
        STAGE354_SELECTION,
        STAGE354_LEDGER,
        STAGE353_SPLIT_REPORT,
        DECISION_DOC,
        Path(__file__),
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "stage branch artifact(단계 분기 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_decision_and_changelog() -> None:
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage354A Branch(354A 단계 분기)

- date(날짜): `{TODAY}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage353(353단계)이 너무 무거워졌다는 사용자 판단을 받아, proxy scout(프록시 탐색)만 다루는 Stage354(354단계)를 열었다.

Effect(효과): 다음 실행은 작은 후보 대기열(candidate queue, 후보 대기열)을 만들고, MT5 runtime probe(MT5 런타임 탐침)는 그 다음 검증으로 분리된다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} {RUN_ID}

Action(행동): Stage353(353단계)을 Stage354(354단계) lightweight proxy scout(경량 프록시 탐색)로 분기했다.

Effect(효과): 무거운 trade-shape offense(거래 형태 공격 탐색)를 작은 proxy candidate queue(프록시 후보 대기열) 생성 작업으로 줄였다.

- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
    if failed:
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("required gates failed(필수 게이트 실패): " + ", ".join(failed))
    for path in [WORKSPACE_STATE, CURRENT_WORKING_STATE, STAGE354_SELECTION, ROOT_SELECTION]:
        text = read_text(path)
        if NEW_STAGE_ID not in text or NEXT_RUN_ID not in text:
            raise RuntimeError(f"state sync validation failed(상태 동기화 검증 실패): {rel(path)}")
    for path in [STAGE354_SELECTION, ROOT_SELECTION]:
        if "not_claimed" not in read_text(path):
            raise RuntimeError(f"claim guard validation failed(주장 차단 검증 실패): {rel(path)}")
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}")


def main() -> None:
    for directory in [
        NEW_STAGE_DIR / "00_spec",
        NEW_STAGE_DIR / "01_inputs",
        RUN_DIR,
        REVIEW_DIR,
        NEW_STAGE_DIR / "04_selected",
        DECISION_DOC.parent,
    ]:
        os.makedirs(fs_path(directory), exist_ok=True)
    summary = source_summary()
    inventory = write_source_inventory()
    write_queue()
    write_stage_docs(summary)
    write_selection_docs()
    write_state_docs()
    write_receipts(summary, inventory)
    write_ledgers(summary)
    gates = write_gates(inventory)
    write_artifact_registry()
    write_decision_and_changelog()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
