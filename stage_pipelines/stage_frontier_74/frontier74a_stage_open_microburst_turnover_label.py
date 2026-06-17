from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists


STAGE_ID = "stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path"
RUN_ID = "frontier74A_stage_open_new_hypothesis_after_f73_session_regime_negative_memory_v1"
NEXT_RUN_ID = "frontier74B_microburst_turnover_raw_label_and_proxy_scout_v1"
PARENT_RUN_ID = "frontier73H_stage_closeout_session_regime_feature_model_rotation_v1"
IDEA_ID = "IDEA-FR74-MICROBURST-TURNOVER-LABEL-DENSE-SMOOTH-RUNTIME-PATH"
STATUS = "stage_open_design_completed_no_authority"
JUDGMENT = "microburst_turnover_label_stage_open_design_only_no_authority"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
SPEC_ROOT = STAGE_ROOT / "00_spec"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f74_stage_open_microburst_turnover_label"
GROK_PROMPT = GROK_PACKET / "prompts/f74_stage_open_microburst_turnover_label_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

F73_CLOSEOUT = ROOT / "stages/stage_frontier_73__session_regime_feature_model_rotation_for_runtime_economics_gap/03_reviews/stage_closeout_report.md"
RETROSPECTIVE_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"
NEGATIVE_REGISTER = ROOT / "docs/registers/negative_result_register.md"
FWD12_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FWD12_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
FWD18_INPUT = ROOT / "data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
FWD18_FEATURE_ORDER = ROOT / "data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_feature_order.txt"
RAW_US100 = ROOT / "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"

ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_md(path: Path, lines: Sequence[str]) -> None:
    write_text(path, "\n".join(lines))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    text = json.dumps(json_ready(payload), ensure_ascii=False, indent=2)
    write_text(path, text)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV without schema: {path}")
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path_exists(path) else ""
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
    if key not in fieldnames:
        raise KeyError(f"{key} not found in {path}")
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(values: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(values).encode("utf-8")).hexdigest()


def git_status() -> str:
    return subprocess.check_output(["git", "status", "--short", "--branch"], cwd=ROOT, text=True, encoding="utf-8").strip()


def required_inputs() -> list[Path]:
    return [
        GROK_PROMPT,
        GROK_CLEAN,
        GROK_METADATA,
        F73_CLOSEOUT,
        RETROSPECTIVE_REGISTER,
        NEGATIVE_REGISTER,
        FWD12_INPUT,
        FWD12_FEATURE_ORDER,
        FWD18_INPUT,
        FWD18_FEATURE_ORDER,
        RAW_US100,
        ALPHA_LEDGER,
        RUN_REGISTRY,
    ]


def data_identity() -> dict[str, Any]:
    fwd12 = pd.read_parquet(io_path(FWD12_INPUT))
    fwd18 = pd.read_parquet(io_path(FWD18_INPUT))
    features12 = [line.strip() for line in read_text(FWD12_FEATURE_ORDER).splitlines() if line.strip()]
    features18 = [line.strip() for line in read_text(FWD18_FEATURE_ORDER).splitlines() if line.strip()]
    raw = pd.read_csv(io_path(RAW_US100), usecols=["time_close_unix", "open", "high", "low", "close", "spread_points"])
    return {
        "fwd12_path": rel(FWD12_INPUT),
        "fwd12_sha256": sha256(FWD12_INPUT),
        "fwd12_rows": int(len(fwd12)),
        "fwd12_split_counts": {str(k): int(v) for k, v in fwd12["split"].value_counts().to_dict().items()},
        "fwd18_path": rel(FWD18_INPUT),
        "fwd18_sha256": sha256(FWD18_INPUT),
        "fwd18_rows": int(len(fwd18)),
        "fwd18_split_counts": {str(k): int(v) for k, v in fwd18["split"].value_counts().to_dict().items()},
        "feature_order_fwd12_sha256": sha256(FWD12_FEATURE_ORDER),
        "feature_order_fwd18_sha256": sha256(FWD18_FEATURE_ORDER),
        "feature_order_hash_fwd12": ordered_hash(features12),
        "feature_order_hash_fwd18": ordered_hash(features18),
        "feature_order_same": features12 == features18,
        "raw_us100_path": rel(RAW_US100),
        "raw_us100_sha256": sha256(RAW_US100),
        "raw_us100_rows": int(len(raw)),
        "time_axis": "MT5 M5 bar close time(메타트레이더5 5분봉 종가 시각)",
    }


def axis_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for horizon, target_atr, stop_atr in ((3, 0.35, 0.30), (6, 0.55, 0.40), (9, 0.75, 0.50)):
        for side in ("long", "short"):
            rows.append(
                {
                    "axis_id": f"microburst_h{horizon}_{side}",
                    "label_target": "first_touch_reward_before_risk(위험 전 보상 선도달)",
                    "horizon_bars": horizon,
                    "side": f"{side}({ '롱' if side == 'long' else '숏' })",
                    "target_atr": target_atr,
                    "stop_atr": stop_atr,
                    "max_hold_bars": horizon,
                    "raw_label_density_gate": ">=2_to_4_trades_day_before_model(모델 전 일 2~4회 이상)",
                    "proxy_density_targets": "5,7,9 trades/day(일 5,7,9회)",
                    "do_not_repeat": "no threshold/cooldown/quota-only density repair(임계값/쿨다운/할당 단독 밀도 수리 금지)",
                }
            )
    return rows


def surface_rows() -> list[dict[str, Any]]:
    return [
        {
            "surface_id": "raw_microburst_density_gate",
            "purpose": "label-only density feasibility(라벨 단독 밀도 가능성)",
            "features": "none(없음)",
            "models": "none(없음)",
            "stop_condition": "if raw labels are below 2/day, repair label before model(원시 라벨이 일 2회 미만이면 모델 전 라벨 수리)",
        },
        {
            "surface_id": "micro_path_core_linear_tree",
            "purpose": "dense micro path signal scout(조밀한 미세 경로 신호 탐색)",
            "features": "core path, ATR, session(핵심 경로, 평균진폭, 세션)",
            "models": "logistic_l2, extra_trees_ref, hist_gbm",
            "stop_condition": "no validation/OOS positive density pair(검증/표본외 양수 밀도 쌍 없음)",
        },
        {
            "surface_id": "adverse_excursion_ablation",
            "purpose": "path-veto value test(경로 차단 가치 시험)",
            "features": "core plus adverse excursion filters(핵심 + 불리 이동 필터)",
            "models": "extra_trees_ref, hist_gbm",
            "stop_condition": "validation DD over 20% despite OOS profit(표본외 이익에도 검증 손실폭 20% 초과)",
        },
        {
            "surface_id": "session_microburst_split",
            "purpose": "cash open/mid/late density split(정규장 초/중/후반 밀도 분할)",
            "features": "session regime core(세션 장세 핵심)",
            "models": "logistic_l2, hist_gbm",
            "stop_condition": "single-session sparse clue below runtime value(단일 세션 희소 단서가 런타임 가치 미달)",
        },
    ]


def prior_delta_rows() -> list[dict[str, str]]:
    return [
        {
            "prior": "F68",
            "memory": "risk-only lifecycle proxy failed validation DD(위험 단독 생명주기 프록시가 검증 손실폭에서 실패)",
            "f74_delta": "label-native reward-before-risk before risk repair(위험 수리 전 라벨 내장 보상-위험 구조)",
        },
        {
            "prior": "F69",
            "memory": "threshold/cooldown/quota repair failed(임계값/쿨다운/할당 수리가 실패)",
            "f74_delta": "raw label density is checked before selection mechanics(선택 장치 전 원시 라벨 밀도 확인)",
        },
        {
            "prior": "F72",
            "memory": "trade-shape-first lifecycle surface was weak(거래 형태 우선 생명주기 표면이 약함)",
            "f74_delta": "short 3/6/9-bar microburst turnover label with density gate(짧은 3/6/9봉 마이크로버스트 회전 라벨과 밀도 게이트)",
        },
        {
            "prior": "F73",
            "memory": "adapter repaired parity but density and validation DD failed(어댑터는 동등성을 고쳤지만 밀도와 검증 손실폭은 실패)",
            "f74_delta": "not adapter-only; lifecycle compression enters the label and proxy design(어댑터 단독이 아니라 생명주기 압축을 라벨/프록시에 넣음)",
        },
    ]


def experiment_design(identity: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "idea_id": IDEA_ID,
        "hypothesis": "microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험한다.",
        "decision_use": "short-horizon first-touch labels(짧은 수평선 선도달 라벨)이 proxy scout(프록시 탐색)와 MT5 Runtime Probe(MT5 런타임 탐침)를 받을 가치가 있는지 결정한다.",
        "comparison_baseline": "F73F direct binary adapter runtime observation(F73F 직접 이진 어댑터 런타임 관찰)",
        "control_variables": ["US100 M5", "same train/validation/OOS split(동일 학습/검증/표본외 분할)", "no inherited winner/baseline(상속 승자/기준선 없음)"],
        "changed_variables": ["label/target(라벨/목표)", "trade shape(거래 형태)", "risk logic inside label(라벨 내부 위험 로직)", "model family after raw gate(원시 게이트 뒤 모델 계열)"],
        "sample_scope": identity,
        "success_criteria": [
            "raw label density >=2/day before model(모델 전 원시 라벨 밀도 일 2회 이상)",
            "proxy moves toward 5-10 trades/day(프록시가 일 5~10회 방향으로 이동)",
            "validation and OOS both positive without DD explosion(검증과 표본외가 모두 양수이고 손실폭 폭발 없음)",
        ],
        "failure_criteria": [
            "raw labels sparse below 2/day(원시 라벨 일 2회 미만)",
            "validation DD >20% with OOS-only gain(표본외만 좋고 검증 손실폭 20% 초과)",
            "density explained only by threshold/cooldown/quota(밀도가 임계값/쿨다운/할당만으로 설명됨)",
        ],
        "invalid_conditions": ["split mismatch(분할 불일치)", "feature order mismatch without record(기록 없는 피처 순서 불일치)", "lookahead beyond horizon(수평선 밖 미래 누수)"],
        "stop_conditions": ["raw density failure -> label repair(원시 밀도 실패 -> 라벨 수리)", "proxy near-miss -> Grok then MT5 probe(프록시 근접 -> Grok 뒤 MT5 탐침)", "repeated quota repair -> close or pivot(할당 수리 반복 -> 마감 또는 전환)"],
        "evidence_plan": ["stage brief(단계 개요)", "axis contract(축 계약)", "raw label density table(원시 라벨 밀도표)", "proxy KPI(프록시 KPI)", "Grok receipt(그록 영수증)", "MT5 runtime receipt if meaningful(의미 신호면 MT5 런타임 영수증)"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def stage_brief_lines() -> list[str]:
    return [
        "# F74 Stage Brief(F74 단계 개요)",
        "",
        f"- stage_id(단계 ID): `{STAGE_ID}`",
        f"- opening_run(개방 실행): `{RUN_ID}`",
        "- hypothesis(가설): microburst turnover labels(마이크로버스트 회전 라벨)이 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험한다.",
        "- novelty_delta(신규성 차이): F73 adapter-only repair(어댑터 단독 수리)가 아니라 label/target(라벨/목표), trade shape(거래 형태), risk logic(위험 로직)을 먼저 바꾼다.",
        "- do_not_repeat(반복 금지): threshold/cooldown/quota-only repair(임계값/쿨다운/할당 단독 수리)로 밀도를 만든 척하지 않는다.",
        "- mandatory_runtime_probe(필수 런타임 탐침): proxy(프록시)가 의미 있거나 근접 신호를 만들면 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]


def report_lines(created_at: str, identity: Mapping[str, Any], grok_hash: str) -> list[str]:
    return [
        "# Frontier74A Stage Open(F74A 단계 개방)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- idea_id(아이디어 ID): `{IDEA_ID}`",
        f"- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Hypothesis(가설)",
        "",
        "short-horizon microburst turnover labels(짧은 수평선 마이크로버스트 회전 라벨)이 first-touch reward-before-risk(위험 전 보상 선도달), native density target(내장 밀도 목표), lifecycle-aware proxy simulation(생명주기 인식 프록시 시뮬레이션)을 결합해 dense smooth runtime path(조밀하고 매끄러운 런타임 경로)의 seed surface(씨앗 표면)를 만들 수 있는지 시험한다.",
        "",
        "## Grok Stage Open Review(Grok 단계 개방 검토)",
        "",
        f"- packet(묶음): `{rel(GROK_PACKET)}`",
        f"- prompt(프롬프트): `{rel(GROK_PROMPT)}`, sha256 `{sha256(GROK_PROMPT)}`",
        f"- output(출력): `{rel(GROK_CLEAN)}`, sha256 `{grok_hash}`",
        "- advice_classification(조언 분류): `accepted(수용)`",
        "- accepted(수용): F74 is novel and bounded(F74는 신규성과 경계가 있다).",
        "- drift_risk(드리프트 위험): density quota backdoor(밀도 할당 우회).",
        "- repair_priority(수리 우선순위): label-only density gate first(라벨 단독 밀도 게이트 우선).",
        "",
        "## Data Identity(데이터 정체성)",
        "",
        f"- fwd12 rows(행): `{identity['fwd12_rows']}`, sha256 `{identity['fwd12_sha256']}`",
        f"- fwd18 rows(행): `{identity['fwd18_rows']}`, sha256 `{identity['fwd18_sha256']}`",
        f"- raw US100 rows(원시 US100 행): `{identity['raw_us100_rows']}`, sha256 `{identity['raw_us100_sha256']}`",
        f"- feature_order_same(피처 순서 동일): `{identity['feature_order_same']}`",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}` raw label density/proxy scout(원시 라벨 밀도/프록시 탐색)를 실행한다.",
    ]


def grok_receipt_lines(created_at: str, grok_hash: str) -> list[str]:
    metadata = json.loads(io_path(GROK_METADATA).read_text(encoding="utf-8"))
    return [
        "# F74A Grok Stage Open Receipt(F74A Grok 단계 개방 영수증)",
        "",
        f"- created_at_utc(생성 시각): `{created_at}`",
        "- trigger_reason(트리거 이유): F74 new frontier stage open(F74 새 전선 단계 개방)은 Grok second opinion(그록 2차 의견)이 필요하다.",
        "- review_size(검토 크기): `medium(중간)`",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{sha256(GROK_PROMPT)}`",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{grok_hash}`",
        f"- wrapper_success(래퍼 성공): `{metadata.get('success')}`; returncode(반환 코드): `{metadata.get('returncode')}`",
        "- advice_classification(조언 분류): `accepted(수용)`",
        "- accepted(수용): label/target shift(라벨/목표 전환), raw label density gate(원시 라벨 밀도 게이트), bounded claim(경계 있는 주장).",
        "- rejected(거절): stage open(단계 개방)을 막는 조언 없음.",
        "- needs_local_verification(로컬 검증 필요): F74B implementation(구현)에서 F72/F73 반복 여부를 확인한다.",
        "- forbidden_claim_check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 없음.",
        f"- final_codex_direction(최종 Codex 방향): `{STAGE_ID}`를 열고 `{NEXT_RUN_ID}`를 실행한다.",
    ]


def gate_audit_lines(created_at: str) -> list[str]:
    return [
        "# F74A Required Gate Coverage Audit(F74A 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "| gate(게이트) | status(상태) | evidence/effect(근거/효과) |",
        "|---|---|---|",
        "| retrospective due check(중간 검토 도래 점검) | `pass_not_due(통과, 아직 아님)` | F73 closeout(마감)은 F66-F70 retrospective(중간 검토) 뒤 3/5이다. |",
        "| stage open Grok review(단계 개방 Grok 검토) | `pass(통과)` | Grok advice(그록 조언)는 accepted(수용)로 분류했다. |",
        "| novelty delta(신규성 차이) | `pass(통과)` | label/target and trade shape(라벨/목표와 거래 형태)를 먼저 바꾼다. |",
        "| do-not-repeat guard(반복 금지 보호) | `pass(통과)` | adapter/threshold/quota-only repair(어댑터/임계값/할당 단독 수리)를 금지한다. |",
        "| final claim guard(최종 주장 보호) | `pass(통과)` | no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). |",
    ]


def base_ledger_row(created_at: str) -> dict[str, Any]:
    report = REVIEWS_ROOT / "frontier74A_stage_open_microburst_turnover_label_report.md"
    manifest = RUN_ROOT / "run_manifest.json"
    audit = REVIEWS_ROOT / "required_gate_coverage_audit_f74a.md"
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open_design",
        "row_id": f"{RUN_ID}__stage_open_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_open_design(단계 개방 설계)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "view": "stage_open(단계 개방)",
        "tier_scope": "Tier A+B planned(Tier A+B 계획)",
        "tier": "Tier A+B planned(Tier A+B 계획)",
        "kpi_scope": "design_and_grok_review(설계와 Grok 검토)",
        "metric_scope": "design_and_grok_review(설계와 Grok 검토)",
        "scoreboard_lane": "experiment_design(실험 설계)",
        "lane": "stage_open(단계 개방)",
        "family": "stage_open_design(단계 개방 설계)",
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
        "primary_kpi": "axis_rows=6; surface_rows=4; grok=accepted",
        "guardrail_kpi": "raw_label_density_gate_first; no quota_only_repair",
        "external_verification_status": "out_of_scope_by_claim_stage_open_design_only(단계 개방 설계 주장 범위 밖)",
        "notes": "F74 opens microburst turnover label exploration after F73 negative memory(F73 부정 기억 뒤 F74 마이크로버스트 회전 라벨 탐색 개방).",
        "run_number": "frontier74A",
        "date": created_at[:10],
        "run_date": created_at[:10],
        "decision": "open_f74_microburst_turnover_label",
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": 5,
        "gate_total": 5,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created_at,
        "required_gate_audit": rel(audit),
        "gate_audit_path": rel(audit),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "microburst_turnover_label_design(마이크로버스트 회전 라벨 설계)",
        "input_run_id": PARENT_RUN_ID,
        "question": "Can microburst turnover labels create dense smooth runtime-path seed surface?(마이크로버스트 회전 라벨이 조밀하고 매끄러운 런타임 경로 씨앗 표면을 만들 수 있나?)",
        "evidence_boundary": "stage_open_design_only_no_runtime(단계 개방 설계 전용, 런타임 없음)",
    }


def update_ledgers(created_at: str) -> None:
    row = base_ledger_row(created_at)
    stage_ledger = REVIEWS_ROOT / "stage_run_ledger.csv"
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(stage_ledger, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers() -> None:
    marker = "<!-- frontier74A_stage_open_microburst_turnover_label_v1 -->"
    block = f"""<!-- frontier74A_stage_open_microburst_turnover_label_v1 -->
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier74(전선74) as microburst turnover label exploration(마이크로버스트 회전 라벨 탐색). Hypothesis(가설): short-horizon first-touch labels(짧은 수평선 선도달 라벨) with native density/lifecycle proxy(내장 밀도/생명주기 프록시)가 F73 parity-only negative memory(F73 동등성 단독 부정 기억) 뒤 dense smooth runtime-path seed surface(조밀하고 매끄러운 런타임 경로 씨앗 표면)를 만들 수 있는지 시험한다. Boundary(경계): stage_open_design_only(단계 개방 설계 전용), no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(IDEA_REGISTRY, marker, block)


def update_state(created_at: str) -> None:
    workspace_state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f74_stage_open_runtime_probe_pending",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f73_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        '  - "Action(행동): F74 stage open(단계 개방)을 완료했다."',
        '  - "Effect(효과): microburst turnover label(마이크로버스트 회전 라벨)을 새 가설로 열고 raw label density gate(원시 라벨 밀도 게이트)를 먼저 검증하게 했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    write_text(WORKSPACE_STATE, "\n".join(workspace_state))
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
            "Action(행동): F74 stage open(단계 개방)을 완료했다.",
            "",
            f"Effect(효과): 다음 실행을 `{NEXT_RUN_ID}`로 설정하고 raw label density gate(원시 라벨 밀도 게이트)를 먼저 검증하게 했다.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def main() -> int:
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F74A required material missing: {missing}")

    created_at = utc_now()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)

    identity = data_identity()
    grok_hash = sha256(GROK_CLEAN)
    axes = axis_rows()
    surfaces = surface_rows()
    prior_deltas = prior_delta_rows()
    design = experiment_design(identity)
    verification = {
        "created_at_utc": created_at,
        "git_status": git_status(),
        "retrospective_due_status": "not_due_after_f73_closeout",
        "grok_prompt_hash": sha256(GROK_PROMPT),
        "grok_clean_hash": grok_hash,
        "data_identity": identity,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    write_json(RUN_ROOT / "f74a_experiment_design.json", design)
    write_json(RUN_ROOT / "f74a_data_identity.json", identity)
    write_json(RUN_ROOT / "f74a_local_verification.json", verification)
    write_json(
        RUN_ROOT / "f74a_model_validation_plan.json",
        {
            "model_families": ["logistic_l2", "extra_trees_ref", "hist_gbm", "small_nn_16_optional"],
            "raw_label_density_gate_before_model": True,
            "selection_targets_trades_day": [5, 7, 9],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(RUN_ROOT / "f74a_axis_contract.csv", axes)
    write_csv(RUN_ROOT / "f74a_proxy_scout_surface_plan.csv", surfaces)
    write_csv(RUN_ROOT / "f74a_prior_stage_difference_table.csv", prior_deltas)
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "artifacts": {
                "axis_contract": rel(RUN_ROOT / "f74a_axis_contract.csv"),
                "surface_plan": rel(RUN_ROOT / "f74a_proxy_scout_surface_plan.csv"),
                "experiment_design": rel(RUN_ROOT / "f74a_experiment_design.json"),
            },
        },
    )

    write_md(SPEC_ROOT / "stage_brief.md", stage_brief_lines())
    write_csv(REVIEWS_ROOT / "f74a_axis_contract_review.csv", axes)
    write_csv(REVIEWS_ROOT / "f74a_proxy_scout_surface_plan_review.csv", surfaces)
    write_csv(REVIEWS_ROOT / "f74a_prior_stage_difference_table.csv", prior_deltas)
    write_json(REVIEWS_ROOT / "f74a_experiment_design_review.json", design)
    write_json(REVIEWS_ROOT / "f74a_data_identity_review.json", identity)
    write_json(REVIEWS_ROOT / "f74a_local_verification.json", verification)
    write_md(REVIEWS_ROOT / "frontier74A_stage_open_microburst_turnover_label_report.md", report_lines(created_at, identity, grok_hash))
    write_md(REVIEWS_ROOT / "grok_stage_open_receipt.md", grok_receipt_lines(created_at, grok_hash))
    write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f74a.md", gate_audit_lines(created_at))
    write_md(
        REVIEWS_ROOT / "review_index.md",
        [
            "# F74 Review Index(F74 검토 색인)",
            "",
            "- `frontier74A_stage_open_microburst_turnover_label_report.md`",
            "- `required_gate_coverage_audit_f74a.md`",
            "- `grok_stage_open_receipt.md`",
        ],
    )

    update_ledgers(created_at)
    update_registers()
    update_state(created_at)

    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "grok_clean_hash": grok_hash,
                    "axis_rows": len(axes),
                    "surface_rows": len(surfaces),
                    "next_run_id": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
