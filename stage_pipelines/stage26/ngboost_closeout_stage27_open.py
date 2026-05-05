from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import io_path, json_ready
from stage_pipelines.stage26 import ngboost_distribution_runtime_probe as runtime_probe
from stage_pipelines.stage26 import ngboost_probabilistic_distribution_scout as scout


STAGE26_ID = scout.STAGE_ID
STAGE27_ID = "27_tail_model__quantile_boosting_risk_surface"
RUN20A_ID = scout.RUN_ID
RUN20B_ID = runtime_probe.RUN_ID
NEXT_RUN_ID = "run21A_quantile_boosting_tail_risk_surface_scout_v1"
PACKET_ID = "stage26_ngboost_closeout_v1"
JUDGMENT = "closed_inconclusive_ngboost_distribution_characteristics_exhausted"
BOUNDARY = "ngboost_characteristic_and_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"

ROOT = scout.ROOT
STAGE26_ROOT = ROOT / "stages" / STAGE26_ID
STAGE27_ROOT = ROOT / "stages" / STAGE27_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
CLOSEOUT_PACKET_PATH = STAGE26_ROOT / "03_reviews/stage26_closeout_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage26_ngboost_closeout_stage27_open.md"
WORKSPACE_STATE_PATH = scout.WORKSPACE_STATE_PATH
CURRENT_WORKING_STATE_PATH = scout.CURRENT_WORKING_STATE_PATH
GOAL_PLAN_PATH = scout.GOAL_PLAN_PATH
SELECTION_STATUS_PATH = scout.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = scout.REVIEW_INDEX_PATH


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return scout.rel(path)


def write_json(path: Path, payload: Any) -> None:
    scout.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    scout.write_md(path, text)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def active_branch() -> str:
    return subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()


def load_summaries() -> tuple[dict[str, Any], dict[str, Any]]:
    run20a = read_json(ROOT / "docs/agent_control/packets" / scout.PACKET_ID / "aggregate_summary.json")
    run20b = read_json(ROOT / "docs/agent_control/packets" / runtime_probe.PACKET_ID / "aggregate_summary.json")
    if run20b.get("external_verification_status") != "completed":
        raise RuntimeError("Stage26 closeout requires completed run20B runtime_probe evidence.")
    return run20a, run20b


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def replace_markdown_section(text: str, heading_prefix: str, new_section: str) -> str:
    start = text.find(heading_prefix)
    if start < 0:
        return text.rstrip() + "\n\n" + new_section.rstrip() + "\n"
    next_start = text.find("\n## ", start + 1)
    if next_start < 0:
        return text[:start] + new_section.rstrip() + "\n"
    return text[:start] + new_section.rstrip() + "\n\n" + text[next_start + 1 :]


def write_stage27_open() -> None:
    write_md(
        STAGE27_ROOT / "00_spec/stage_brief.md",
        f"""# Stage27 Quantile Boosting Tail Risk Surface(27단계 분위수 부스팅 꼬리 위험 표면)

## Core Question(핵심 질문)

Can quantile boosting(분위수 부스팅) expose tail-risk surface(꼬리 위험 표면), asymmetric loss(비대칭 손실), and risk-aware permission/abstention clues(위험 인식 허용/기권 단서) without inheriting Stage26(26단계) NGBoost(자연 그래디언트 부스팅) thresholds(임계값)?

효과(effect, 효과): Stage27(27단계)는 probability class shape(분류 확률 모양)가 아니라 return distribution tail(수익률 분포 꼬리)과 quantile spread(분위수 간격)를 독립 주제로 탐색한다.

## First Planned Run(첫 계획 실행)

`{NEXT_RUN_ID}`
""",
    )
    write_md(
        STAGE27_ROOT / "01_inputs/input_refs.md",
        f"""# Stage27 Input References(27단계 입력 참조)

- source data surface(원천 데이터 표면): audited 58-feature MT5 price-proxy model input(감사된 58개 피처 MT5 가격 대리 모델 입력)
- tier rule(티어 규칙): Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined/routed(Tier A+B 합산/라우팅)
- planned first run(계획된 첫 실행): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage26(26단계) selected variant(선택 변형), threshold(임계값), runtime score table(런타임 점수표)을 상속하지 않는다.
""",
    )
    write_md(
        STAGE27_ROOT / "03_reviews/review_index.md",
        f"""# Stage27 Review Index(27단계 검토 색인)

No reviewed run yet(아직 검토된 실행 없음).

효과(effect, 효과): 다음 작업은 `{NEXT_RUN_ID}`부터 기록한다.
""",
    )
    write_md(
        STAGE27_ROOT / "04_selected/selection_status.md",
        f"""# Stage27 Selection Status(27단계 선택 상태)

- stage(단계): `{STAGE27_ID}`
- status(상태): `opened_not_started`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage27(27단계)는 open-only(개방만) 상태이며 아직 결과 주장을 만들지 않는다.
""",
    )


def write_closeout(run20a: Mapping[str, Any], run20b: Mapping[str, Any]) -> None:
    validation = run20b.get("validation_routed", {})
    oos = run20b.get("oos_routed", {})
    selected_variant = run20a.get("selected_variant_id")
    normalized = run20b.get("kpi_management", {}).get("normalized_records")
    parser_errors = run20b.get("kpi_management", {}).get("parser_errors")
    write_md(
        CLOSEOUT_PACKET_PATH,
        f"""# Stage26 NGBoost Closeout Packet(26단계 NGBoost 마감 묶음)

## Judgment(판정)

- stage(단계): `{STAGE26_ID}`
- run range(실행 범위): `run20A-run20B`
- judgment(판정): `{JUDGMENT}`
- selected variant(선택 변형): `{selected_variant}`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage26(26단계)는 NGBoost(자연 그래디언트 부스팅)의 distributional uncertainty(분포 불확실성)와 MT5 handoff behavior(MT5 인계 행동)를 보존하고, micro-tuning(미세탐색) 없이 Stage27(27단계) topic pivot(주제 전환)으로 이동한다.

## Evidence(근거)

- Python scout(파이썬 탐색): `{RUN20A_ID}`, judgment(판정) `{run20a.get('judgment')}`
- MT5 runtime_probe(MT5 런타임 탐침): `{RUN20B_ID}`, judgment(판정) `{run20b.get('closure_judgment')}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{run20b.get('mt5_kpi_record_count')}`
- normalized records(정규화 기록): `{normalized}`
- parser errors(파서 오류): `{parser_errors}`
- validation routed net/PF/trades(검증 라우팅 순손익/수익 팩터/거래 수): `{validation.get('net_profit')}` / `{validation.get('profit_factor')}` / `{validation.get('trade_count')}`
- OOS routed net/PF/trades(표본외 라우팅 순손익/수익 팩터/거래 수): `{oos.get('net_profit')}` / `{oos.get('profit_factor')}` / `{oos.get('trade_count')}`

## Preserved Clues(보존 단서)

- NGBoost(자연 그래디언트 부스팅)는 entropy(엔트로피), nonflat confidence(비평탄 확신), direction bias(방향 편향)로 permission/abstention(허용/기권) 축을 보여줬다.
- selected variant(선택 변형) `{selected_variant}`는 Tier B compatible(Tier B 호환) core42 distribution surface(42개 핵심 피처 분포 표면)였다.
- MT5 runtime_probe(MT5 런타임 탐침)는 distilled score table(증류 점수표) 방식으로 completed(완료)되었다.

## Negative Memory(부정 기억)

- validation routed(검증 라우팅)는 손실이었고 OOS routed(표본외 라우팅)는 작은 표본이라 edge(거래 우위)로 해석하지 않는다.
- run20B(20B 실행)는 native NGBoost runtime(원본 NGBoost 런타임)이 아니라 distilled score-table handoff(증류 점수표 인계)다.
- high entropy(높은 엔트로피)가 많아 certainty model(확신 모델)로 쓰면 안 된다.

## Next Stage(다음 단계)

Open Stage27(27단계) `{STAGE27_ID}` as open-only(개방만). Next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.
""",
    )
    write_md(
        DECISION_PATH,
        f"""# Decision(결정): Stage26 Closeout And Stage27 Open(26단계 마감 및 27단계 개방)

Stage26(26단계) `{STAGE26_ID}`를 reviewed closeout(검토된 마감)으로 닫고 Stage27(27단계) `{STAGE27_ID}`를 open-only(개방만) 상태로 연다.

효과(effect, 효과): NGBoost(자연 그래디언트 부스팅)의 clue(단서)와 negative memory(부정 기억)는 보존하되, baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않고 quantile boosting(분위수 부스팅) topic pivot(주제 전환)으로 이동한다.

Next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.
""",
    )


def set_top_level_value(text: str, key: str, value: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(f"{key}: "):
            lines[index] = f"{key}: {value}"
            break
    else:
        lines.insert(0, f"{key}: {value}")
    return "\n".join(lines) + "\n"


def replace_current_focus_stage26_line(text: str) -> str:
    replacement = (
        f"- treat Stage 27 as opened_not_started after Stage26 NGBoost(자연 그래디언트 부스팅) "
        f"reviewed closeout(검토된 마감); next action is {NEXT_RUN_ID}, "
        "and no baseline, promotion, or runtime authority exists"
    )
    lines = text.splitlines()
    replaced = False
    for index, line in enumerate(lines):
        if line.startswith("- treat Stage 26 as active_run20B"):
            lines[index] = replacement
            replaced = True
            break
    if not replaced:
        for index, line in enumerate(lines):
            if line == "current_focus:":
                lines.insert(index + 1, replacement)
                break
    return "\n".join(lines) + "\n"


def update_workspace_state(branch: str, run20a: Mapping[str, Any], run20b: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = set_top_level_value(state, "active_branch", branch)
    state = set_top_level_value(state, "active_stage", STAGE27_ID)
    state = set_top_level_value(state, "current_run_id", "not_started")
    state = state.replace(
        "stage25_reviewed_closed_stage26_opened",
        "stage25_reviewed_closed_stage26_reviewed_closed_stage27_opened",
    )
    state = state.replace(
        "status: reviewed_closed_stage26_reviewed_closed_stage27_opened",
        "status: reviewed_closed_stage26_opened",
    )
    state = state.replace(
        "status: active_run20B_mt5_runtime_probe_blocked_after_attempt",
        "status: reviewed_closed_stage27_opened",
    )
    state = state.replace(
        "status: active_run20B_mt5_runtime_probe_completed",
        "status: reviewed_closed_stage27_opened",
    )
    state = replace_current_focus_stage26_line(state)

    model_block = f"""stage26_ngboost_model:
  stage_id: {STAGE26_ID}
  status: reviewed_closed_stage27_opened
  current_run_id: {RUN20B_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {run20a.get('selected_variant_id')}
  boundary: {BOUNDARY}
  judgment: {JUDGMENT}
  mt5_runtime_probe_status: completed_by_next_milestone_{RUN20B_ID}
  mt5_kpi_record_count: {run20b.get('mt5_kpi_record_count')}
  closeout_packet_path: {rel(CLOSEOUT_PACKET_PATH)}
  report_path: stages/{STAGE26_ID}/03_reviews/run20B_ngboost_distribution_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage26_ngboost_model:", model_block)
    state = state.replace(
        f"stage26_ngboost_run20A_structural_scout:\n  packet_id: {scout.PACKET_ID}\n  status: reviewed_structural_scout_completed\n  judgment: inconclusive_ngboost_probabilistic_distribution_scout_completed\n  current_run_id: {RUN20B_ID}",
        f"stage26_ngboost_run20A_structural_scout:\n  packet_id: {scout.PACKET_ID}\n  status: reviewed_structural_scout_completed\n  judgment: inconclusive_ngboost_probabilistic_distribution_scout_completed\n  current_run_id: {RUN20A_ID}",
        1,
    )
    closeout_block = f"""stage26_ngboost_closeout:
  packet_id: {PACKET_ID}
  status: reviewed_closed_stage27_opened
  judgment: {JUDGMENT}
  current_run_id: {RUN20B_ID}
  run_range: run20A-run20B
  selected_variant_id: {run20a.get('selected_variant_id')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  closeout_packet_path: {rel(CLOSEOUT_PACKET_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage26_ngboost_closeout:", closeout_block)
    stage27_block = f"""stage27_quantile_boosting_model:
  stage_id: {STAGE27_ID}
  status: opened_not_started
  current_run_id: not_started
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: topic_open_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  stage_brief_path: stages/{STAGE27_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE27_ID}/04_selected/selection_status.md
  next_action: {NEXT_RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage27_quantile_boosting_model:", stage27_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_goal_plan(branch: str) -> None:
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    plan = plan.replace(f"- active stage(활성 단계): `{STAGE26_ID}`", f"- active stage(활성 단계): `{STAGE27_ID}`", 1)
    plan = plan.replace(f"- current run(현재 실행): `{RUN20B_ID}`", "- current run(현재 실행): `not_started`", 1)
    plan = plan.replace("- active branch(활성 브랜치): `codex/stage26-ngboost-probabilistic`", f"- active branch(활성 브랜치): `{branch}`", 1)
    plan = plan.replace(f"- active stage folder(활성 단계 폴더): `stages/{STAGE26_ID}`", f"- active stage folder(활성 단계 폴더): `stages/{STAGE27_ID}`", 1)
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage26(26단계) `stage26_closeout_and_stage27_open_only`.",
        f"Current active milestone(현재 활성 마일스톤): Stage27(27단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
    )
    plan = plan.replace(
        "Current active milestone(현재 활성 마일스톤): Stage26(26단계) `repair_run20B_ngboost_runtime_probe_then_rerun_exact_attempts`.",
        f"Current active milestone(현재 활성 마일스톤): Stage27(27단계) `{NEXT_RUN_ID}` broad scout(넓은 탐색).",
    )

    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `stage26_closeout_stage27_open` completed(완료).
- active branch(활성 브랜치): `{branch}`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage27(27단계), `not_started`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE26_ID}/03_reviews`, `stages/{STAGE27_ID}/00_spec`, `stages/{STAGE27_ID}/01_inputs`, `stages/{STAGE27_ID}/03_reviews`, `stages/{STAGE27_ID}/04_selected`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): Stage26 closeout(26단계 마감), Stage27 open docs(27단계 개방 문서), current truth docs(현재 진실 문서), goal plan(목표 계획).
- active stage folder(활성 단계 폴더): `stages/{STAGE27_ID}`.
- current run id(현재 실행 ID): `not_started`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): previous Stage26 report(이전 26단계 보고서) `stages/{STAGE26_ID}/02_runs/{RUN20B_ID}/mt5/reports`; closeout report(마감 보고서) `{rel(CLOSEOUT_PACKET_PATH)}`.
- blocker(차단 사유): `none(없음)`.
- exact next action(정확한 다음 행동): `{NEXT_RUN_ID}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage27(27단계) quantile boosting(분위수 부스팅) broad scout(넓은 탐색)에서 시작한다.
"""
    plan = replace_markdown_section(plan, "## Latest Stop Resume State", resume)
    outcome = "- `2026-05-05`: Stage26(26단계) reviewed closeout(검토된 마감)을 완료하고 Stage27(27단계)를 open-only(개방만)로 열었다."
    if outcome not in plan:
        plan = plan.rstrip() + "\n" + outcome + "\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def update_text_docs(branch: str) -> None:
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage26 Selection Status(26단계 선택 상태)

- stage(단계): `{STAGE26_ID}`
- status(상태): `reviewed_closed_stage27_opened`
- selected variant(선택 변형): `v02_core42_distribution_surface`
- selected operating reference(선택 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`
- selected baseline(선택 기준선): `none(없음)`
- runtime authority(런타임 권위): `none(없음)`
- closeout packet(마감 묶음): `{rel(CLOSEOUT_PACKET_PATH)}`
- next action(다음 행동): `{NEXT_RUN_ID}`

효과(effect, 효과): Stage26(26단계)는 보존 단서와 부정 기억만 남기고 Stage27(27단계)로 이동한다.
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else ""
    line = f"- `stage26_closeout`: `{rel(CLOSEOUT_PACKET_PATH)}`\n"
    if "stage26_closeout" not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage26 Closeout / Stage27 Open(최신 26단계 마감 / 27단계 개방)

Stage26(26단계) NGBoost(자연 그래디언트 부스팅)를 reviewed closeout(검토된 마감)으로 닫고 Stage27(27단계) `{STAGE27_ID}`를 open-only(개방만) 상태로 열었다.

Result(결과): `{JUDGMENT}`. active branch(활성 브랜치): `{branch}`. next exact action(다음 정확한 행동): `{NEXT_RUN_ID}`.

효과(effect, 효과): NGBoost(자연 그래디언트 부스팅)의 단서와 부정 기억은 보존하되 baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않고 quantile boosting(분위수 부스팅) topic pivot(주제 전환)으로 이동한다.

"""
    if "## Latest Stage26 Closeout / Stage27 Open" not in current:
        io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")


def write_packet(run20a: Mapping[str, Any], run20b: Mapping[str, Any], branch: str, created_at: str) -> dict[str, Any]:
    summary = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE26_ID,
        "status": "reviewed_closed_stage27_opened",
        "judgment": JUDGMENT,
        "run_range": "run20A-run20B",
        "selected_variant_id": run20a.get("selected_variant_id"),
        "selected_operating_reference": None,
        "selected_promotion_candidate": None,
        "selected_baseline": None,
        "runtime_authority": None,
        "boundary": BOUNDARY,
        "mt5_runtime_probe_status": run20b.get("external_verification_status"),
        "mt5_kpi_record_count": run20b.get("mt5_kpi_record_count"),
        "validation_routed": run20b.get("validation_routed"),
        "oos_routed": run20b.get("oos_routed"),
        "closeout_packet_path": rel(CLOSEOUT_PACKET_PATH),
        "decision_path": rel(DECISION_PATH),
        "next_stage_id": STAGE27_ID,
        "next_action": NEXT_RUN_ID,
        "active_branch": branch,
        "created_at_utc": created_at,
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
    }
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    write_json(PACKET_ROOT / "skill_receipts.json", [
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "skill": "obsidian-result-judgment", "status": "executed", "judgment": JUDGMENT, "boundary": BOUNDARY},
        {"packet_id": PACKET_ID, "created_at_utc": created_at, "skill": "obsidian-runtime-parity", "status": "executed", "runtime_probe": RUN20B_ID, "claim_boundary": BOUNDARY},
    ])
    write_json(PACKET_ROOT / "final_claim_guard.json", {
        "packet_id": PACKET_ID,
        "allowed_claim": "Stage26 NGBoost explored and closed inconclusive; Stage27 opened.",
        "forbidden_claims": summary["forbidden_claims"],
        "runtime_authority": None,
    })
    return summary


def run(_: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    branch = active_branch()
    run20a, run20b = load_summaries()
    write_stage27_open()
    write_closeout(run20a, run20b)
    update_workspace_state(branch, run20a, run20b)
    update_goal_plan(branch)
    update_text_docs(branch)
    summary = write_packet(run20a, run20b, branch, created_at)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description="Close Stage26 NGBoost and open Stage27 quantile boosting.")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    run(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
