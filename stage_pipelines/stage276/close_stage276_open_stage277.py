from __future__ import annotations

import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE276_ID = "276_onnx_candidate_campaign__aggressive_fresh_surface_probe"
STAGE277_ID = "277_onnx_candidate_campaign__fresh_thesis_rebuild"
OLD_STAGE277_ID = "277_onnx_candidate_campaign__fresh_thesis_rebuild_after_aggressive_surface_failure"
SOURCE_RUN_ID = "run276D_review_aggressive_fresh_surface_mt5_probe_v1"
RUN_ID = "run276E_close_stage276_open_stage277_fresh_thesis_rebuild_v1"
STAGE277_OPEN_ID = "stage277_fresh_thesis_rebuild_after_aggressive_surface_failure_open_v1"
STATUS = "completed_stage276_closeout_stage277_fresh_thesis_rebuild_open_no_candidate_selection"
JUDGMENT = "valid_negative_aggressive_fresh_surface_probe_stage277_opened_no_candidate_selection"
NEXT_ACTION = "run277A_design_fresh_thesis_rebuild_packet"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE276 = ROOT / "stages" / STAGE276_ID
STAGE277 = ROOT / "stages" / STAGE277_ID
RUN276D = STAGE276 / "02_runs" / "run276D"
RUN_DIR = STAGE276 / "02_runs" / "run276E"
REVIEWS276 = STAGE276 / "03_reviews"
REVIEWS277 = STAGE277 / "03_reviews"
SELECTED276 = STAGE276 / "04_selected" / "selection_status.md"
SELECTED277 = STAGE277 / "04_selected" / "selection_status.md"

SOURCE_RUN_MANIFEST = RUN276D / "run_manifest.json"
SOURCE_REVIEW_RESULT = RUN276D / "review_result.json"
SOURCE_PACKAGE_SUMMARY = RUN276D / "package_summary.csv"
SOURCE_FAILURE_MEMORY = RUN276D / "failure_memory.csv"
SOURCE_NEGATIVE_SLICE = RUN276D / "negative_slice_summary.csv"
SOURCE_VARIANT_SUMMARY = RUN276D / "variant_summary.csv"
SOURCE_PARSER_CHECKS = RUN276D / "parser_checks.csv"
SOURCE_GATES = RUN276D / "gates.csv"
SOURCE_FORENSICS = RUN276D / "forensics_summary.json"
SOURCE_LINEAGE = RUN276D / "artifact_lineage_receipt.json"
SOURCE_REPORT = REVIEWS276 / "run276D_report.md"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
HANDOFF_MANIFEST = RUN_DIR / "stage277_handoff_manifest.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
SEED_QUEUE_RUN = RUN_DIR / "stage277_rebuild_thesis_seed_queue.csv"
FAILURE_MEMORY_RUN = RUN_DIR / "stage276_failure_memory.csv"
NEGATIVE_SLICE_RUN = RUN_DIR / "stage276_negative_slice_summary.csv"
VARIANT_SUMMARY_RUN = RUN_DIR / "stage276_variant_summary.csv"
STAGE276_CLOSEOUT = REVIEWS276 / "stage276_closeout_stage277_handoff.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-23_stage276_closeout_stage277_fresh_thesis_rebuild_open.md"

STAGE277_BRIEF = STAGE277 / "00_spec" / "stage_brief.md"
STAGE277_INPUTS = STAGE277 / "01_inputs" / "input_refs.md"
STAGE277_FAILURE_MEMORY = STAGE277 / "01_inputs" / "stage276_failure_memory.csv"
STAGE277_NEGATIVE_SLICE = STAGE277 / "01_inputs" / "stage276_negative_slice_summary.csv"
STAGE277_VARIANT_SUMMARY = STAGE277 / "01_inputs" / "stage276_variant_summary.csv"
STAGE277_SEED_QUEUE = STAGE277 / "01_inputs" / "stage277_rebuild_thesis_seed_queue.csv"
STAGE277_REVIEW_INDEX = REVIEWS277 / "review_index.md"
STAGE277_LEDGER = REVIEWS277 / "stage_run_ledger.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage276/close_stage276_open_stage277.py")

STAGE_LEDGER_COLUMNS = (
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
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
SEED_COLUMNS = (
    "seed_id",
    "stage_id",
    "source_memory",
    "fresh_thesis",
    "source_failure_pattern",
    "broad_sweep",
    "extreme_sweep",
    "micro_search_gate",
    "discard_condition",
    "required_evidence",
    "tier_scope",
    "candidate_boundary",
    "next_action",
)


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def source_inputs() -> list[Path]:
    return [
        SOURCE_RUN_MANIFEST,
        SOURCE_REVIEW_RESULT,
        SOURCE_PACKAGE_SUMMARY,
        SOURCE_FAILURE_MEMORY,
        SOURCE_NEGATIVE_SLICE,
        SOURCE_VARIANT_SUMMARY,
        SOURCE_PARSER_CHECKS,
        SOURCE_GATES,
        SOURCE_FORENSICS,
        SOURCE_LINEAGE,
        SOURCE_REPORT,
    ]


def copy_csv(source: Path, target: Path) -> list[dict[str, str]]:
    rows = read_csv_rows(source)
    columns = list(rows[0].keys()) if rows else ["empty"]
    write_csv(target, columns, rows)
    return rows


def review_result() -> dict[str, Any]:
    return json.loads(io_path(SOURCE_REVIEW_RESULT).read_text(encoding="utf-8-sig"))


def seed_rows() -> list[dict[str, str]]:
    return [
        {
            "seed_id": "stage277A_session_loss_avoidance_surface",
            "stage_id": STAGE277_ID,
            "source_memory": "Stage276(276단계) cp275A/cp275D weak month/session/deep slice(약한 월/세션/깊은 구간) failure memory(실패 기억)",
            "fresh_thesis": "session loss avoidance surface(세션 손실 회피 표면)가 약한 시간대를 단순 제거가 아니라 entry timing/risk state(진입 시점/위험 상태)로 다시 만든다.",
            "source_failure_pattern": "pf_too_thin(수익 팩터 과소), month_hole(월 구멍), deep_slice_hole(깊은 구간 구멍)",
            "broad_sweep": "session bucket(세션 구간), chron segment(시간 순서 구간), volatility context(변동성 문맥)를 넓게 조합한다.",
            "extreme_sweep": "weak-session hard off(약한 세션 완전 차단), weak-session reduced risk(약한 세션 축소 위험), late-chron inversion(후반 시간 역전)을 시험한다.",
            "micro_search_gate": "Tier A/Tier B(티어 A/티어 B) validation/OOS(검증/표본외) 양쪽에서 PF(수익 팩터)와 DD(drawdown, 손실폭)가 동시에 개선될 때만 미세 탐색한다.",
            "discard_condition": "거래 수가 얇아지거나 OOS(표본외) 후반 손실이 커지면 폐기한다.",
            "required_evidence": "feature surface(피처 표면), decision surface(판단 표면), risk logic(위험 로직), MT5 probe design(MT5 탐침 설계), paired tier rows(티어 쌍 행)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
            "candidate_boundary": "fresh thesis seed only(새 논제 씨앗만), selected candidate(선택 후보) 아님",
            "next_action": NEXT_ACTION,
        },
        {
            "seed_id": "stage277B_validation_pf_floor_rebalanced_entry_surface",
            "stage_id": STAGE277_ID,
            "source_memory": "Stage276(276단계) cp275A OOS positive but validation PF thin(표본외 양수지만 검증 수익 팩터 과소) failure memory(실패 기억)",
            "fresh_thesis": "validation PF floor rebalanced entry surface(검증 수익 팩터 하한 재균형 진입 표면)가 OOS(표본외) 공급을 버리지 않고 entry creation(진입 생성)을 다시 만든다.",
            "source_failure_pattern": "validation PF(검증 수익 팩터) 1.05 미만, closed balance DD watch(확정 잔액 손실폭 관찰), month hole(월 구멍)",
            "broad_sweep": "entry source(진입 원천), score margin(점수 여유), risk-distance(위험 거리), hold horizon(보유 예측수평선)을 넓게 바꾼다.",
            "extreme_sweep": "wide entry(넓은 진입), tight entry(좁은 진입), validation-first risk cap(검증 우선 위험 상한), OOS-supply-preserve branch(표본외 공급 보존 분기)를 함께 본다.",
            "micro_search_gate": "validation PF(검증 수익 팩터)가 여유 있게 1.05를 넘고 OOS(표본외) 거래 수가 유지될 때만 미세 탐색한다.",
            "discard_condition": "validation(검증)만 좋아지고 OOS(표본외) 공급 또는 기대값이 무너지면 폐기한다.",
            "required_evidence": "new entry creation receipt(새 진입 생성 영수증), feature order source(피처 순서 원천), risk cap plan(위험 상한 계획), MT5 queue(MT5 대기열)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
            "candidate_boundary": "fresh thesis seed only(새 논제 씨앗만), selected candidate(선택 후보) 아님",
            "next_action": NEXT_ACTION,
        },
        {
            "seed_id": "stage277C_directional_asymmetry_reversal_from_failure_memory",
            "stage_id": STAGE277_ID,
            "source_memory": "Stage276(276단계) cp275B divergence reversal(괴리 반전) OOS negative(표본외 음수) failure memory(실패 기억)",
            "fresh_thesis": "directional asymmetry reversal surface(방향 비대칭 반전 표면)가 cp275B(275B 패키지)를 보존하지 않고, 실패 방향을 side-state feature(방향 상태 피처)로 다시 해석한다.",
            "source_failure_pattern": "OOS negative(표본외 음수), session 13-20 report time(보고 시간 13-20 세션) loss concentration(손실 집중), high DD(높은 손실폭)",
            "broad_sweep": "side-specific entry(방향별 진입), divergence sign flip(괴리 부호 반전), session-aware side cap(세션 인식 방향 상한)을 넓게 시험한다.",
            "extreme_sweep": "long-only(매수 전용), short-only(매도 전용), side flip(방향 반전), no-trade danger session(위험 세션 미거래)을 비교한다.",
            "micro_search_gate": "side split(방향 분리)이 Tier A/Tier B(티어 A/티어 B)에서 같은 방향으로 손실을 줄일 때만 미세 탐색한다.",
            "discard_condition": "방향 반전이 단순 운 좋음이거나 한 티어만 좋아지면 폐기한다.",
            "required_evidence": "side attribution(방향 귀속), session attribution(세션 귀속), decision surface hash(판단 표면 해시), paired tier review(티어 쌍 검토)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
            "candidate_boundary": "fresh thesis seed only(새 논제 씨앗만), selected candidate(선택 후보) 아님",
            "next_action": NEXT_ACTION,
        },
        {
            "seed_id": "stage277D_macro_squeeze_failure_contrast_surface",
            "stage_id": STAGE277_ID,
            "source_memory": "Stage276(276단계) cp275D macro volatility squeeze release(거시 변동성 압축 해제) late OOS hole(후반 표본외 구멍)",
            "fresh_thesis": "macro squeeze contrast surface(거시 압축 대비 표면)가 squeeze release(압축 해제)를 직접 추격하지 않고 failure contrast(실패 대비)를 위험 보상 비대칭으로 쓴다.",
            "source_failure_pattern": "chron_late(시간 후반) deep negative(깊은 음수), OOS negative(표본외 음수), DD(drawdown, 손실폭) 과대",
            "broad_sweep": "macro proxy(거시 대리), volatility expansion(변동성 확장), late-chron risk compression(후반 시간 위험 압축)을 넓게 조합한다.",
            "extreme_sweep": "squeeze-on(압축 중), squeeze-release(압축 해제), post-release cooldown(해제 후 냉각), late-OOS kill switch(후반 표본외 중단)를 시험한다.",
            "micro_search_gate": "late OOS(후반 표본외) 손실이 줄고 전체 trade count(거래 수)가 유지될 때만 미세 탐색한다.",
            "discard_condition": "late loss(후반 손실)를 줄이는 대신 전체 기대값이 사라지면 폐기한다.",
            "required_evidence": "macro feature receipt(거시 피처 영수증), risk/reward asymmetry receipt(위험/보상 비대칭 영수증), MT5 runtime probe plan(MT5 런타임 탐침 계획)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
            "candidate_boundary": "fresh thesis seed only(새 논제 씨앗만), selected candidate(선택 후보) 아님",
            "next_action": NEXT_ACTION,
        },
    ]


def cleanup_old_long_stage277_path() -> None:
    old_stage = ROOT / "stages" / OLD_STAGE277_ID
    if path_exists(old_stage):
        resolved_root = ROOT.resolve()
        resolved_old = old_stage.resolve()
        if resolved_old == resolved_root or resolved_root not in resolved_old.parents:
            raise RuntimeError(f"Refusing to remove outside workspace: {resolved_old}")
        old_io = Path("\\\\?\\" + str(resolved_old)) if sys.platform == "win32" else old_stage
        shutil.rmtree(old_io)

    if path_exists(ARTIFACT_REGISTRY):
        rows = read_csv_rows(ARTIFACT_REGISTRY)
        filtered = [
            row
            for row in rows
            if OLD_STAGE277_ID not in str(row.get("path", ""))
            and OLD_STAGE277_ID not in str(row.get("artifact_id", ""))
            and OLD_STAGE277_ID not in str(row.get("stage_id", ""))
        ]
        if len(filtered) != len(rows):
            write_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, filtered)


def write_stage_docs(
    created_at: str,
    seeds: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    variant_rows: Sequence[Mapping[str, Any]],
    review: Mapping[str, Any],
) -> None:
    seed_lines = "\n".join(
        f"- `{row['seed_id']}`: {row['fresh_thesis']}"
        for row in seeds
    )
    write_md(
        STAGE276_CLOSEOUT,
        f"""# Stage276 Closeout(276단계 종료) and Stage277 Handoff(277단계 인계)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`
- negative_slice_rows(부정 구간 행): `{len(negative_rows)}`
- variant_summary_rows(변형 요약 행): `{len(variant_rows)}`
- survivor_watch_rows(생존 관찰 행): `{review.get('survivor_watch_rows', 0)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Closeout Meaning(종료 의미)

Stage276(276단계)은 aggressive fresh surface MT5 probe(공격형 새 표면 MT5 탐침)를 review(검토)했지만 survivor watch(생존 관찰)가 `0`개였다.
Effect(효과): cp275A/cp275B/cp275D(275A/275B/275D 패키지)는 candidate(후보)가 아니라 failure memory(실패 기억)와 source clue(원천 단서)로만 남긴다.

## Stage277 Seeds(277단계 씨앗)

{seed_lines}

## Claim Boundary(주장 경계)

`{BOUNDARY}`
""",
    )
    write_md(
        DECISION_DOC,
        f"""# Decision(결정): Stage276 Closeout(276단계 종료), Stage277 Open(277단계 개시)

- date(날짜): `2026-05-23`
- created_at_utc(생성 UTC): `{created_at}`
- transition_run(전환 실행): `{RUN_ID}`
- from_stage(이전 단계): `{STAGE276_ID}`
- to_stage(다음 단계): `{STAGE277_ID}`
- decision(결정): Stage276(276단계)을 valid negative(유효한 부정)로 닫고 Stage277(277단계)을 fresh thesis rebuild(새 논제 재구성)로 연다.
- effect(효과): 같은 repair loop(수리 반복)를 이어가지 않고, 실패 기억에서 새 edge/decision/risk surface(거래 우위/판단/위험 표면)를 다시 만든다.
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Evidence(근거)

- run276D_report(276D 보고서): `{rel(SOURCE_REPORT)}`
- failure_memory(실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- negative_slice_summary(부정 구간 요약): `{rel(SOURCE_NEGATIVE_SLICE)}`
- package_summary(패키지 요약): `{rel(SOURCE_PACKAGE_SUMMARY)}`
- parser_checks(파서 점검): `{rel(SOURCE_PARSER_CHECKS)}`
- gate_receipts(게이트 영수증): `{rel(SOURCE_GATES)}`

## Boundary(경계)

Stage277(277단계)은 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX export/parity(온엑스 내보내기/동등성), MT5 runtime reproduction(MT5 런타임 재현)를 아직 주장하지 않는다.
""",
    )
    write_md(
        STAGE277_BRIEF,
        f"""# Stage277 Brief(277단계 개요): Fresh Thesis Rebuild After Aggressive Surface Failure(공격형 표면 실패 이후 새 논제 재구성)

- stage_id(단계 ID): `{STAGE277_ID}`
- opened_by(개시 실행): `{RUN_ID}`
- stage_open_id(단계 개시 ID): `{STAGE277_OPEN_ID}`
- active_question(핵심 질문): Stage276(276단계)의 weak-slice failure memory(약한 구간 실패 기억)를 cp275A/cp275B/cp275D(275A/275B/275D 패키지) 보존이 아니라 fresh thesis(새 논제) 재구성으로 바꿀 수 있는가?
- work_family(작업군): `research_development(연구개발)`
- primary_skill(주 스킬): `obsidian-exploration-mandate(탐색 원칙)`
- support_skills(보조 스킬): `obsidian-artifact-lineage(산출물 계보)`, `obsidian-result-judgment(결과 판정)`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Fresh Thesis Seeds(새 논제 씨앗)

{seed_lines}

## Required Records(필수 기록)

- Tier A separate(Tier A 분리)
- Tier B separate(Tier B 분리)
- Tier A+B combined(Tier A+B 합산)
- feature surface(피처 표면)
- decision surface(판단 표면)
- risk logic(위험 로직)
- Adapter path(어댑터 경로)
- runtime handoff(런타임 인계)
- failure memory(실패 기억)

## Boundary(경계)

Stage277(277단계)은 candidate construction(후보 구성)을 준비하는 단계다.
Effect(효과): 이번 단계에서 selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위), operating promotion(운영 승격)을 만들지 않는다.
""",
    )
    write_md(
        STAGE277_INPUTS,
        f"""# Stage277 Inputs(277단계 입력)

- stage276_closeout(276단계 종료): `{rel(STAGE276_CLOSEOUT)}`
- decision_doc(결정 문서): `{rel(DECISION_DOC)}`
- stage277_seed_queue(277단계 씨앗 대기열): `{rel(STAGE277_SEED_QUEUE)}`
- stage276_failure_memory(276단계 실패 기억): `{rel(STAGE277_FAILURE_MEMORY)}`
- stage276_negative_slice_summary(276단계 부정 구간 요약): `{rel(STAGE277_NEGATIVE_SLICE)}`
- stage276_variant_summary(276단계 변형 요약): `{rel(STAGE277_VARIANT_SUMMARY)}`
- run276D_report(276D 보고서): `{rel(SOURCE_REPORT)}`
- run276D_lineage(276D 계보): `{rel(SOURCE_LINEAGE)}`
- run276D_gates(276D 게이트): `{rel(SOURCE_GATES)}`

Effect(효과): Stage277(277단계)는 Stage276(276단계)의 이름을 후보로 계승하지 않고, 실패 기억과 약한 구간을 새 thesis(논제)의 입력으로만 쓴다.
""",
    )
    write_md(
        STAGE277_REVIEW_INDEX,
        f"""# Stage277 Review Index(277단계 검토 색인)

- stage_brief(단계 개요): `{rel(STAGE277_BRIEF)}`
- input_refs(입력 참조): `{rel(STAGE277_INPUTS)}`
- seed_queue(씨앗 대기열): `{rel(STAGE277_SEED_QUEUE)}`
- failure_memory_source(실패 기억 원천): `{rel(STAGE277_FAILURE_MEMORY)}`
- negative_slice_source(부정 구간 원천): `{rel(STAGE277_NEGATIVE_SLICE)}`
- selection_status(선택 상태): `{rel(SELECTED277)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE277_LEDGER)}`

## Open Run(개시 실행)

- stage277_open(277단계 개시): `{STAGE277_OPEN_ID}`
- next_action(다음 행동): `{NEXT_ACTION}`
""",
    )
    write_md(
        SELECTED277,
        f"""# Stage277 Selection Status(277단계 선택 상태)

- stage_status(단계 상태): `opened_fresh_thesis_rebuild_no_candidate_selection`
- current_run(현재 실행): `{STAGE277_OPEN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

Stage277(277단계)은 Stage276(276단계)의 failure memory(실패 기억)를 fresh thesis seed(새 논제 씨앗)로 바꾸는 단계다.
Effect(효과): 후보명, alias(별칭), profile(프로필), run id(실행 ID)를 candidate package(후보 패키지)로 착각하지 않는다.
""",
    )


def write_receipts(seeds: Sequence[Mapping[str, Any]], review: Mapping[str, Any]) -> None:
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "Stage276 aggressive fresh surface probe(276단계 공격형 새 표면 탐침)",
                "evidence_available": f"run276D report(276D 보고서), failure memory(실패 기억) {len(read_csv_rows(SOURCE_FAILURE_MEMORY))} rows, parser checks(파서 점검), gate receipts(게이트 영수증)",
                "evidence_missing": "selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX export/parity(온엑스 내보내기/동등성), MT5 runtime reproduction(MT5 런타임 재현)",
                "judgment_label": "valid_negative_aggressive_fresh_surface_probe_no_candidate_selection",
                "judgment_class": "valid_negative_or_failure_memory(유효 부정 또는 실패 기억)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "Stage276(276단계)은 survivor watch(생존 관찰) 0개라 후보를 고르지 않고 Stage277(277단계) 새 논제로 넘긴다.",
            },
            {
                "result_subject": "Stage277 fresh thesis rebuild open(277단계 새 논제 재구성 개시)",
                "evidence_available": f"seed queue(씨앗 대기열) {len(seeds)} rows, Stage276 failure memory(276단계 실패 기억)",
                "evidence_missing": "candidate package(후보 패키지), score surface(점수 표면), MT5 result(MT5 결과)",
                "judgment_label": "stage_open_planning_only_no_candidate_selection",
                "judgment_class": "planning_open(계획 개시)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "Stage277(277단계)은 후보 선택이 아니라 새 후보 구성을 설계하는 출발점이다.",
            },
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "artifact_lineage_gate(산출물 계보 게이트)",
                "status": "passed(통과)",
                "evidence_path": rel(HANDOFF_MANIFEST),
                "effect": "Stage276(276단계) 원천 근거와 Stage277(277단계) 입력을 연결한다.",
            },
            {
                "gate_name": "result_judgment_gate(결과 판정 게이트)",
                "status": "passed_valid_negative_boundary(유효 부정 경계 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "Stage276(276단계)을 후보 없음으로 닫고 Stage277(277단계)을 계획 개시로만 연다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_onnx_no_goal(선택 후보 없음/온엑스 없음/목표 달성 없음으로 통과)",
                "evidence_path": rel(SELECTED277),
                "effect": "선택 후보, ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            },
            {
                "gate_name": "stage_scope_gate(단계 범위 게이트)",
                "status": "passed_bounded_fresh_thesis_rebuild(제한된 새 논제 재구성으로 통과)",
                "evidence_path": rel(STAGE277_BRIEF),
                "effect": "한 단계에 모든 작업을 몰지 않고 다음 큰 질문만 연다.",
            },
            {
                "gate_name": "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
                "status": "passed(통과)",
                "evidence_path": rel(GATE_AUDIT),
                "effect": "계보, 판정, 주장 경계, 단계 범위를 closeout(종료)에 연결한다.",
            },
        ],
    )


def write_handoff_manifest(
    created_at: str,
    seeds: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    review: Mapping[str, Any],
) -> None:
    payload = {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "from_stage": STAGE276_ID,
        "to_stage": STAGE277_ID,
        "source_run_id": SOURCE_RUN_ID,
        "stage277_open_id": STAGE277_OPEN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "survivor_watch_rows": review.get("survivor_watch_rows", 0),
        "failure_memory_rows": len(failure_rows),
        "negative_slice_rows": len(negative_rows),
        "seed_rows": list(seeds),
        "source_inputs": [rel(path) for path in source_inputs()],
        "stage277_inputs": [
            rel(STAGE277_SEED_QUEUE),
            rel(STAGE277_FAILURE_MEMORY),
            rel(STAGE277_NEGATIVE_SLICE),
            rel(STAGE277_VARIANT_SUMMARY),
        ],
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(HANDOFF_MANIFEST, payload)


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)}


def manifest_payload(created_at: str, outputs: Sequence[Path], seeds: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "stage_id": STAGE276_ID,
        "target_stage_id": STAGE277_ID,
        "source_run_id": SOURCE_RUN_ID,
        "producer": rel(PRODUCER_PATH),
        "consumer": [STAGE277_ID, NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY)],
        "source_inputs": [rel(path) for path in source_inputs()],
        "source_hashes": output_hashes(source_inputs()),
        "output_artifacts": [rel(path) for path in outputs],
        "output_hashes": output_hashes(outputs),
        "seed_count": len(seeds),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": manifest["consumer"],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE277_LEDGER)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def update_registers(created_at: str, seeds: Sequence[Mapping[str, Any]], outputs: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE276_ID,
                "lane": "stage_closeout",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE276_CLOSEOUT),
                "notes": f"target_stage={STAGE277_ID};seed_rows={len(seeds)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
            {
                "run_id": STAGE277_OPEN_ID,
                "stage_id": STAGE277_ID,
                "lane": "stage_open",
                "status": "opened_fresh_thesis_rebuild_no_candidate_selection",
                "judgment": "stage_open_planning_only_no_candidate_selection",
                "path": rel(STAGE277_BRIEF),
                "notes": f"opened_from={RUN_ID};seed_rows={len(seeds)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            },
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__stage276_closeout",
                "stage_id": STAGE276_ID,
                "run_id": RUN_ID,
                "subrun_id": "stage276_closeout",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Stage276 closeout(276단계 종료)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "stage_transition",
                "scoreboard_lane": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(STAGE276_CLOSEOUT),
                "primary_kpi": f"seed_rows={len(seeds)};survivor_watch_rows=0",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_stage_transition",
                "notes": f"target_stage={STAGE277_ID};valid_negative_boundary=Stage276.",
            },
            {
                "ledger_row_id": f"{STAGE277_OPEN_ID}__stage_open",
                "stage_id": STAGE277_ID,
                "run_id": STAGE277_OPEN_ID,
                "subrun_id": "stage_open",
                "parent_run_id": RUN_ID,
                "record_view": "Stage277 open(277단계 개시)",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "kpi_scope": "stage_open",
                "scoreboard_lane": "fresh_thesis_rebuild",
                "status": "opened_fresh_thesis_rebuild_no_candidate_selection",
                "judgment": "stage_open_planning_only_no_candidate_selection",
                "path": rel(STAGE277_BRIEF),
                "primary_kpi": f"fresh_thesis_seed_rows={len(seeds)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_stage_open",
                "notes": f"next_action={NEXT_ACTION}.",
            },
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        REVIEWS276 / "stage_run_ledger.csv",
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__stage276_closeout",
                "stage_id": STAGE276_ID,
                "run_id": RUN_ID,
                "view": "stage276_closeout_stage277_open",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "stage_transition",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "valid_negative_no_candidate_no_onnx",
                "report_path": rel(STAGE276_CLOSEOUT),
                "notes": f"target_stage={STAGE277_ID};seed_rows={len(seeds)}.",
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        STAGE277_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{STAGE277_OPEN_ID}__stage_open",
                "stage_id": STAGE277_ID,
                "run_id": STAGE277_OPEN_ID,
                "view": "stage277_open_fresh_thesis_rebuild",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "stage_open",
                "status": "opened_fresh_thesis_rebuild_no_candidate_selection",
                "judgment": "stage_open_planning_only_no_candidate_selection",
                "evidence_boundary": "stage_open_only_no_candidate_no_onnx",
                "report_path": rel(STAGE277_BRIEF),
                "notes": f"opened_from={RUN_ID};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "stage276_closeout_stage277_open_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE276_ID if str(path).startswith(str(STAGE276)) else STAGE277_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "Stage276 closeout and Stage277 open artifact.",
        }
        for path in outputs
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(seeds: Sequence[Mapping[str, Any]], failure_rows: Sequence[Mapping[str, Any]]) -> None:
    stage276_selection = io_path(SELECTED276).read_text(encoding="utf-8-sig")
    stage276_selection = replace_line_prefix(stage276_selection, "- stage_status(", "- stage_status(단계 상태): `closed_valid_negative_no_candidate_selection`")
    stage276_selection = replace_line_prefix(stage276_selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    stage276_selection = replace_line_prefix(stage276_selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    stage276_selection = replace_line_prefix(stage276_selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    stage276_selection = append_once(
        stage276_selection,
        "stage276_closeout_stage277",
        f"- stage276_closeout_stage277(276단계 종료/277단계 개시): `{rel(STAGE276_CLOSEOUT)}`",
    )
    write_md(SELECTED276, stage276_selection)

    review276 = io_path(REVIEWS276 / "review_index.md").read_text(encoding="utf-8-sig")
    review276 = append_once(
        review276,
        "stage276_closeout_stage277",
        "\n".join(
            [
                f"- stage276_closeout_stage277(276단계 종료/277단계 개시): `{rel(STAGE276_CLOSEOUT)}`",
                f"- stage276_to_stage277_decision(276->277 결정): `{rel(DECISION_DOC)}`",
                f"- run276E_manifest(276E 실행 목록): `{rel(RUN_MANIFEST)}`",
            ]
        ),
    )
    write_md(REVIEWS276 / "review_index.md", review276)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(", "- current_packet(현재 작업 묶음): `stage277_fresh_thesis_rebuild_after_aggressive_surface_failure_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{STAGE277_OPEN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE277_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{STAGE276_ID}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_rebuild_after_aggressive_surface_failure`")
    current = replace_line_prefix(current, "- status(", "- status(상태): `opened_fresh_thesis_rebuild_no_candidate_selection`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run276E_summary",
        (
            f"- run276E_summary(276E 요약): Stage276(276단계)을 valid negative(유효한 부정)로 닫고 Stage277(277단계)을 "
            f"fresh thesis rebuild(새 논제 재구성) seed(씨앗) `{len(seeds)}`개로 열었다. "
            f"Effect(효과): failure memory(실패 기억) `{len(failure_rows)}`개를 후보 보존이 아니라 새 thesis(논제) 입력으로 넘기며 "
            "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {STAGE277_OPEN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE277_ID}")
    focus = (
        "- >-\n"
        f"  Stage277(277단계) fresh thesis rebuild(새 논제 재구성) `{STAGE277_OPEN_ID}`. "
        f"Effect(효과): Stage276(276단계)의 failure memory(실패 기억) `{len(failure_rows)}`개에서 seed(씨앗) `{len(seeds)}`개를 열었고 "
        "selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage277(277단계) fresh thesis rebuild(새 논제 재구성)")
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run276E Stage276 closeout and Stage277 open(276E 276단계 종료와 277단계 개시)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): Stage277 fresh thesis seed(277단계 새 논제 씨앗) `{len(seeds)}`개를 열고 Stage276 failure memory(276단계 실패 기억) `{len(failure_rows)}`개를 입력으로 고정했다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = idea.replace(
        f"| `IDEA-ST277-FRESH-THESIS-REBUILD-AFTER-AGGRESSIVE-SURFACE-FAILURE` | `{OLD_STAGE277_ID}` |",
        f"| `IDEA-ST277-FRESH-THESIS-REBUILD-AFTER-AGGRESSIVE-SURFACE-FAILURE` | `{STAGE277_ID}` |",
    )
    idea = append_once(
        idea,
        "IDEA-ST277-FRESH-THESIS-REBUILD-AFTER-AGGRESSIVE-SURFACE-FAILURE",
        f"| `IDEA-ST277-FRESH-THESIS-REBUILD-AFTER-AGGRESSIVE-SURFACE-FAILURE` | `{STAGE277_ID}` | Stage276(276단계) failure memory(실패 기억)를 fresh thesis rebuild(새 논제 재구성)로 바꾼다. | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `opened_research_development_only` | seed rows(씨앗 행) `{len(seeds)}`; next_action(다음 행동) `{NEXT_ACTION}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)

    negative = io_path(NEGATIVE_REGISTER).read_text(encoding="utf-8-sig") if path_exists(NEGATIVE_REGISTER) else "# Negative Result Register(부정 결과 등록부)\n"
    negative = append_once(
        negative,
        "NEG-ST276-RUN276D-AGGRESSIVE-FRESH-SURFACE-FAILURE",
        (
            "| `NEG-ST276-RUN276D-AGGRESSIVE-FRESH-SURFACE-FAILURE` | `IDEA-ST276-AGGRESSIVE-FRESH-SURFACE-PROBE` | "
            "aggressive fresh surface(공격형 새 표면)가 ONNX-worthy candidate(온엑스화 가치 후보)로 이어질 수 있다 | "
            "run276D(276D 실행)에서 survivor watch(생존 관찰)가 `0`개였고 cp275A/cp275B/cp275D(275A/275B/275D 패키지)는 pf_too_thin/OOS negative/deep slice hole(수익 팩터 과소/표본외 음수/깊은 구간 구멍)로 실패했다 | "
            "weak session/month/chron late(약한 세션/월/시간 후반) 실패 기억은 Stage277(277단계) fresh thesis seed(새 논제 씨앗)로 보존한다 | "
            "새 feature/decision/risk surface(피처/판단/위험 표면)가 생기고 Tier A/Tier B(티어 A/티어 B) paired evidence(쌍 근거)가 닫힐 때만 재개한다 | "
            f"`{rel(STAGE276_CLOSEOUT)}` |"
        ),
    )
    write_md(NEGATIVE_REGISTER, negative)


def run() -> dict[str, Any]:
    must_exist(source_inputs())
    cleanup_old_long_stage277_path()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    review = review_result()
    seeds = seed_rows()
    failure_rows = copy_csv(SOURCE_FAILURE_MEMORY, FAILURE_MEMORY_RUN)
    negative_rows = copy_csv(SOURCE_NEGATIVE_SLICE, NEGATIVE_SLICE_RUN)
    variant_rows = copy_csv(SOURCE_VARIANT_SUMMARY, VARIANT_SUMMARY_RUN)
    write_csv(SEED_QUEUE_RUN, SEED_COLUMNS, seeds)
    write_csv(STAGE277_SEED_QUEUE, SEED_COLUMNS, seeds)
    write_csv(STAGE277_FAILURE_MEMORY, list(failure_rows[0].keys()) if failure_rows else ["empty"], failure_rows)
    write_csv(STAGE277_NEGATIVE_SLICE, list(negative_rows[0].keys()) if negative_rows else ["empty"], negative_rows)
    write_csv(STAGE277_VARIANT_SUMMARY, list(variant_rows[0].keys()) if variant_rows else ["empty"], variant_rows)

    write_stage_docs(created_at, seeds, failure_rows, negative_rows, variant_rows, review)
    write_handoff_manifest(created_at, seeds, failure_rows, negative_rows, review)
    write_receipts(seeds, review)

    outputs = [
        HANDOFF_MANIFEST,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        SEED_QUEUE_RUN,
        FAILURE_MEMORY_RUN,
        NEGATIVE_SLICE_RUN,
        VARIANT_SUMMARY_RUN,
        STAGE276_CLOSEOUT,
        DECISION_DOC,
        STAGE277_BRIEF,
        STAGE277_INPUTS,
        STAGE277_SEED_QUEUE,
        STAGE277_FAILURE_MEMORY,
        STAGE277_NEGATIVE_SLICE,
        STAGE277_VARIANT_SUMMARY,
        STAGE277_REVIEW_INDEX,
        SELECTED277,
        STAGE277_LEDGER,
    ]
    manifest = manifest_payload(created_at, outputs, seeds)
    write_json(RUN_MANIFEST, manifest)
    outputs.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, outputs, seeds)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    outputs.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, outputs, seeds)
    write_json(RUN_MANIFEST, manifest)

    update_registers(created_at, seeds, outputs)
    update_state_docs(seeds, failure_rows)

    return {
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "active_stage": STAGE277_ID,
        "stage277_open_id": STAGE277_OPEN_ID,
        "seed_rows": len(seeds),
        "failure_memory_rows": len(failure_rows),
        "negative_slice_rows": len(negative_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "closeout": rel(STAGE276_CLOSEOUT),
        "decision_doc": rel(DECISION_DOC),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
