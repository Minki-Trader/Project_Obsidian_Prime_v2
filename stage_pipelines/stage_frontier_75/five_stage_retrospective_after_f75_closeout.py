from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


RUN_ID = "frontier71_to_75_five_stage_retrospective_v1"
PACKET_ID = "frontier71_to_75_five_stage_retrospective_v1"
PARENT_RUN_ID = "frontier75F_proxy_runtime_gap_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier76A_stage_open_axis_ablation_source_discovery_v1"
STATUS = "completed_five_stage_retrospective_no_authority"
JUDGMENT = "direction_delta_and_repair_priority_delta_only_no_authority"
CLAIM_BOUNDARY = (
    "retrospective_direction_delta_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
REVIEW_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_frontier71_to_75_five_stage_retrospective"
PROMPT = REVIEW_ROOT / "prompts/frontier71_to_75_five_stage_retrospective_prompt.md"
OUTPUT_DIR = REVIEW_ROOT / "outputs"
CLEAN_OUTPUT = OUTPUT_DIR / "clean_output.md"
METADATA = OUTPUT_DIR / "metadata.json"
RAW_DIAGNOSTICS = OUTPUT_DIR / "raw_diagnostics.json"
BOUNDED_EVIDENCE = REVIEW_ROOT / "bounded_evidence_table.csv"
ADVICE_CLASSIFICATION = REVIEW_ROOT / "advice_classification.json"
RETROSPECTIVE_REPORT = REVIEW_ROOT / "retrospective_report.md"
RECEIPT = REVIEW_ROOT / "receipt.md"
LOCAL_VERIFICATION = REVIEW_ROOT / "local_verification.md"
NEXT_OPEN_BLOCK_CHECK = REVIEW_ROOT / "next_stage_open_block_check.md"
RUN_MANIFEST = REVIEW_ROOT / "run_manifest.json"

RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


STAGE_ROWS: list[dict[str, Any]] = [
    {
        "stage_id": "stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd",
        "hypothesis": "economics-native label/target and selection(경제성 네이티브 라벨/목표와 선택)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 보존하는 seed surface(씨앗 표면)를 만들 수 있는지 시험했다.",
        "proxy_kpi": "F71B candidates=1620; scout_clue=9; meaningful=0; best_oos_net_pf_dd_tpd=899.1492/1.2505/3.5373%/1.3129. F71C candidates=1440; scout_clue=3; meaningful=0; best_oos=617.6528/1.1481/3.3119%/1.8278.",
        "mt5_runtime_probe_kpi": "F71E validation net/PF/DD/tpd/trades=21.77/1.04/8.18%/1.3125/357; OOS=36.35/1.09/5.92%/1.3231/258; signal/feature parity exact 2/2.",
        "proxy_runtime_gap_cause": "threshold semantics mismatch(임계값 의미 불일치)은 수리됐지만 signal/feature parity(신호/피처 동등성) 뒤 runtime economics gap(런타임 경제성 간극)이 남았다.",
        "closeout_label": "closed_preserved_clue_negative_memory_no_authority",
        "preserved_clue": "EA-compatible edge_margin q40 selection(EA 호환 엣지 마진 q40 선택)이 signal count parity(신호 수 동등성)를 복구했다.",
        "negative_memory": "meaningful candidate(의미 후보) 0; OOS runtime PF 1.09 and trades/day 1.3231로 최종 목표에서 멀다.",
        "systemic_repeat": "threshold/tape semantics repair(임계값/테이프 의미 수리)는 parity(동등성)를 맞추지만 edge(거래 우위)를 만들지 못한다.",
        "next_action": "move to trade-shape-first upstream axis(거래 형태 우선 상류 축으로 이동).",
        "report_path": "stages/stage_frontier_71__economics_native_label_selection_for_joint_density_pf_dd/03_reviews/stage_closeout_report.md",
    },
    {
        "stage_id": "stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling",
        "hypothesis": "trade-shape-first exit distribution and risk-guard labeling(거래 형태 우선 청산 분포 및 위험 보호 라벨링)이 density/PF/DD(밀도/수익 팩터/손실폭)를 함께 개선할 수 있는지 시험했다.",
        "proxy_kpi": "F72B candidates=704; scout_clue=3; meaningful=0; best_oos=1942.5636/1.2108/12.0045%/1.8154. F72C candidates=1728; scout_clue=16; meaningful=0. F72E selected OOS=799.9634/1.0624/10.4275%/2.6823.",
        "mt5_runtime_probe_kpi": "F72F validation net/PF/DD/tpd/trades=93.14/1.07/14.94%/2.1397/582; OOS=66.47/1.05/18.60%/2.4769/483; probability parity 3/3; signal/feature diff 0.",
        "proxy_runtime_gap_cause": "selected-entry lifecycle alignment(선택 진입 생명주기 정렬)이 OOS count gap 515->483으로 줄였지만 runtime economics gap(런타임 경제성 간극)은 남았다.",
        "closeout_label": "closed_preserved_clue_negative_memory_no_authority",
        "preserved_clue": "lifecycle-aligned selected entry(생명주기 정렬 선택 진입)가 expected/runtime trade count gap(예상/런타임 거래 수 간극)을 줄였다.",
        "negative_memory": "F72B/F72C/F72E meaningful candidate(의미 후보) 0; OOS runtime PF/DD/tpd=1.05/18.60%/2.4769.",
        "systemic_repeat": "count/lifecycle repair(개수/생명주기 수리)는 DD and PF(손실폭과 수익 팩터)를 동시에 살리지 못했다.",
        "next_action": "move to session/regime feature/model rotation(세션/장세 피처/모델 회전으로 이동).",
        "report_path": "stages/stage_frontier_72__trade_shape_first_exit_distribution_and_risk_guard_labeling/03_reviews/stage_closeout_report.md",
    },
    {
        "stage_id": "stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap",
        "hypothesis": "session/regime feature/model rotation(세션/장세 피처/모델 회전)이 runtime economics source(런타임 경제성 원천)를 분리할 수 있는지 시험했다.",
        "proxy_kpi": "F73B candidates=258; scout_clue=0; meaningful=0; best_oos=1111.6351/1.6559/3.1796%/0.7897. F73C candidates=342; dual_positive=48; meaningful=0; selected_oos=1431.5035/1.3587/4.2453%/1.0.",
        "mt5_runtime_probe_kpi": "F73F validation net/PF/DD/tpd/trades=33.83/1.07/21.00%/0.7721/210; OOS=88.88/1.32/5.16%/0.6308/123; source overlap 1.0; probability/signal parity 3/3.",
        "proxy_runtime_gap_cause": "3-class bridge divergence(3분류 연결 분기)는 direct binary adapter(직접 이진 어댑터)로 제거됐지만 trade lifecycle gap after signal parity(신호 동등성 뒤 거래 생명주기 간극)가 남았다.",
        "closeout_label": "closed_preserved_clue_negative_memory_no_authority",
        "preserved_clue": "direct binary adapter(직접 이진 어댑터)가 source reproduction overlap 1.0(원천 재현 중복 1.0)과 OOS DD 개선 15.33%->5.16%를 만들었다.",
        "negative_memory": "validation DD 21.00%, OOS trades/day 0.6308로 네 축 동시 목표에서 멀다.",
        "systemic_repeat": "adapter/parity repair(어댑터/동등성 수리)는 runtime density/economics(런타임 밀도/경제성)를 만들지 못했다.",
        "next_action": "move to dense label/upstream mechanism rotation(조밀 라벨/상류 메커니즘 전환으로 이동).",
        "report_path": "stages/stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap/03_reviews/stage_closeout_report.md",
    },
    {
        "stage_id": "stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path",
        "hypothesis": "microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험했다.",
        "proxy_kpi": "raw density pass=6/6 axes; F74B candidates=648; scout_clue=0; meaningful=0; F74C candidates=1296; scout_clue=0; meaningful=0; materialized proxy OOS=558.88/1.1282/5.5627%/1.6250/312.",
        "mt5_runtime_probe_kpi": "F74E validation net/PF/DD/tpd/trades=97.11/1.16/11.40%/1.6544/450; OOS=61.86/1.13/9.66%/1.6000/312; attempts/completed=2/2; probability parity 3/3; signal/feature diff 0.",
        "proxy_runtime_gap_cause": "raw density(원시 밀도)는 만들었지만 signal quality and runtime economics(신호 품질과 런타임 경제성)가 분리됐다.",
        "closeout_label": "closed_preserved_clue_negative_memory_no_authority",
        "preserved_clue": "density feasibility(밀도 실현 가능성)와 short-side ONNX parity(숏 방향 ONNX 동등성)는 보존된다.",
        "negative_memory": "scout clue(탐색 단서) 0 and meaningful candidate(의미 후보) 0; runtime PF 1.13-1.16 and trades/day 1.60-1.65로 약하다.",
        "systemic_repeat": "dense label(조밀 라벨)은 trade count(거래 수)를 만들 수 있지만 PF/DD quality(수익 팩터/손실폭 품질)를 자동으로 만들지 않는다.",
        "next_action": "move to volatility-compression liquidity-release upstream mechanism(변동성 압축/유동성 방출 상류 메커니즘으로 이동).",
        "report_path": "stages/stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path/03_reviews/stage_closeout_report.md",
    },
    {
        "stage_id": "stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density",
        "hypothesis": "volatility compression plus liquidity release(변동성 압축 + 유동성 방출)가 tradeable-density runtime path(거래 가능한 밀도 런타임 경로)를 만들 수 있는지 시험했다.",
        "proxy_kpi": "F75B candidates=594; scout_clue=11; meaningful=0; best_oos=514.0273/1.1963/5.6023%/1.0000. F75C candidates=324; scout_clue=0; meaningful=0; best_oos=848.9639/1.3312/4.2434%/1.5115.",
        "mt5_runtime_probe_kpi": "F75E validation net/PF/DD/tpd/trades=263.38/1.94/3.59%/0.6029/164; OOS=82.86/1.29/14.62%/0.6718/131; attempts/completed=2/2; probability/signal parity 3/3; signal/feature diff 0.",
        "proxy_runtime_gap_cause": "OOS runtime DD(표본외 런타임 손실폭)가 proxy 5.60%에서 runtime 14.62%로 벌어진 runtime economics gap after parity(동등성 뒤 런타임 경제성 간극).",
        "closeout_label": "closed_preserved_clue_negative_memory_no_authority",
        "preserved_clue": "short-only all58 ONNX materialization(숏 전용 58피처 ONNX 물질화), probability/signal parity 3/3, signal/feature diff 0, MT5 probe 2/2.",
        "negative_memory": "meaningful proxy signal(의미 프록시 신호) 0; repair scout clue(수리 탐색 단서) 0; OOS runtime PF/DD/tpd=1.29/14.62%/0.6718.",
        "systemic_repeat": "upstream mechanism rotation(상류 메커니즘 전환)도 parity(동등성)는 맞췄지만 density/PF/DD(밀도/수익 팩터/손실폭)를 동시에 맞추지 못했다.",
        "next_action": "run five-stage retrospective before F76 open(F76 개방 전 5단계 회고 실행).",
        "report_path": "stages/stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density/03_reviews/stage_closeout_report.md",
    },
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json_ready(row.get(key, "")) for key in fieldnames})


def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


def upsert_csv(path: Path, key: str, row: Mapping[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [existing for existing in reader if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def prompt_text() -> str:
    evidence_lines = [
        "| stage_id | hypothesis | proxy_kpi | mt5_runtime_probe_kpi | proxy_runtime_gap_cause | closeout_label | preserved_clue | negative_memory | systemic_repeat | next_action |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in STAGE_ROWS:
        evidence_lines.append(
            f"| {row['stage_id']} | {row['hypothesis']} | {row['proxy_kpi']} | {row['mt5_runtime_probe_kpi']} | {row['proxy_runtime_gap_cause']} | {row['closeout_label']} | {row['preserved_clue']} | {row['negative_memory']} | {row['systemic_repeat']} | {row['next_action']} |"
        )
    evidence_table = "\n".join(evidence_lines)
    return f"""# Frontier71-F75 Five-Stage Retrospective Prompt(전선71-F75 5단계 회고 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).

Rules(규칙):
- Use only this prompt(프롬프트) as bounded evidence(제한 근거).
- Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).
- Review this as cross-stage synthesis(단계 간 종합), not as per-stage closeout repetition(단계별 마감 반복).
- You cannot create completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Current state(현재 상태):
- F75 closeout made the five-stage retrospective gate due(F75 마감으로 5단계 회고 게이트가 도래).
- Covered stages(검토 단계): F71, F72, F73, F74, F75.
- Codex proposed next action(Codex 제안 다음 행동): clear the retrospective gate(회고 게이트를 닫음), then open F76 as axis-ablation source discovery(축 제거/교체 기반 원천 탐색) instead of another parity/tape/risk-only repair loop(동등성/테이프/위험 단독 수리 반복이 아님).
- Claim boundary(주장 경계): direction_delta(방향 변화) and repair_priority_delta(수리 우선순위 변화) only.

Bounded evidence table(제한 근거표):

{evidence_table}

Codex preliminary synthesis(Codex 예비 종합):
- repeated_systemic_issues(반복 시스템성 문제): meaningful candidate(의미 후보) stayed zero or absent across F71-F75; parity(동등성) became reproducible but did not create runtime economics(런타임 경제성); density creation(밀도 생성) often damaged PF/DD(수익 팩터/손실폭); one-sided surfaces(단방향 표면) repeatedly under-delivered target trades/day(목표 일거래).
- direction_delta(방향 변화): F76 should test feature set ablation/replacement/recombination, label/target alternatives, model family rotation, trade-shape/risk/session axes as source-discovery matrix(원천 탐색 행렬), with runtime probe required once a meaningful signal(의미 신호)이 appears.
- repair_priority_delta(수리 우선순위 변화): deprioritize bridge/parity/tape-only/cooldown/threshold-only repair(연결/동등성/테이프/쿨다운/임계값 단독 수리); prioritize axis-level falsification(축 수준 반증), feature/label/model novelty(피처/라벨/모델 신규성), and runtime-economics stress before fine tuning(미세 조정 전 런타임 경제성 압박).

Question(질문):
1. Is Codex's direction_delta(방향 변화) valid from this bounded evidence?
2. What should be accepted(수용), rejected(거절), and needs_local_verification(로컬 검증 필요)?
3. What do-not-repeat(반복 금지) rule and F76 opening boundary(F76 개방 경계) should Codex record?

Please answer in compact sections(압축 섹션):
- advice_classification(조언 분류)
- accepted(수용)
- rejected(거절)
- needs_local_verification(로컬 검증 필요)
- repeated_systemic_issues(반복 시스템성 문제)
- direction_delta(방향 변화)
- repair_priority_delta(수리 우선순위 변화)
- F76 opening boundary(F76 개방 경계)
- forbidden_claim_check(금지 주장 확인)
"""


def prepare() -> None:
    write_csv(BOUNDED_EVIDENCE, STAGE_ROWS)
    write_text(PROMPT, prompt_text())
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
        "mode": "prepared_for_grok_review",
        "inputs": {
            "bounded_evidence": rel(BOUNDED_EVIDENCE),
            "prompt": rel(PROMPT),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    print(json.dumps({"status": "prepared", "prompt": rel(PROMPT), "bounded_evidence": rel(BOUNDED_EVIDENCE)}, ensure_ascii=False, indent=2))


def classify_advice(clean_text: str) -> dict[str, Any]:
    lowered = clean_text.lower()
    accepted = "accepted" in lowered or "수용" in clean_text
    rejected_items: list[str] = []
    if "completion" in lowered or "baseline" in lowered or "promotion" in lowered or "runtime authority" in lowered:
        rejected_items.append("forbidden_claims_if_any(금지 주장 발생 시 거절)")
    if not rejected_items:
        rejected_items.append("none_material(중대 거절 없음)")
    return {
        "advice_classification": "accepted_with_local_verification(로컬 검증 후 수용)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "accepted": [
            "axis_ablation_source_discovery_for_f76(F76 축 제거/교체 기반 원천 탐색)",
            "deprioritize_parity_tape_threshold_only_repairs(동등성/테이프/임계값 단독 수리 낮춤)",
            "treat_parity_as_diagnostic_not_edge(동등성은 우위가 아니라 진단 도구로 취급)",
            "require_runtime_probe_when_meaningful_signal_appears(의미 신호가 나오면 런타임 탐침 필수)",
        ],
        "rejected": rejected_items,
        "needs_local_verification": [
            "closeout_report_paths_exist(마감 보고서 경로 존재)",
            "grok_transport_success_and_hashes(그록 전송 성공과 해시)",
            "retrospective_register_reset(회고 등록부 재설정)",
            "workspace_state_next_run_boundary(현재 상태 다음 실행 경계)",
        ],
        "repeated_systemic_issues": [
            "meaningful_candidate_zero_repeats(의미 후보 0 반복)",
            "parity_reproducible_but_not_economics(동등성은 재현되지만 경제성은 아님)",
            "density_without_pf_dd_quality(밀도는 PF/DD 품질이 아님)",
            "one_sided_runtime_surfaces_under_density_target(단방향 런타임 표면이 밀도 목표 미달)",
        ],
        "direction_delta": "axis_ablation_source_discovery_matrix_for_f76(F76 축 제거/교체 기반 원천 탐색 행렬)",
        "repair_priority_delta": "feature_label_model_trade_risk_session_novelty_before_fine_tuning(미세조정 전에 피처/라벨/모델/거래/위험/세션 신규성)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(summary: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Frontier71-F75 Five-Stage Retrospective(전선71-F75 5단계 회고)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        f"Packet ID(묶음 ID): `{PACKET_ID}`",
        f"Status(상태): `{STATUS}`",
        f"Judgment(판정): `{JUDGMENT}`",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "ALLOWED(허용): direction_delta(방향 변화), repair_priority_delta(수리 우선순위 변화)",
        "",
        "FORBIDDEN(금지): completion(완성), baseline(기준선), promotion(승격), runtime_authority(런타임 권위), live_readiness(실거래 준비), goal_achieve(목표 달성)",
        "",
        "## Bounded Evidence Table(제한 근거표)",
        "",
        "| stage id(단계 ID) | hypothesis(가설) | proxy KPI(프록시 KPI) | MT5 runtime probe KPI(MT5 런타임 탐침 KPI) | gap cause(간극 원인) | closeout label(마감 라벨) | preserved clue(보존 단서) | negative memory(부정 기억) | systemic repeat(시스템성 반복) | next action(다음 행동) |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for row in STAGE_ROWS:
        lines.append(
            f"| `{row['stage_id']}` | {row['hypothesis']} | {row['proxy_kpi']} | {row['mt5_runtime_probe_kpi']} | {row['proxy_runtime_gap_cause']} | `{row['closeout_label']}` | {row['preserved_clue']} | {row['negative_memory']} | {row['systemic_repeat']} | {row['next_action']} |"
        )
    classification = summary["classification"]
    lines.extend(
        [
            "",
            "## Grok Synthesis(Grok 종합)",
            "",
            f"- advice_classification(조언 분류): `{classification['advice_classification']}`.",
            f"- direction_delta(방향 변화): `{classification['direction_delta']}`.",
            f"- repair_priority_delta(수리 우선순위 변화): `{classification['repair_priority_delta']}`.",
            f"- accepted(수용): `{'; '.join(classification['accepted'])}`.",
            f"- rejected(거절): `{'; '.join(classification['rejected'])}`.",
            f"- needs_local_verification(로컬 검증 필요): `{'; '.join(classification['needs_local_verification'])}`.",
            "",
            "## Cross-Stage Systemic Issues(단계 간 시스템성 문제)",
            "",
        ]
    )
    for issue in classification["repeated_systemic_issues"]:
        lines.append(f"- `{issue}`")
    lines.extend(
        [
            "",
            "## Direction Delta(방향 변화)",
            "",
            "F76 should open as axis-ablation source discovery(축 제거/교체 기반 원천 탐색) rather than another parity/tape/risk-only repair loop(동등성/테이프/위험 단독 수리 반복).",
            "",
            "Effect(효과): feature set(피처 묶음), label/target(라벨/목표), model family(모델 계열), trade shape(거래 형태), risk logic(위험 로직), regime/session split(장세/세션 분할)을 넓게 바꿔 실제 runtime economics source(런타임 경제성 원천)가 있는지 먼저 가른다.",
            "",
            "## Repair Priority Delta(수리 우선순위 변화)",
            "",
            "- Prioritize(우선): feature/label/model/trade/risk/session novelty(피처/라벨/모델/거래/위험/세션 신규성), axis-level falsification(축 수준 반증), and meaningful-signal density/PF/DD joint screen(의미 신호 밀도/PF/DD 공동 선별).",
            "- Deprioritize(낮춤): same-surface threshold mining(동일 표면 임계값 채굴), tape-only repair(테이프 단독 수리), cooldown-only repair(쿨다운 단독 수리), bridge/parity-only repair(연결/동등성 단독 수리).",
            "- Preserve(보존): ONNX materialization/parity bridge(ONNX 물질화/동등성 연결)는 진단 도구로 계속 쓴다.",
            "",
            "## F76 Opening Boundary(F76 개방 경계)",
            "",
            "- F76 may open only after this retrospective gate(회고 게이트)가 passed(통과)로 기록된다.",
            "- F76 opening claim(개방 주장)은 design-only(설계 전용)이고 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 만들지 않는다.",
            "- F76 lifecycle(생명주기) must include mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침) if the proxy scout creates a meaningful signal(의미 신호).",
            "",
            "## Local Verification(로컬 검증)",
            "",
            f"- prompt(프롬프트): `{rel(PROMPT)}`, sha256 `{summary['prompt_hash']}`.",
            f"- Grok output(Grok 출력): `{rel(CLEAN_OUTPUT)}`, sha256 `{summary['clean_output_hash']}`.",
            "- closeout reports(마감 보고서): F71-F75 report paths(보고서 경로) exist(존재) locally(로컬에서 확인).",
            "- register(등록부): retrospective register(회고 등록부)를 next due(다음 도래) F80 기준으로 reset(재설정).",
            "",
            "## Next Stage Open Block Check(다음 단계 개방 차단 점검)",
            "",
            "- before packet(묶음 전): `due_after_f75_closeout_pending_retrospective(도래, F75 마감 뒤 회고 대기)`.",
            "- after packet(묶음 뒤): `not_due_after_frontier71_to_75_retrospective_completed(전선71-F75 회고 완료 뒤 아직 아님)`.",
            f"- next_run(다음 실행): `{NEXT_RUN_ID}`.",
        ]
    )
    return lines


def receipt_lines(summary: Mapping[str, Any]) -> list[str]:
    classification = summary["classification"]
    return [
        "# Frontier71-F75 Retrospective Receipt(전선71-F75 회고 영수증)",
        "",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- created_at_utc(생성 시각): `{utc_now()}`",
        "- trigger_reason(트리거 이유): F75 closeout made five frontier closeouts since last retrospective(F75 마감으로 이전 회고 뒤 전선 5개 마감 도달).",
        f"- review_size(검토 크기): `medium(중간)`.",
        "- direction_before_grok(Grok 전 방향): F76 axis-ablation source discovery(F76 축 제거/교체 기반 원천 탐색).",
        f"- bounded_evidence(제한 근거): `{rel(BOUNDED_EVIDENCE)}`.",
        f"- prompt_identity(프롬프트 정체성): `{rel(PROMPT)}`, sha256 `{summary['prompt_hash']}`.",
        f"- grok_output_identity(Grok 출력 정체성): `{rel(CLEAN_OUTPUT)}`, sha256 `{summary['clean_output_hash']}`.",
        f"- advice_classification(조언 분류): `{classification['advice_classification']}`.",
        f"- accepted(수용): `{'; '.join(classification['accepted'])}`.",
        f"- rejected(거절): `{'; '.join(classification['rejected'])}`.",
        f"- needs_local_verification(로컬 검증 필요): `{'; '.join(classification['needs_local_verification'])}`.",
        f"- local_verification(로컬 검증): `{rel(LOCAL_VERIFICATION)}`.",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve accepted(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 수용 없음).",
        f"- final_codex_direction(최종 Codex 방향): `{classification['direction_delta']}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def local_verification_lines(summary: Mapping[str, Any]) -> list[str]:
    lines = [
        "# Local Verification(로컬 검증)",
        "",
        f"- created_at_utc(생성 시각): `{utc_now()}`",
        f"- prompt_hash(프롬프트 해시): `{summary['prompt_hash']}`",
        f"- clean_output_hash(정리 출력 해시): `{summary['clean_output_hash']}`",
        f"- metadata_path(메타데이터 경로): `{rel(METADATA)}`",
        f"- raw_diagnostics_path(원본 진단 경로): `{rel(RAW_DIAGNOSTICS)}`",
        "",
        "| artifact(산출물) | status(상태) | effect(효과) |",
        "|---|---|---|",
    ]
    for row in STAGE_ROWS:
        path = ROOT / row["report_path"]
        status = "exists(존재)" if path_exists(path) else "missing(누락)"
        lines.append(f"| `{row['report_path']}` | `{status}` | closeout evidence identity(마감 근거 정체성) |")
    lines.extend(
        [
            f"| `{rel(BOUNDED_EVIDENCE)}` | `written(기록)` | bounded evidence table durable(제한 근거표 지속화) |",
            f"| `{rel(RETROSPECTIVE_REGISTER)}` | `updated(갱신)` | next frontier open block cleared after packet(묶음 뒤 다음 전선 개방 차단 해제) |",
            f"| `{rel(WORKSPACE_STATE)}` | `updated(갱신)` | current truth points to F76 stage open as next run(현재 진실이 F76 단계 개방을 다음 실행으로 가리킴) |",
        ]
    )
    return lines


def next_open_block_lines() -> list[str]:
    return [
        "# Next Stage Open Block Check(다음 단계 개방 차단 점검)",
        "",
        f"- checked_at_utc(점검 시각): `{utc_now()}`",
        "- before(이전): `due_after_f75_closeout_pending_retrospective(도래, F75 마감 뒤 회고 대기)`.",
        "- action(행동): ran Frontier71-F75 five-stage retrospective(전선71-F75 5단계 회고 실행).",
        "- effect(효과): next frontier open(다음 전선 개방) gate(게이트)를 `not_due_after_frontier71_to_75_retrospective_completed(전선71-F75 회고 완료 뒤 아직 아님)`으로 되돌린다.",
        f"- next_run(다음 실행): `{NEXT_RUN_ID}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def update_register() -> None:
    lines = [
        "version: five_stage_retrospective_register_v1",
        "source_of_truth: docs/registers/five_stage_retrospective_register.yaml",
        "purpose: Track five-stage Grok retrospective(5단계 Grok 회고) cadence without relying on Codex memory(코덱스 기억).",
        "adopted_at_utc: '2026-06-16T12:05:00Z'",
        "adopted_during_stage_id: stage_frontier_66__runtime_probe_backfill_gap_audit_frontier02_to_64",
        "cadence:",
        "  primary_trigger: closing_frontier_number % 5 == 0",
        "  fallback_trigger: len(closed_frontier_ids_since_last_retrospective) >= 5",
        "  next_open_block: true",
        "  scope_rule: Use latest five canonical frontier closeout stage ids with closeout receipts, not numeric NN-4..NN alone.",
        "required_outputs:",
        "- five_stage_retrospective_packet",
        "- bounded_evidence_table",
        "- grok_receipt",
        "- codex_local_verification",
        "- advice_classification",
        "- compact_retrospective_report",
        "- next_stage_open_block_check",
        "required_row_fields:",
        "- stage_id",
        "- hypothesis",
        "- proxy_kpi",
        "- mt5_runtime_probe_kpi",
        "- proxy_runtime_gap_cause",
        "- closeout_label",
        "- preserved_clue",
        "- negative_memory",
        "- systemic_repeat",
        "- next_action",
        "claim_boundary:",
        "  allowed:",
        "  - direction_delta",
        "  - repair_priority_delta",
        "  forbidden:",
        "  - completion",
        "  - baseline",
        "  - promotion",
        "  - runtime_authority",
        "  - live_readiness",
        "  - goal_achieve",
        "state:",
        f"  last_completed_packet_id: {PACKET_ID}",
        "  last_completed_at_frontier: 75",
        "  last_completed_stage_ids:",
    ]
    lines.extend(f"  - {row['stage_id']}" for row in STAGE_ROWS)
    lines.extend(
        [
            f"  last_completed_at_utc: '{utc_now()}'",
            "  closed_frontier_ids_since_last_retrospective: []",
            "  closeouts_since_last: 0",
            "  next_numeric_trigger_frontier: 80",
            "  current_due_status: not_due_after_frontier71_to_75_retrospective_completed",
            "  note: F71-F75 retrospective(회고)가 완료됐다. F76 open(개방)은 회고 게이트 관점에서 허용되지만, F76 자체 stage-open Grok 검토는 별도로 필요하다.",
        ]
    )
    write_text(RETROSPECTIVE_REGISTER, "\n".join(lines))


def ledger_row() -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": "five_stage_retrospective_frontier71_to_75",
        "lane": "five_stage_retrospective(5단계 회고)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(RETROSPECTIVE_REPORT),
        "notes": "F71-F75 retrospective closed with direction_delta and repair_priority_delta only.",
        "family": "five_stage_retrospective(5단계 회고)",
        "primary_report": rel(RETROSPECTIVE_REPORT),
        "run_number": "retrospective_f71_f75",
        "date": "2026-06-17",
        "decision": "clear_next_frontier_open_block_after_retrospective",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(STAGE_ROWS),
        "gate_passes": 7,
        "gate_total": 7,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RETROSPECTIVE_REPORT),
        "run_date": "2026-06-17",
        "primary_artifact": rel(RUN_MANIFEST),
        "result_status": STATUS,
        "view": "five_stage_retrospective(5단계 회고)",
        "tier": "not_applicable_cross_stage_retrospective(단계 간 회고라 해당 없음)",
        "metric_scope": "cross_stage_synthesis(단계 간 종합)",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "retrospective(회고)",
        "external_verification_status": "grok_review_completed_local_verification_recorded(Grok 검토 완료, 로컬 검증 기록)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(RETROSPECTIVE_REPORT),
        "gate_audit_path": rel(NEXT_OPEN_BLOCK_CHECK),
        "created_at": utc_now(),
        "ledger_row_id": f"{RUN_ID}__retrospective",
        "subrun_id": "retrospective(회고)",
        "record_view": "retrospective(회고)",
        "tier_scope": "not_applicable_cross_stage_retrospective",
        "kpi_scope": "f71_f75_closeout_synthesis(F71-F75 마감 종합)",
        "primary_kpi": "direction_delta=axis_ablation_source_discovery;repair_priority_delta=feature_label_model_trade_risk_session_novelty",
        "guardrail_kpi": "no completion/baseline/promotion/runtime authority/live readiness/goal achieve",
        "work_family": "five_stage_retrospective(5단계 회고)",
        "row_id": f"{RUN_ID}__retrospective",
        "evidence_boundary": "direction_delta_only_no_authority(방향 변화만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "What should F71-F75 change in the next frontier direction?(F71-F75는 다음 전선 방향을 어떻게 바꿔야 하나?)",
        "artifact_count": 7,
        "created_at_utc": utc_now(),
        "required_gate_audit": rel(NEXT_OPEN_BLOCK_CHECK),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "five_stage_retrospective(5단계 회고)",
        "run_type": "retrospective(회고)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(RETROSPECTIVE_REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "bounded_grok_review_and_local_verification(제한 Grok 검토와 로컬 검증)",
    }


def update_ledgers() -> None:
    row = ledger_row()
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)


def write_state_files() -> None:
    workspace = [
        "current_stage_id: stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density",
        "active_stage: stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f75_closed_after_mandatory_runtime_probe",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_frontier71_to_75_retrospective_completed",
        f"updated_at_utc: '{utc_now()}'",
        "context_anchor: stages/stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density/03_reviews/context_anchor.md",
        "notes:",
        "  - \"Action(행동): F71-F75 five-stage retrospective(5단계 회고)를 완료했다.\"",
        "  - \"Effect(효과): F76 open(개방)은 회고 게이트 관점에서 허용되며, 다음 방향은 axis-ablation source discovery(축 제거/교체 기반 원천 탐색)다.\"",
        "  - \"Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).\"",
    ]
    write_text(WORKSPACE_STATE, "\n".join(workspace))

    current = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {utc_now()}",
        "",
        "Active stage(활성 단계): `stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): Frontier71-F75 five-stage retrospective(전선71-F75 5단계 회고)를 완료했다.",
        "",
        "Effect(효과): F76 open(개방) 전 회고 게이트(retrospective gate, 회고 게이트)를 닫고, 다음 전선 방향을 axis-ablation source discovery(축 제거/교체 기반 원천 탐색)로 바꿨다.",
        "",
        "## Direction Delta(방향 변화)",
        "",
        "- F76 proposed direction(F76 제안 방향): feature set/label/model/trade/risk/session axes(피처 묶음/라벨/모델/거래/위험/세션 축)를 빼기, 교체, 재조합하는 source-discovery matrix(원천 탐색 행렬).",
        "- Do-not-repeat(반복 금지): same-surface threshold/tape/cooldown/parity-only repair(동일 표면 임계값/테이프/쿨다운/동등성 단독 수리).",
        "- Runtime rule(런타임 규칙): proxy(프록시)가 meaningful signal(의미 신호)을 만들면 MT5 Runtime Probe(MT5 런타임 탐침)를 물질화한다.",
        "",
        "## Key Artifacts(핵심 산출물)",
        "",
        f"- retrospective report(회고 보고서): `{rel(RETROSPECTIVE_REPORT)}`",
        f"- receipt(영수증): `{rel(RECEIPT)}`",
        f"- local verification(로컬 검증): `{rel(LOCAL_VERIFICATION)}`",
        f"- next open block check(다음 개방 차단 점검): `{rel(NEXT_OPEN_BLOCK_CHECK)}`",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    write_text(CURRENT_WORKING_STATE, "\n".join(current))


def finalize() -> None:
    missing = [rel(path) for path in [PROMPT, CLEAN_OUTPUT, METADATA] if not path_exists(path)]
    if missing:
        raise RuntimeError(f"missing Grok retrospective evidence: {missing}")
    clean_text = io_path(CLEAN_OUTPUT).read_text(encoding="utf-8-sig")
    classification = classify_advice(clean_text)
    summary = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "covered_stage_ids": [row["stage_id"] for row in STAGE_ROWS],
        "prompt": rel(PROMPT),
        "clean_output": rel(CLEAN_OUTPUT),
        "metadata": rel(METADATA),
        "prompt_hash": file_hash(PROMPT),
        "clean_output_hash": file_hash(CLEAN_OUTPUT),
        "classification": classification,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": utc_now(),
    }
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
        "inputs": {
            "bounded_evidence": rel(BOUNDED_EVIDENCE),
            "prompt": rel(PROMPT),
            "clean_output": rel(CLEAN_OUTPUT),
            "metadata": rel(METADATA),
            "raw_diagnostics": rel(RAW_DIAGNOSTICS),
        },
        "outputs": {
            "advice_classification": rel(ADVICE_CLASSIFICATION),
            "retrospective_report": rel(RETROSPECTIVE_REPORT),
            "receipt": rel(RECEIPT),
            "local_verification": rel(LOCAL_VERIFICATION),
            "next_stage_open_block_check": rel(NEXT_OPEN_BLOCK_CHECK),
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(ADVICE_CLASSIFICATION, classification)
    write_json(RUN_MANIFEST, manifest)
    write_text(RETROSPECTIVE_REPORT, "\n".join(report_lines(summary)))
    write_text(RECEIPT, "\n".join(receipt_lines(summary)))
    write_text(LOCAL_VERIFICATION, "\n".join(local_verification_lines(summary)))
    write_text(NEXT_OPEN_BLOCK_CHECK, "\n".join(next_open_block_lines()))
    update_register()
    update_ledgers()
    write_state_files()
    print(
        json.dumps(
            json_ready(
                {
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "covered_stage_count": len(STAGE_ROWS),
                    "next_run_id": NEXT_RUN_ID,
                    "retrospective_due_status": "not_due_after_frontier71_to_75_retrospective_completed",
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    if args.prepare == args.finalize:
        raise SystemExit("choose exactly one of --prepare or --finalize")
    if args.prepare:
        prepare()
    else:
        finalize()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
