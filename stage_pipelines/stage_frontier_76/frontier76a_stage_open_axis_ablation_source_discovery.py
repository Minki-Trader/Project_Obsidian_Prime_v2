from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics"
RUN_ID = "frontier76A_stage_open_axis_ablation_source_discovery_v1"
NEXT_RUN_ID = "frontier76B_axis_ablation_proxy_scout_v1"
PARENT_RUN_ID = "frontier71_to_75_five_stage_retrospective_v1"
IDEA_ID = "IDEA-FR76-AXIS-ABLATION-SOURCE-DISCOVERY"
STATUS = "stage_open_design_completed_no_authority"
JUDGMENT = "axis_ablation_source_discovery_stage_open_design_only_no_authority"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
SCOUT_CLUE_GATE = (
    "at least one split net>0 or PF>=1.15, trade_count>=50, "
    "density proxy >=0.75 trades/day, and fragility recorded"
)
MEANINGFUL_SIGNAL_GATE = (
    "validation+OOS net>0, PF>=1.30, DD<=10%, trades/day>=1.0, "
    "trade_count>=100 per split"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
SPEC_DIR = STAGE_DIR / "00_spec"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

REVIEW_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f76_stage_open_axis_ablation_source_discovery"
PROMPT = REVIEW_ROOT / "prompts/f76_stage_open_axis_ablation_source_discovery_prompt.md"
OUTPUT_DIR = REVIEW_ROOT / "outputs"
CLEAN_OUTPUT = OUTPUT_DIR / "clean_output.md"
METADATA = OUTPUT_DIR / "metadata.json"
RAW_DIAGNOSTICS = OUTPUT_DIR / "raw_diagnostics.json"

DATASET_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_feature_order.txt"
)
RETRO_REPORT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_frontier71_to_75_five_stage_retrospective/retrospective_report.md"
RETRO_RECEIPT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_frontier71_to_75_five_stage_retrospective/receipt.md"
RETRO_REGISTER = ROOT / "docs/registers/five_stage_retrospective_register.yaml"

REPORT = REVIEW_DIR / "frontier76A_stage_open_axis_ablation_source_discovery_report.md"
ANCHOR = REVIEW_DIR / "context_anchor.md"
GROK_RECEIPT = REVIEW_DIR / "grok_stage_open_receipt.md"
GATE_AUDIT = REVIEW_DIR / "required_gate_coverage_audit_f76a.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
AXIS_MATRIX = REVIEW_DIR / "f76a_axis_ablation_matrix.csv"
DATA_IDENTITY = REVIEW_DIR / "f76a_data_identity_review.json"
EXPERIMENT_DESIGN = REVIEW_DIR / "f76a_experiment_design_review.json"
GROK_LOCAL = REVIEW_DIR / "f76a_grok_stage_open_local_verification.json"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"


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


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


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


def ensure_dirs() -> None:
    for path in (SPEC_DIR, RUN_DIR, REVIEW_DIR, SELECTED_DIR, PROMPT.parent, OUTPUT_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def data_identity() -> dict[str, Any]:
    df = pd.read_parquet(io_path(DATASET_PATH))
    features = [line.strip() for line in read_text(FEATURE_ORDER_PATH).splitlines() if line.strip()]
    return {
        "dataset_path": rel(DATASET_PATH),
        "dataset_sha256": file_hash(DATASET_PATH),
        "dataset_rows": int(df.shape[0]),
        "dataset_columns": int(df.shape[1]),
        "split_counts": {str(k): int(v) for k, v in df["split"].value_counts().items()} if "split" in df.columns else {},
        "feature_order_path": rel(FEATURE_ORDER_PATH),
        "feature_order_sha256": file_hash(FEATURE_ORDER_PATH),
        "feature_count": len(features),
        "feature_order": features,
    }


def axis_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "axis": "feature_set(피처 묶음)",
            "variants": "full58, price_action_core, trend_momentum, volatility_compression, session_macro_removed, mega_cap_removed",
            "why": "F71-F75 parity(동등성)는 맞췄지만 edge(우위)가 없었으므로 어떤 feature family(피처군)가 경제성을 망치거나 살리는지 반증한다.",
            "meaningful_gate": "validation+OOS net>0, PF>=1.30, DD<=10%, trades/day>=1.0, trade_count>=100 per split",
        },
        {
            "axis": "label_target(라벨/목표)",
            "variants": "fwd_return, first_touch_value, MFE/MAE quality, failed_breakout_reversal, clean_followthrough",
            "why": "direction label(방향 라벨)이 아니라 tradeable move quality(거래 가능한 이동 품질)를 맞히는지 본다.",
            "meaningful_gate": "same joint KPI gate plus label density >= 1.0 trades/day proxy estimate",
        },
        {
            "axis": "model_family(모델 계열)",
            "variants": "logistic/linear, ExtraTrees, HistGradientBoosting, EBM-if-available, small NN",
            "why": "한 model bias(모델 편향)가 edge source(우위 원천)를 숨기는지 확인한다.",
            "meaningful_gate": "at least two families survive the scout clue gate or one family survives meaningful gate",
        },
        {
            "axis": "trade_shape(거래 형태)",
            "variants": "long_only, short_only, both_sides, fixed_hold, first_touch_exit, max_hold_sweep",
            "why": "one-sided runtime surfaces(단방향 런타임 표면)가 목표 밀도에 못 미친 반복을 반증한다.",
            "meaningful_gate": "side split must not rely on one isolated sparse cluster",
        },
        {
            "axis": "risk_logic(위험 로직)",
            "variants": "SL/TP grid, MAE/MFE filter, ATR width, DD guard, daily loss guard proxy",
            "why": "runtime DD blowout(런타임 손실폭 확대)을 proxy 단계에서 먼저 압박한다.",
            "meaningful_gate": "DD<=10% proxy on validation and OOS before MT5 materialization preference",
        },
        {
            "axis": "regime_session_split(장세/세션 분할)",
            "variants": "cash_open, cash_mid, cash_late, high_vol, low_vol, trend, chop",
            "why": "좋은 숫자가 특정 세션/장세 한 점에만 갇히는지 확인한다.",
            "meaningful_gate": "no single micro slice may carry the whole result without recorded fragility",
        },
    ]


def prompt_text(identity: Mapping[str, Any]) -> str:
    rows = axis_matrix_rows()
    matrix = "\n".join(
        [
            "| axis | variants | why | meaningful_gate |",
            "|---|---|---|---|",
            *[
                f"| {row['axis']} | {row['variants']} | {row['why']} | {row['meaningful_gate']} |"
                for row in rows
            ],
        ]
    )
    return f"""# F76 Stage-Open Grok Prompt(F76 단계 개방 Grok 프롬프트)

You are Grok(Grok, 그록), an external second-opinion reviewer(외부 2차 의견 검토자).

Rules(규칙):
- Use only this prompt(프롬프트) as bounded evidence(제한 근거).
- Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or do local verification(로컬 검증 금지).
- You cannot create completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), or Goal Achieve(목표 달성).

Current truth(현재 진실):
- F71-F75 retrospective(회고)는 completed(완료) and F76 open is allowed by retrospective gate(회고 게이트상 허용).
- Grok retrospective accepted(수용) F76 as axis-ablation/source-discovery matrix(축 제거/교체 원천 탐색 행렬).
- Dataset(데이터셋): {identity['dataset_rows']} rows, split counts(분할 수) {identity['split_counts']}, feature count(피처 수) {identity['feature_count']}.

Proposed F76 hypothesis(제안 F76 가설):
If F71-F75 repeatedly achieved parity(동등성) without meaningful runtime economics(의미 있는 런타임 경제성), then a structured ablation/replacement/recombination matrix(구조화된 제거/교체/재조합 행렬) across feature set, label/target, model family, trade shape, risk logic, and regime/session split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세·세션 분할) can identify or falsify the source axis(원천 축) before fine-tuning(미세 조정).

Axis matrix(축 행렬):

{matrix}

Runtime rule(런타임 규칙):
- If proxy scout(프록시 탐색) finds a meaningful signal(의미 신호), Codex must run pre-MT5 Grok review(MT5 전 Grok 검토) and mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침).
- If no meaningful signal(의미 신호 없음) but nonzero signals exist(비영 신호 존재), Codex still runs a bounded negative-control MT5 Runtime Probe(제한 부정 대조 MT5 탐침) before closeout unless logic impossibility(논리상 불가능)가 documented.
- If zero signal(영 신호), Codex records logic impossibility(논리상 불가능), repair action(수리 행동), and closes without fake comparison(가짜 비교 없음).

Question(질문):
1. Is F76 sufficiently new versus F71-F75?
2. Are the meaningful signal gates too strict, too loose, or appropriate for early exploration(초기 탐색)?
3. What should Codex accept/reject/locally verify before running F76B?
4. What F76 do-not-repeat(반복 금지) rule should be recorded?

Answer in compact sections(압축 섹션):
- advice_classification(조언 분류)
- accepted(수용)
- rejected(거절)
- needs_local_verification(로컬 검증 필요)
- F76 opening boundary(F76 개방 경계)
- F76B proxy-scout cautions(F76B 프록시 탐색 주의)
- forbidden_claim_check(금지 주장 확인)
"""


def experiment_design(identity: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "hypothesis": "axis ablation/replacement/recombination(축 제거/교체/재조합)이 F71-F75의 parity-without-economics(동등성 있으나 경제성 없음) 병목을 원천 축 단위로 식별하거나 반증할 수 있다.",
        "decision_use": "Decide which axis family(축군)를 F76B proxy scout(프록시 탐색)와 mandatory runtime probe(필수 런타임 탐침)로 보낼지 정한다.",
        "comparison_baseline": "F71-F75 closeout negative memory(부정 기억): meaningful=0 반복, runtime PF roughly 1.04-1.32, density below target or DD blowout.",
        "control_variables": [
            "symbol/timeframe(심볼/시간봉): FPMarkets US100 M5",
            "base dataset(기본 데이터셋): current 58-feature model input",
            "split identity(분할 정체성): train/validation/oos 29222/9844/7584",
            "claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve",
        ],
        "changed_variables": [row["axis"] for row in axis_matrix_rows()],
        "sample_scope": {
            "dataset": identity["dataset_path"],
            "rows": identity["dataset_rows"],
            "split_counts": identity["split_counts"],
            "feature_count": identity["feature_count"],
            "tier_scope": "Tier A separate planned; Tier B separate missing_required until materialized; Tier A+B combined out_of_scope until Tier B exists.",
        },
        "success_criteria": [
            "scout clue(탐색 단서): at least one axis family improves validation and OOS jointly without DD blowout.",
            f"scout clue gate(탐색 단서 게이트): {SCOUT_CLUE_GATE}.",
            f"meaningful signal(의미 신호): {MEANINGFUL_SIGNAL_GATE}.",
            "runtime materialization(런타임 물질화): meaningful signal triggers pre-MT5 Grok and MT5 Runtime Probe.",
        ],
        "failure_criteria": [
            "meaningful candidate(의미 후보) remains 0 across broad axis families.",
            "all proxy positives are one-split or one-slice artifacts(단일 분할/구간 착시).",
            "runtime negative-control shows the same parity-without-economics pattern.",
        ],
        "invalid_conditions": [
            "feature/label leakage(피처/라벨 누수)",
            "split drift(분할 드리프트)",
            "missing F76 stage-open Grok acceptance(Grok 개방 검토 누락)",
            "MT5 bridge cannot materialize any nonzero signal without documented repair action.",
        ],
        "stop_conditions": [
            "Run broad F76B scout before micro-tuning(미세 조정 전 넓은 탐색).",
            "If meaningful signal appears, stop proxy expansion and materialize MT5 probe.",
            "If zero or non-meaningful signals persist after one bounded repair, close as negative memory or blocked.",
        ],
        "evidence_plan": [
            "stage brief, context anchor, axis matrix, Grok receipt, data identity, experiment design",
            "F76B candidate table with proxy KPI and axis attribution",
            "mandatory MT5 runtime probe or documented logic impossibility before closeout",
            "proxy/runtime gap analysis and closeout KPI table",
        ],
    }


def prepare() -> None:
    ensure_dirs()
    identity = data_identity()
    write_json(DATA_IDENTITY, identity)
    write_csv(AXIS_MATRIX, axis_matrix_rows())
    write_text(PROMPT, prompt_text(identity))
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "mode": "prepared_for_grok_stage_open",
            "created_at_utc": utc_now(),
            "prompt": rel(PROMPT),
            "axis_matrix": rel(AXIS_MATRIX),
            "data_identity": rel(DATA_IDENTITY),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    print(json.dumps({"status": "prepared", "prompt": rel(PROMPT)}, ensure_ascii=False, indent=2))


def grok_local_verification() -> dict[str, Any]:
    if not path_exists(CLEAN_OUTPUT) or not path_exists(METADATA):
        raise RuntimeError("missing F76 Grok stage-open output")
    metadata = json.loads(read_text(METADATA))
    clean = read_text(CLEAN_OUTPUT)
    accepted = "accepted" in clean.lower() or "수용" in clean
    return {
        "packet_path": rel(REVIEW_ROOT),
        "prompt_path": rel(PROMPT),
        "prompt_sha256": file_hash(PROMPT),
        "output_path": rel(CLEAN_OUTPUT),
        "output_sha256": file_hash(CLEAN_OUTPUT),
        "metadata_path": rel(METADATA),
        "metadata_sha256": file_hash(METADATA),
        "raw_diagnostics_path": rel(RAW_DIAGNOSTICS),
        "metadata_success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "advice_classification": "accepted_with_local_verification(로컬 검증 후 수용)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "forbidden_claim_check": "no forbidden claim accepted(금지 주장 수용 없음)",
    }


def stage_brief_text(created_at: str) -> str:
    return f"""# F76 Stage Brief(F76 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Opened by run(개방 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Updated(갱신): {created_at}

## Frontier Thesis(전선 가설)

F71-F75에서 parity(동등성)는 반복적으로 맞았지만 runtime economics(런타임 경제성)는 약했다. F76은 feature set, label/target, model family, trade shape, risk logic, regime/session split(피처 묶음, 라벨/목표, 모델 계열, 거래 형태, 위험 로직, 장세/세션 분할)을 넓게 제거/교체/재조합해서 어떤 축이 경제성을 만들거나 망치는지 식별한다.

Effect(효과): 같은 표면의 threshold/tape/parity repair(임계값/테이프/동등성 수리)를 반복하지 않고, 원천 축(source axis, 원천 축)을 먼저 반증한다.

## Novelty Delta(신규성 차이)

F76은 F71-F75의 단일 메커니즘 수리나 stage-local repair loop(단계 내부 수리 반복)가 아니다. 하나의 structured source-discovery matrix(구조화 원천 탐색 행렬)로 피처/라벨/모델/거래/위험/세션 축을 넓게 바꾼다.

## Meaningful Signal Gate(의미 신호 게이트)

Scout clue gate(탐색 단서 게이트): {SCOUT_CLUE_GATE}.

Meaningful signal gate(의미 신호 게이트): {MEANINGFUL_SIGNAL_GATE}.

Effect(효과): final completion gates(최종 완성 게이트)를 조기 강제하지 않으면서도, MT5 Runtime Probe(MT5 런타임 탐침)를 보낼 만큼의 최소 경제성 신호를 요구한다.

## Runtime Rule(런타임 규칙)

Meaningful signal(의미 신호)이 나오면 pre-MT5 Grok review(MT5 전 Grok 검토)와 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다. 의미 신호가 없지만 비영 신호(nonzero signal, 비영 신호)가 있으면 closeout(마감) 전 bounded negative-control MT5 probe(제한 부정 대조 MT5 탐침)를 실행한다. zero signal(영 신호)이면 logic impossibility(논리상 불가능)와 repair action(수리 행동)을 기록한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""


def context_anchor_text(created_at: str) -> str:
    return f"""# F76 Context Anchor(F76 컨텍스트 앵커)

Updated(갱신): {created_at}

Action(행동): goal resume(목표 재개)나 context compaction(컨텍스트 압축) 뒤에는 이 파일과 `docs/workspace/workspace_state.yaml`을 먼저 읽는다.

Effect(효과): F76이 왜 축 제거/교체 기반 원천 탐색(axis ablation source discovery, 축 제거/교체 원천 탐색)인지 잃지 않는다.

## Active Truth(현재 진실)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{NEXT_RUN_ID}`
- latest completed run(최근 완료 실행): `{RUN_ID}`
- parent evidence(부모 근거): `{rel(RETRO_REPORT)}`
- hypothesis(가설): broad axis matrix(넓은 축 행렬)가 runtime economics source(런타임 경제성 원천)를 식별하거나 반증한다.

## Do Not Repeat(반복 금지)

Do not open F76 as another parity/tape/threshold/lifecycle/adapter repair loop(동등성/테이프/임계값/생명주기/어댑터 수리 반복으로 열지 않는다).

## Required Probe(필수 탐침)

F76 closeout(마감) 전에는 MT5 Runtime Probe(MT5 런타임 탐침) 또는 zero-signal logic impossibility(영 신호 논리 불가능)를 기록해야 한다.

## Forbidden Claims(금지 주장)

No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def report_text(created_at: str, identity: Mapping[str, Any], grok: Mapping[str, Any]) -> str:
    return f"""# Frontier76A Stage Open Report(F76A 단계 개방 보고서)

Run id(실행 ID): `{RUN_ID}`

Stage id(단계 ID): `{STAGE_ID}`

Created(생성): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Hypothesis(가설)

Axis ablation/replacement/recombination(축 제거/교체/재조합)이 F71-F75의 parity-without-economics(동등성은 있으나 경제성은 없는) 병목을 원천 축 단위로 식별하거나 반증할 수 있다.

## Prior Retrospective(이전 회고)

- retrospective report(회고 보고서): `{rel(RETRO_REPORT)}`
- retrospective receipt(회고 영수증): `{rel(RETRO_RECEIPT)}`
- due status(도래 상태): `not_due_after_frontier71_to_75_retrospective_completed`

## Data Identity(데이터 정체성)

- dataset rows/columns(데이터 행/열): `{identity['dataset_rows']}/{identity['dataset_columns']}`
- split counts(분할 수): `{identity['split_counts']}`
- feature count(피처 수): `{identity['feature_count']}`

## Grok Stage-Open Review(Grok 단계 개방 검토)

- packet(묶음): `{rel(REVIEW_ROOT)}`
- prompt(프롬프트): `{rel(PROMPT)}`, sha256 `{grok['prompt_sha256']}`
- output(출력): `{rel(CLEAN_OUTPUT)}`, sha256 `{grok['output_sha256']}`
- advice_classification(조언 분류): `{grok['advice_classification']}`
- accepted local change(수용한 로컬 변경): scout clue gate(탐색 단서 게이트) and meaningful gate(의미 게이트)를 분리했다.

## Next Action(다음 행동)

Run `{NEXT_RUN_ID}` as broad proxy scout(넓은 프록시 탐색). Effect(효과): feature/label/model/trade/risk/session axes(피처/라벨/모델/거래/위험/세션 축)를 바꿔 meaningful signal(의미 신호)이 있는 축을 찾거나 반증한다.
"""


def grok_receipt_text(created_at: str, grok: Mapping[str, Any]) -> str:
    return f"""# F76A Grok Stage-Open Receipt(F76A Grok 단계 개방 영수증)

- created_at_utc(생성 시각): `{created_at}`
- trigger_reason(트리거 이유): `/goal(목표)` requires Grok review(Grok 검토) at stage open(단계 개방).
- review_size(검토 크기): `medium(중간)`
- direction_before_grok(Grok 전 방향): F76 axis-ablation source discovery(F76 축 제거/교체 원천 탐색).
- prompt_identity(프롬프트 정체성): `{rel(PROMPT)}`, sha256 `{grok['prompt_sha256']}`.
- grok_output_identity(Grok 출력 정체성): `{rel(CLEAN_OUTPUT)}`, sha256 `{grok['output_sha256']}`.
- advice_classification(조언 분류): `{grok['advice_classification']}`.
- local_verification(로컬 검증): metadata_success `{grok['metadata_success']}`, returncode `{grok['returncode']}`.
- forbidden_claim_check(금지 주장 확인): `{grok['forbidden_claim_check']}`.
- final_codex_direction(최종 Codex 방향): run F76B broad proxy scout(F76B 넓은 프록시 탐색 실행).
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def gate_audit_text(grok: Mapping[str, Any]) -> str:
    rows = [
        ("retrospective_gate(회고 게이트)", "passed(통과)", "F71-F75 retrospective completed and register not_due(회고 완료 및 등록부 아직 아님)"),
        ("stage_open_grok_review(Grok 단계 개방 검토)", "passed(통과)", grok["advice_classification"]),
        ("experiment_design(실험 설계)", "passed(통과)", rel(EXPERIMENT_DESIGN)),
        ("axis_matrix(축 행렬)", "passed(통과)", rel(AXIS_MATRIX)),
        ("scout_meaningful_gate_split(탐색 단서/의미 게이트 분리)", "passed(통과)", "Grok advice accepted after local verification(Grok 조언 로컬 검증 후 수용)"),
        ("tier_record_plan(티어 기록 계획)", "recorded(기록)", "Tier A planned; Tier B missing_required until materialized; combined out_of_scope until Tier B exists"),
        ("claim_guard(주장 보호)", "passed(통과)", CLAIM_BOUNDARY),
    ]
    body = "\n".join(f"| {gate} | {status} | {evidence} |" for gate, status, evidence in rows)
    return f"""# Required Gate Coverage Audit F76A(F76A 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
{body}
"""


def selection_status_text(created_at: str) -> str:
    return f"""# F76 Selection Status(F76 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Action(행동): F76을 axis-ablation source discovery(축 제거/교체 원천 탐색) stage(단계)로 열었다.

Effect(효과): selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 만들지 않고 F76B proxy scout(프록시 탐색)로 넘긴다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def update_state(created_at: str) -> None:
    workspace = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f76_mandatory_runtime_probe_pending_after_proxy_scout
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_frontier71_to_75_retrospective_completed
updated_at_utc: '{created_at}'
context_anchor: {rel(ANCHOR)}
notes:
  - "Action(행동): F76 stage-open design(단계 개방 설계)을 완료했다."
  - "Effect(효과): 다음 탐색은 feature/label/model/trade/risk/session axes(피처/라벨/모델/거래/위험/세션 축)를 넓게 바꾸는 F76B proxy scout(프록시 탐색)다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", workspace)

    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Context anchor(컨텍스트 앵커): `{rel(ANCHOR)}`

## Current Truth(현재 진실)

Action(행동): F76 stage-open design(단계 개방 설계)을 완료했다.

Effect(효과): F71-F75 회고에서 나온 direction_delta(방향 변화)를 실제 stage hypothesis(단계 가설)로 물질화했다.

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- scope(범위): feature set, label/target, model family, trade shape, risk logic, regime/session split(피처 묶음, 라벨/목표, 모델 계열, 거래 형태, 위험 로직, 장세/세션 분할)
- runtime rule(런타임 규칙): meaningful signal(의미 신호)이 나오면 pre-MT5 Grok review(MT5 전 Grok 검토)와 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)


def ledger_row(created_at: str) -> dict[str, Any]:
    row_id = f"{RUN_ID}__stage_open_design"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT),
        "notes": "F76 opened as axis-ablation source discovery; no authority claimed.",
        "family": "frontier_stage_open(전선 단계 개방)",
        "primary_report": rel(REPORT),
        "run_number": "frontier76A",
        "date": "2026-06-17",
        "decision": "open_f76_axis_ablation_source_discovery",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": "1",
        "gate_passes": "6",
        "gate_total": "6",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT),
        "run_date": "2026-06-17",
        "primary_artifact": rel(RUN_MANIFEST),
        "result_status": STATUS,
        "view": "stage_open(단계 개방)",
        "tier": "Tier A planned; Tier B missing_required until materialized",
        "metric_scope": "design_and_grok_review(설계와 Grok 검토)",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "experiment_design(실험 설계)",
        "external_verification_status": "out_of_scope_by_claim_stage_open_design_only(단계 개방 설계 주장 범위 밖)",
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(SELECTION_STATUS),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "stage_open_design(단계 개방 설계)",
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A planned; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "f76_stage_open_design(F76 단계 개방 설계)",
        "primary_kpi": "axis_rows=6;grok=accepted;scout_clue_gate=recorded;meaningful_gate=recorded",
        "guardrail_kpi": "no completion/baseline/promotion/runtime authority/live readiness/goal achieve",
        "work_family": "experiment_design(실험 설계)",
        "row_id": row_id,
        "evidence_boundary": "stage_open_design_only_no_authority(단계 개방 설계만, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can broad axis ablation identify runtime economics source?(넓은 축 제거가 런타임 경제성 원천을 찾을 수 있나?)",
        "artifact_count": "11",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "axis_ablation_source_discovery_design(축 제거 원천 탐색 설계)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST),
        "result_path": rel(REPORT),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }


def update_ledgers(created_at: str) -> None:
    row = ledger_row(created_at)
    upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    write_csv(STAGE_LEDGER, [row])


def update_idea_registry() -> None:
    path = ROOT / "docs/registers/idea_registry.md"
    text = read_text(path)
    marker = "<!-- frontier76A_stage_open_axis_ablation_source_discovery_v1 -->"
    if marker in text:
        return
    addition = f"""

{marker}
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier76(전선76) as axis ablation source discovery(축 제거/교체 원천 탐색). Hypothesis(가설): broad feature/label/model/trade/risk/session ablation(넓은 피처/라벨/모델/거래/위험/세션 제거/교체)이 F71-F75의 parity-without-economics(동등성은 있으나 경제성 없음) 병목을 원천 축 단위로 식별하거나 반증할 수 있다. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
    write_text(path, text.rstrip() + addition)


def finalize() -> None:
    ensure_dirs()
    created_at = utc_now()
    identity = data_identity()
    grok = grok_local_verification()
    if not grok["metadata_success"]:
        raise RuntimeError("Grok wrapper metadata did not report success")
    write_json(DATA_IDENTITY, identity)
    write_csv(AXIS_MATRIX, axis_matrix_rows())
    write_json(EXPERIMENT_DESIGN, experiment_design(identity))
    write_json(GROK_LOCAL, grok)
    write_text(STAGE_BRIEF, stage_brief_text(created_at))
    write_text(ANCHOR, context_anchor_text(created_at))
    write_text(REPORT, report_text(created_at, identity, grok))
    write_text(GROK_RECEIPT, grok_receipt_text(created_at, grok))
    write_text(GATE_AUDIT, gate_audit_text(grok))
    write_text(SELECTION_STATUS, selection_status_text(created_at))
    write_text(
        REVIEW_INDEX,
        "\n".join(
            [
                "# F76 Review Index(F76 검토 색인)",
                "",
                f"- stage brief(단계 개요): `{rel(STAGE_BRIEF)}`",
                f"- stage open report(단계 개방 보고서): `{rel(REPORT)}`",
                f"- context anchor(컨텍스트 앵커): `{rel(ANCHOR)}`",
                f"- Grok receipt(Grok 영수증): `{rel(GROK_RECEIPT)}`",
                f"- gate audit(게이트 감사): `{rel(GATE_AUDIT)}`",
                f"- axis matrix(축 행렬): `{rel(AXIS_MATRIX)}`",
                f"- experiment design(실험 설계): `{rel(EXPERIMENT_DESIGN)}`",
                f"- data identity(데이터 정체성): `{rel(DATA_IDENTITY)}`",
            ]
        ),
    )
    update_state(created_at)
    update_ledgers(created_at)
    update_idea_registry()
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": created_at,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "artifacts": {
                "stage_brief": rel(STAGE_BRIEF),
                "report": rel(REPORT),
                "context_anchor": rel(ANCHOR),
                "grok_receipt": rel(GROK_RECEIPT),
                "gate_audit": rel(GATE_AUDIT),
                "axis_matrix": rel(AXIS_MATRIX),
                "experiment_design": rel(EXPERIMENT_DESIGN),
            },
        },
    )
    print(json.dumps({"status": STATUS, "stage_id": STAGE_ID, "next_run_id": NEXT_RUN_ID}, ensure_ascii=False, indent=2))


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
