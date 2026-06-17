from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path"
RUN_ID = "frontier74D_pre_mt5_grok_microburst_negative_control_runtime_probe_v1"
PARENT_RUN_ID = "frontier74C_microburst_label_feature_repair_proxy_v1"
NEXT_RUN_ID = "frontier74E_mt5_microburst_negative_control_runtime_probe_v1"
STATUS = "pre_mt5_grok_review_accepted_no_authority"
JUDGMENT = "negative_control_runtime_probe_accepted_no_authority"
CLAIM_BOUNDARY = (
    "pre_mt5_review_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f74d_pre_mt5_microburst_negative_control_runtime_probe"
GROK_PROMPT = GROK_PACKET / "prompts/f74d_pre_mt5_microburst_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"
F74C_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f74c_summary.json"

ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    write_text(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2))


def write_md(path: Path, lines: list[str]) -> None:
    write_text(path, "\n".join(lines))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.rstrip())


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        raise FileNotFoundError(f"ledger header missing: {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def required_inputs() -> list[Path]:
    return [GROK_PROMPT, GROK_CLEAN, GROK_METADATA, F74C_SUMMARY, ALPHA_LEDGER, RUN_REGISTRY]


def report_lines(created_at: str, prompt_hash: str, output_hash: str) -> list[str]:
    return [
        "# Frontier74D Pre-MT5 Grok Review(F74D MT5 전 Grok 검토)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Grok Classification(Grok 분류)",
        "",
        "- advice_classification(조언 분류): `accepted(수용)`",
        "- accepted direction(수용 방향): run a mandatory negative-control MT5 Runtime Probe(필수 부정 대조 MT5 런타임 탐침) before closeout or more repair(마감 또는 추가 수리 전).",
        "- drift risk(드리프트 위험): density quota backdoor(밀도 할당 우회) and indirect promotion(간접 승격) risk.",
        "- probe design requirement(탐침 설계 요구): frozen negative-control identity(고정 부정 대조 정체성) for `f74c_1212` and side-by-side proxy vs MT5 KPI(프록시 대 MT5 KPI 나란히 비교).",
        "",
        "## Evidence Identity(근거 정체성)",
        "",
        f"- packet(묶음): `{rel(GROK_PACKET)}`",
        f"- prompt(프롬프트): `{rel(GROK_PROMPT)}`, sha256 `{prompt_hash}`",
        f"- output(출력): `{rel(GROK_CLEAN)}`, sha256 `{output_hash}`",
    ]


def receipt_lines(created_at: str, prompt_hash: str, output_hash: str) -> list[str]:
    metadata = json.loads(io_path(GROK_METADATA).read_text(encoding="utf-8"))
    return [
        "# F74D Grok Receipt(F74D Grok 영수증)",
        "",
        f"- created_at_utc(생성 시각): `{created_at}`",
        "- trigger_reason(트리거 이유): MT5 Runtime Probe(MT5 런타임 탐침)는 주요 검증이므로 Grok review(그록 검토)가 필요하다.",
        "- review_size(검토 크기): `medium(중간)`",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{prompt_hash}`",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{output_hash}`",
        f"- wrapper_success(래퍼 성공): `{metadata.get('success')}`; returncode(반환 코드): `{metadata.get('returncode')}`",
        "- advice_classification(조언 분류): `accepted(수용)`",
        "- local_verification(로컬 검증): prompt/output files(프롬프트/출력 파일), metadata(메타데이터), and F74C summary(F74C 요약) exist locally(로컬 존재).",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        f"- final_codex_direction(최종 Codex 방향): run `{NEXT_RUN_ID}` as negative-control runtime probe(부정 대조 런타임 탐침).",
    ]


def gate_lines(created_at: str) -> list[str]:
    return [
        "# F74D Required Gate Coverage Audit(F74D 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
        "| pre-MT5 Grok review(MT5 전 Grok 검토) | `pass(통과)` | advice accepted(조언 수용). |",
        "| negative-control boundary(부정 대조 경계) | `pass(통과)` | F74C no-scout state is preserved; no positive claim(F74C 탐색 단서 없음 상태 보존, 긍정 주장 없음). |",
        "| final claim guard(최종 주장 보호) | `pass(통과)` | no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). |",
    ]


def update_ledgers(created_at: str) -> None:
    report = REVIEWS_ROOT / "frontier74D_pre_mt5_grok_negative_control_runtime_probe_report.md"
    manifest = RUN_ROOT / "run_manifest.json"
    audit = REVIEWS_ROOT / "required_gate_coverage_audit_f74d.md"
    row = {
        "ledger_row_id": f"{RUN_ID}__pre_mt5_grok",
        "row_id": f"{RUN_ID}__pre_mt5_grok",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "pre_mt5_review(MT5 전 검토)",
        "tier_scope": "Tier A separate; Tier B missing_required; Tier A+B out_of_scope_by_claim",
        "kpi_scope": "external_review_packet(외부 검토 묶음)",
        "scoreboard_lane": "runtime_probe_precheck(런타임 탐침 사전 점검)",
        "status": STATUS,
        "result_status": STATUS,
        "judgment": JUDGMENT,
        "result_judgment": JUDGMENT,
        "path": rel(report),
        "report_path": rel(report),
        "primary_report": rel(report),
        "primary_artifact": rel(manifest),
        "output_path": rel(manifest),
        "result_path": rel(report),
        "primary_kpi": "grok=accepted;target=f74c_1212",
        "guardrail_kpi": "negative_control_no_authority",
        "external_verification_status": "pre_mt5_review_completed(MT5 전 검토 완료)",
        "notes": "F74D Grok accepted negative-control MT5 Runtime Probe(F74D Grok이 부정 대조 MT5 런타임 탐침을 수용).",
        "run_number": "frontier74D",
        "date": created_at[:10],
        "run_date": created_at[:10],
        "decision": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "rows": 1,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created_at,
        "required_gate_audit": rel(audit),
        "gate_audit_path": rel(audit),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "run_type": "negative_control_runtime_probe_precheck(부정 대조 런타임 탐침 사전 점검)",
        "input_run_id": PARENT_RUN_ID,
        "question": "Should F74 run a mandatory negative-control MT5 Runtime Probe?(F74가 필수 부정 대조 MT5 런타임 탐침을 실행해야 하나?)",
        "evidence_boundary": "pre_mt5_review_only_no_runtime_yet(MT5 전 검토 전용, 런타임 아직 없음)",
    }
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers() -> None:
    marker = "<!-- frontier74D_pre_mt5_grok_negative_control_runtime_probe_v1 -->"
    block = f"""<!-- frontier74D_pre_mt5_grok_negative_control_runtime_probe_v1 -->
- `{RUN_ID}` recorded pre-MT5 Grok review(MT5 전 Grok 검토). Result(결과): `accepted(수용)` for mandatory negative-control MT5 Runtime Probe(필수 부정 대조 MT5 런타임 탐침) using `f74c_1212`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state(created_at: str) -> None:
    lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f74_pre_mt5_grok_accepted_runtime_probe_next",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f73_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F74D pre-MT5 Grok review(MT5 전 Grok 검토)를 기록했다."',
        '  - "Effect(효과): 다음 실행을 mandatory negative-control MT5 Runtime Probe(필수 부정 대조 MT5 런타임 탐침)로 고정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    write_text(WORKSPACE_STATE, "\n".join(lines))
    write_md(
        SELECTED_ROOT / "selection_status.md",
        [
            "# F74 Selection Status(F74 선택 상태)",
            "",
            f"- stage(단계): `{STAGE_ID}`",
            f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
            f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
            f"- status(상태): `{STATUS}`",
            f"- judgment(판정): `{JUDGMENT}`",
            "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
            "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
            "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
            "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
            "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
            f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`",
        ],
    )
    write_md(
        CURRENT_WORKING_STATE,
        [
            "# Current Working State(현재 작업 상태)",
            "",
            f"Updated(갱신): {created_at}",
            "",
            f"Active stage(활성 단계): `{STAGE_ID}`",
            f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "",
            "## Current Truth(현재 진실)",
            "",
            "Action(행동): F74D pre-MT5 Grok review(MT5 전 Grok 검토)를 기록했다.",
            "",
            f"Effect(효과): 다음 실행을 `{NEXT_RUN_ID}`로 설정했다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F74D required material missing: {missing}")
    created_at = utc_now()
    prompt_hash = sha256(GROK_PROMPT)
    output_hash = sha256(GROK_CLEAN)
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "grok_packet": rel(GROK_PACKET),
        "grok_prompt_hash": prompt_hash,
        "grok_output_hash": output_hash,
    }
    write_json(RUN_ROOT / "run_manifest.json", payload)
    write_json(RUN_ROOT / "f74d_pre_mt5_grok_summary.json", payload)
    write_md(REVIEWS_ROOT / "frontier74D_pre_mt5_grok_negative_control_runtime_probe_report.md", report_lines(created_at, prompt_hash, output_hash))
    write_md(REVIEWS_ROOT / "grok_pre_mt5_negative_control_runtime_probe_receipt.md", receipt_lines(created_at, prompt_hash, output_hash))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f74d.md", gate_lines(created_at))
    update_ledgers(created_at)
    update_registers()
    update_state(created_at)
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
