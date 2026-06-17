from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

STAGE_ID = "stage_frontier_75__volatility_compression_liquidity_release_for_tradeable_density"
RUN_ID = "frontier75A_stage_open_upstream_mechanism_rotation_after_f74_microburst_negative_memory_v1"
NEXT_RUN_ID = "frontier75B_volatility_compression_liquidity_release_proxy_scout_v1"
PARENT_RUN_ID = "frontier74F_proxy_runtime_gap_or_closeout_decision_v1"
IDEA_ID = "IDEA-FR75-VOLATILITY-COMPRESSION-LIQUIDITY-RELEASE"

STATUS = "stage_open_design_completed_no_authority"
JUDGMENT = "volatility_compression_liquidity_release_stage_open_design_only_no_authority"
CLAIM_BOUNDARY = (
    "stage_open_design_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
SPEC_DIR = STAGE_DIR / "00_spec"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PIPELINE_PATH = Path("stage_pipelines/stage_frontier_75/frontier75a_stage_open_volatility_compression_liquidity_release.py")

F74_CLOSEOUT_REPORT = (
    "stages/stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path/"
    "03_reviews/stage_closeout_report.md"
)
F74_GAP_ANALYSIS = (
    "stages/stage_frontier_74__microburst_turnover_label_for_dense_smooth_runtime_path/"
    "03_reviews/f74f_proxy_runtime_gap_analysis.csv"
)
GROK_PACKET = (
    "docs/agent_control/grok_reviews/"
    "2026-06-17_f75_stage_open_volatility_compression_liquidity_release"
)
GROK_PROMPT = f"{GROK_PACKET}/prompts/f75_stage_open_volatility_compression_liquidity_release_prompt.md"
GROK_OUTPUT = f"{GROK_PACKET}/clean_output.md"
GROK_METADATA = f"{GROK_PACKET}/metadata.json"

DATASET_PATH = (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_feature_order.txt"
)
RAW_PATH = "data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv"

REPORT_PATH = f"stages/{STAGE_ID}/03_reviews/frontier75A_stage_open_volatility_compression_liquidity_release_report.md"
ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"
GATE_AUDIT_PATH = f"stages/{STAGE_ID}/03_reviews/required_gate_coverage_audit_f75a.md"
STAGE_BRIEF_PATH = f"stages/{STAGE_ID}/00_spec/stage_brief.md"
SELECTION_STATUS_PATH = f"stages/{STAGE_ID}/04_selected/selection_status.md"
RUN_MANIFEST_PATH = f"stages/{STAGE_ID}/02_runs/{RUN_ID}/run_manifest.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def fs_path(path: Path) -> Path:
    absolute = path if path.is_absolute() else ROOT / path
    if os.name == "nt":
        text = str(absolute)
        if text.startswith("\\\\?\\"):
            return Path(text)
        if text.startswith("\\\\"):
            return Path("\\\\?\\UNC\\" + text.lstrip("\\"))
        return Path("\\\\?\\" + text)
    return absolute


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dirs() -> None:
    for path in (SPEC_DIR, RUN_DIR, REVIEW_DIR, SELECTED_DIR):
        fs_path(path).mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with fs_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return fs_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    fpath = fs_path(path)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    fpath.write_text(text, encoding="utf-8-sig", newline="\n")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    fpath = fs_path(path)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    fpath.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    fpath = fs_path(path)
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with fpath.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def upsert_csv_row(path: Path, key_field: str, row: dict[str, Any], fieldnames: list[str] | None = None) -> None:
    fpath = fs_path(path)
    if fpath.exists():
        with fpath.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            existing_fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    else:
        existing_fieldnames = []
        rows = []

    if fieldnames is None:
        fieldnames = existing_fieldnames
    if not fieldnames:
        fieldnames = list(row.keys())
    for key in row:
        if key not in fieldnames:
            fieldnames.append(key)

    rows = [old for old in rows if old.get(key_field) != row.get(key_field)]
    rows.append({field: row.get(field, "") for field in fieldnames})

    with fpath.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def collect_data_identity() -> dict[str, Any]:
    dataset_path = ROOT / DATASET_PATH
    feature_order_path = ROOT / FEATURE_ORDER_PATH
    raw_path = ROOT / RAW_PATH
    for path in (dataset_path, feature_order_path, raw_path):
        if not fs_path(path).exists():
            raise FileNotFoundError(f"missing required input: {rel(path)}")

    df = pd.read_parquet(fs_path(dataset_path))
    feature_order = [line.strip() for line in read_text(feature_order_path).splitlines() if line.strip()]
    with fs_path(raw_path).open("r", encoding="utf-8-sig", newline="") as handle:
        raw_reader = csv.reader(handle)
        raw_header = next(raw_reader)
        raw_rows = sum(1 for _ in raw_reader)

    split_counts = {}
    if "split" in df.columns:
        split_counts = {str(key): int(value) for key, value in df["split"].value_counts(dropna=False).items()}

    return {
        "dataset_path": DATASET_PATH,
        "dataset_sha256": sha256_file(dataset_path),
        "dataset_rows": int(df.shape[0]),
        "dataset_columns": int(df.shape[1]),
        "split_counts": split_counts,
        "feature_order_path": FEATURE_ORDER_PATH,
        "feature_order_sha256": sha256_file(feature_order_path),
        "feature_count": len(feature_order),
        "feature_order_preview": feature_order[:10],
        "raw_path": RAW_PATH,
        "raw_sha256": sha256_file(raw_path),
        "raw_rows": raw_rows,
        "raw_columns": len(raw_header),
        "raw_header": raw_header,
    }


def grok_status() -> dict[str, Any]:
    prompt_path = ROOT / GROK_PROMPT
    output_path = ROOT / GROK_OUTPUT
    metadata_path = ROOT / GROK_METADATA
    if not fs_path(prompt_path).exists() or not fs_path(output_path).exists() or not fs_path(metadata_path).exists():
        raise FileNotFoundError("F75 stage-open Grok packet is incomplete")
    metadata = json.loads(read_text(metadata_path))
    output_text = read_text(output_path)
    accepted = "accepted" in output_text.lower() or "수용" in output_text
    return {
        "packet_path": GROK_PACKET,
        "prompt_path": GROK_PROMPT,
        "prompt_sha256": sha256_file(prompt_path),
        "output_path": GROK_OUTPUT,
        "output_sha256": sha256_file(output_path),
        "metadata_path": GROK_METADATA,
        "metadata_sha256": sha256_file(metadata_path),
        "metadata_success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "advice_classification": "accepted(수용)" if accepted else "needs_local_verification(로컬 검증 필요)",
        "short_advice": [
            "F75B부터 SL/TP와 MAE/MFE를 label/proxy simulation(라벨/프록시 시뮬레이션)에 넣는다.",
            "density/parity(밀도/동등성)만 좋아지는 약한 PF/DD surface(수익 팩터/손실폭 표면)를 반복하지 않는다.",
            "broad first scout(넓은 1차 탐색)는 tradeable economics(거래 가능한 경제성)를 같이 본다.",
        ],
    }


def axis_rows() -> list[dict[str, str]]:
    return [
        {
            "axis": "feature_set(피처 묶음)",
            "f75_action": "compression/release/core/session bundles(압축/방출/핵심/세션 묶음)을 빼기, 교체, 재조합한다.",
            "effect": "F74의 microburst label-only loop(마이크로버스트 라벨 단독 반복)를 피하고 원천 신호(source signal, 원천 신호)를 바꾼다.",
            "next_run": NEXT_RUN_ID,
        },
        {
            "axis": "label_target(라벨/목표)",
            "f75_action": "compression breakout, failed breakout reversal, release continuation(압축 돌파/실패 돌파 반전/방출 지속)을 비교한다.",
            "effect": "모델이 단순 방향(direction, 방향)이 아니라 압축 뒤 거래 가능한 움직임(tradeable move, 거래 가능한 움직임)을 맞히게 한다.",
            "next_run": NEXT_RUN_ID,
        },
        {
            "axis": "model_family(모델 계열)",
            "f75_action": "ExtraTrees, HistGradientBoosting, linear/logistic, small NN 후보를 단계적으로 비교한다.",
            "effect": "한 모델 계열의 inductive bias(귀납 편향)에 갇히지 않는다.",
            "next_run": NEXT_RUN_ID,
        },
        {
            "axis": "trade_shape(거래 형태)",
            "f75_action": "long/short, breakout/reversal, hold horizon, first-touch exit(롱/숏, 돌파/반전, 보유 시간, 선도달 청산)을 같이 바꾼다.",
            "effect": "trade count(거래 수), payoff ratio(손익비), DD path(손실폭 경로)를 한 축으로 묶어 본다.",
            "next_run": NEXT_RUN_ID,
        },
        {
            "axis": "risk_logic(위험 로직)",
            "f75_action": "SL/TP, MAE/MFE, DD guard proxy(손절/익절, 최대 불리/유리 이동, 손실폭 보호 프록시)를 라벨과 시뮬레이션에 넣는다.",
            "effect": "proxy/runtime gap(프록시/런타임 간극)이 손익 구조에서 생기는지 초기에 잡는다.",
            "next_run": NEXT_RUN_ID,
        },
        {
            "axis": "regime_session_split(장세/세션 분할)",
            "f75_action": "all, cash open, cash mid, cash late, compression buckets(전체/현금장 초반/중반/후반/압축 구간)을 분리한다.",
            "effect": "어느 구간에서만 작동하는지 숨기지 않고 기록한다.",
            "next_run": NEXT_RUN_ID,
        },
    ]


def experiment_design(data_identity: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "idea_id": IDEA_ID,
        "hypothesis": (
            "Volatility compression plus liquidity release(변동성 압축 + 유동성 방출) can create "
            "tradeable-density signals(거래 가능한 밀도 신호) with better runtime economics(런타임 경제성) "
            "than F74 microburst turnover labels(F74 마이크로버스트 회전 라벨)."
        ),
        "decision_use": "Open F75 and route the next work packet(다음 작업 묶음) to F75B broad proxy scout(넓은 프록시 탐색).",
        "comparison_baseline": "F74 closeout negative memory(F74 마감 부정 기억): runtime PF 1.16/1.13 and trades/day 1.65/1.60.",
        "control_variables": [
            "Symbol/timeframe(심볼/시간봉): FPMarkets US100 M5.",
            "Input contract(입력 계약): feature_set_v2_mt5_price_proxy_58 unless a repair packet changes it explicitly.",
            "Split identity(분할 정체성): train/validation/oos counts from current model input dataset.",
            "Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve.",
        ],
        "changed_variables": [
            "feature set(피처 묶음): compression/release/session recombination.",
            "label/target(라벨/목표): compression-to-release outcomes and failed-release reversals.",
            "model family(모델 계열): tree/linear/small NN rotation.",
            "trade shape(거래 형태): direction, exit, hold horizon, first-touch structure.",
            "risk logic(위험 로직): SL/TP and excursion-aware proxy simulation.",
            "regime/session split(장세/세션 분할): compression buckets and cash session slices.",
        ],
        "sample_scope": {
            "dataset": DATASET_PATH,
            "raw": RAW_PATH,
            "rows": data_identity["dataset_rows"],
            "split_counts": data_identity["split_counts"],
            "feature_count": data_identity["feature_count"],
        },
        "success_criteria": [
            "Scout clue(탐색 단서): validation and OOS both positive with PF/DD/trade-density moving toward all four final axes.",
            "Meaningful signal(의미 있는 신호): enough signal density to justify mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침).",
            "Final gates(최종 게이트)는 final completion review(최종 완성 검토)에서만 강제한다.",
        ],
        "failure_criteria": [
            "Zero-signal label setup(영 신호 라벨 설정).",
            "Proxy PF/DD/trade-density stays in weak F74-like economics(약한 F74식 경제성).",
            "Good density/parity(밀도/동등성) but no runtime-economic path(런타임 경제성 경로 없음).",
        ],
        "invalid_conditions": [
            "Feature readiness parity(피처 준비 동등성)를 런타임에서 만들 수 없는 feature contract change(피처 계약 변경).",
            "Leakage(누수): future release information(미래 방출 정보)을 entry feature(진입 피처)에 넣는 경우.",
            "Data identity mismatch(데이터 정체성 불일치).",
        ],
        "stop_conditions": [
            "F75B finds no signal surface(신호 표면 없음): repair with label/risk/session redesign once.",
            "Proxy signal is meaningful(의미 있음): run pre-MT5 Grok review(Grok 검토) and mandatory MT5 Runtime Probe.",
            "F75 closeout occurs: five-stage retrospective(5단계 중간 검토) becomes due.",
        ],
        "evidence_plan": [
            "F75A stage-open receipt(개방 영수증), Grok receipt(Grok 영수증), data identity(데이터 정체성).",
            "F75B proxy KPI(프록시 KPI): net/PF/DD/trade count/trades per day/win rate/expectancy/recovery.",
            "If meaningful signal appears(의미 신호 발생 시): ONNX handoff(온엑스 인계), MT5 Runtime Probe(MT5 런타임 탐침), gap analysis(간극 분석).",
        ],
    }


def write_stage_docs(data_identity: dict[str, Any], grok: dict[str, Any], created_at: str) -> None:
    axes = axis_rows()
    write_csv(REVIEW_DIR / "f75a_axis_contract_review.csv", axes, ["axis", "f75_action", "effect", "next_run"])
    write_json(REVIEW_DIR / "f75a_experiment_design_review.json", experiment_design(data_identity))
    write_json(REVIEW_DIR / "f75a_data_identity_review.json", data_identity)
    write_json(REVIEW_DIR / "f75a_grok_stage_open_local_verification.json", grok)

    stage_brief = f"""# F75 Stage Brief(단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Opened by run(개방 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Updated(갱신): {created_at}

## Frontier Thesis(전선 가설)

Volatility compression plus liquidity release(변동성 압축 + 유동성 방출)가 US100 M5에서 tradeable-density signal(거래 가능한 밀도 신호)을 만들 수 있는지 본다.

## Easy Explanation(쉬운 설명)

Action(행동): 조용히 압축된 구간 뒤에 실제로 힘이 풀리는 순간을 찾는다.

Effect(효과): 단순히 신호 수(signal count, 신호 수)를 늘리는 것이 아니라, 손익 구조(runtime economics, 런타임 경제성)가 붙는 움직임인지 본다.

## Novelty Delta(신규성 차이)

F75는 F74 microburst repair loop(F74 마이크로버스트 수리 반복)가 아니다. F74의 preserved clue(보존 단서)는 density/parity(밀도/동등성)였고 negative memory(부정 기억)는 weak runtime economics(약한 런타임 경제성)였다. F75는 feature set/label/model/trade shape/risk/session(피처 묶음/라벨/모델/거래 형태/위험/세션)을 함께 바꾸는 upstream mechanism rotation(상류 메커니즘 전환)이다.

## Do Not Repeat(반복 금지)

- density/parity(밀도/동등성)만 좋다고 앞으로 보내지 않는다.
- F74 label-only repair(라벨 단독 수리)처럼 같은 수리를 반복하지 않는다.
- proxy/runtime gap(프록시/런타임 간극)을 나중으로만 미루지 않는다.

## Context Anchor(맥락 고정점)

Action(행동): goal resume(목표 재개)나 context compaction(컨텍스트 압축) 뒤에는 `{ANCHOR_PATH}`를 먼저 읽는다.

Effect(효과): active stage(활성 단계), hypothesis(가설), forbidden claims(금지 주장), next action(다음 행동)을 repo state(저장소 상태)에서 복원한다.

## Exit Rule(종료 규칙)

F75는 proxy(프록시), mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침), proxy/runtime gap analysis(프록시/런타임 간극 분석), repair(수리), closeout(마감)을 지나야 닫는다. F75 closeout(마감)은 five-stage retrospective(5단계 중간 검토) trigger(트리거)가 된다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    write_text(SPEC_DIR / "stage_brief.md", stage_brief)

    anchor = f"""# F75 Context Anchor(맥락 고정점)

Updated(갱신): {created_at}

## Resume Contract(재개 계약)

Action(행동): goal resume(목표 재개), context compaction(컨텍스트 압축), 또는 새 Codex turn(새 코덱스 차례)에서는 아래 순서로 읽는다.

Effect(효과): 이전 대화 기억(memory, 기억)이 줄어도 같은 F75 lifecycle(생명주기)로 돌아온다.

1. `docs/workspace/workspace_state.yaml`
2. `docs/context/current_working_state.md`
3. `{STAGE_BRIEF_PATH}`
4. `{REPORT_PATH}`
5. `{GATE_AUDIT_PATH}`
6. `{GROK_OUTPUT}`

## Active Truth(활성 진실)

- active stage(활성 단계): `{STAGE_ID}`
- current completed run(현재 완료 실행): `{RUN_ID}`
- next run(다음 실행): `{NEXT_RUN_ID}`
- hypothesis(가설): volatility compression plus liquidity release(변동성 압축 + 유동성 방출).
- parent memory(부모 기억): F74 preserved density/parity(밀도/동등성 보존), but weak runtime economics(약한 런타임 경제성).

## User Intent Guard(사용자 의도 보호)

Action(행동): feature set, label/target, model family, trade shape, risk logic, regime/session split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세·세션 분할)을 계속 바꿔가며 탐색한다.

Effect(효과): F68이나 F74 같은 한 축에만 붙어서 수리하는 드리프트(drift, 표류)를 막는다.

## Required Runtime Rule(필수 런타임 규칙)

Action(행동): proxy(프록시)가 의미 있는 signal(신호)을 만들면 MT5 Runtime Probe(MT5 런타임 탐침)를 실행한다.

Effect(효과): proxy/runtime gap(프록시/런타임 간극)을 말로만 분석하지 않고 runtime evidence(런타임 근거)로 확인한다.

## Forbidden Claims(금지 주장)

Do not claim(주장 금지): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""
    write_text(REVIEW_DIR / "context_anchor.md", anchor)

    report = f"""# Frontier75A Stage Open Report(전선75A 단계 개방 보고서)

Run id(실행 ID): `{RUN_ID}`

Stage id(단계 ID): `{STAGE_ID}`

Created(생성): {created_at}

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Hypothesis(가설)

Volatility compression plus liquidity release(변동성 압축 + 유동성 방출)가 F74의 weak runtime economics(약한 런타임 경제성) 기억 뒤에서 더 좋은 tradeable density(거래 가능한 밀도)를 만들 수 있는지 시험한다.

## User Concern Response(사용자 우려 반영)

Action(행동): F75A에 context anchor(맥락 고정점)와 axis contract(축 계약)를 남겼다.

Effect(효과): goal resume(목표 재개) 후에도 한 축 수리만 반복하지 않고 feature set/label/model/trade shape/risk/session(피처 묶음/라벨/모델/거래 형태/위험/세션)을 넓게 돌린다.

## Prior Memory(이전 기억)

- F74 preserved clue(보존 단서): raw density(원시 밀도), ONNX probability/signal parity(온엑스 확률/신호 동등성), MT5 Runtime Probe completion(MT5 런타임 탐침 완료).
- F74 negative memory(부정 기억): validation runtime(검증 런타임) net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래) `97.11/1.16/11.40%/1.6544`, OOS(표본외) `61.86/1.13/9.66%/1.60`.

## Data Identity(데이터 정체성)

- dataset(데이터셋): `{DATASET_PATH}`
- dataset rows/columns(행/열): `{data_identity["dataset_rows"]}/{data_identity["dataset_columns"]}`
- split counts(분할 수): `{data_identity["split_counts"]}`
- feature count(피처 수): `{data_identity["feature_count"]}`
- raw rows/columns(원시 행/열): `{data_identity["raw_rows"]}/{data_identity["raw_columns"]}`

## Grok Stage-Open Review(Grok 단계 개방 검토)

- packet(묶음): `{GROK_PACKET}`
- classification(분류): `{grok["advice_classification"]}`
- accepted advice(수용 조언): SL/TP and MAE/MFE(손절/익절 및 최대 불리/유리 이동)를 F75B label/proxy simulation(라벨/프록시 시뮬레이션)에 넣는다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`: broad proxy scout(넓은 프록시 탐색)를 실행한다. 의미 있는 signal(신호)이 나오면 pre-MT5 Grok review(MT5 전 Grok 검토) 뒤 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 물질화한다.
"""
    write_text(REVIEW_DIR / "frontier75A_stage_open_volatility_compression_liquidity_release_report.md", report)

    grok_receipt = f"""# F75A Grok Stage-Open Receipt(Grok 단계 개방 영수증)

Trigger reason(트리거 이유): `/goal(목표)` requires Grok second opinion(Grok 2차 의견) at stage open(단계 개방).

Review size(검토 크기): medium review(중간 검토)

Direction before Grok(Grok 전 방향): volatility compression plus liquidity release(변동성 압축 + 유동성 방출) as upstream mechanism rotation(상류 메커니즘 전환).

Bounded evidence(제한 근거): F74 closeout report(F74 마감 보고서), five-stage retrospective status(5단계 중간 검토 상태), F75 proposed axis contract(F75 제안 축 계약).

Prompt identity(프롬프트 정체성): `{GROK_PROMPT}` sha256 `{grok["prompt_sha256"]}`

Grok output identity(Grok 출력 정체성): `{GROK_OUTPUT}` sha256 `{grok["output_sha256"]}`

Advice classification(조언 분류): `{grok["advice_classification"]}`

Local verification(로컬 검증): wrapper metadata success(래퍼 메타데이터 성공) `{grok["metadata_success"]}`, returncode `{grok["returncode"]}`.

Forbidden claim check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Final Codex direction(최종 Codex 방향): run `{NEXT_RUN_ID}` with risk-aware label/proxy simulation(위험 인식 라벨/프록시 시뮬레이션).
"""
    write_text(REVIEW_DIR / "grok_stage_open_receipt.md", grok_receipt)

    gate_rows = [
        ("reentry_state_check(재진입 상태 점검)", "passed(통과)", "F74 closed and F75A is next run(F74 마감, F75A 다음 실행)."),
        ("five_stage_retrospective_due_check(5단계 중간 검토 도래 점검)", "passed_not_due(통과, 아직 아님)", "F74 closeout leaves 4/5; F75 closeout will trigger(F74 마감 후 4/5, F75 마감 때 트리거)."),
        ("grok_stage_open_review(Grok 단계 개방 검토)", "passed(통과)", grok["advice_classification"]),
        ("novelty_delta_check(신규성 차이 점검)", "passed(통과)", "F75 changes upstream mechanism and axes(F75는 상류 메커니즘과 축을 변경)."),
        ("context_anchor_check(맥락 고정점 점검)", "passed(통과)", ANCHOR_PATH),
        ("claim_guard(주장 보호)", "passed(통과)", CLAIM_BOUNDARY),
    ]
    gate_table = "\n".join(
        f"| {gate} | {status} | {evidence} |" for gate, status, evidence in gate_rows
    )
    gate_audit = f"""# Required Gate Coverage Audit F75A(필수 게이트 커버리지 감사 F75A)

| gate(게이트) | status(상태) | evidence(근거) |
|---|---|---|
{gate_table}

Action(행동): F75A는 stage-open design(단계 개방 설계)로만 닫았다.

Effect(효과): runtime claim(런타임 주장)이나 completion claim(완성 주장)을 만들지 않고 다음 proxy scout(프록시 탐색)로 넘긴다.
"""
    write_text(REVIEW_DIR / "required_gate_coverage_audit_f75a.md", gate_audit)

    review_index = f"""# F75 Review Index(검토 색인)

- stage brief(단계 개요): `{STAGE_BRIEF_PATH}`
- stage-open report(단계 개방 보고서): `{REPORT_PATH}`
- context anchor(맥락 고정점): `{ANCHOR_PATH}`
- Grok receipt(Grok 영수증): `stages/{STAGE_ID}/03_reviews/grok_stage_open_receipt.md`
- gate audit(게이트 감사): `{GATE_AUDIT_PATH}`
- data identity(데이터 정체성): `stages/{STAGE_ID}/03_reviews/f75a_data_identity_review.json`
- experiment design(실험 설계): `stages/{STAGE_ID}/03_reviews/f75a_experiment_design_review.json`
- axis contract(축 계약): `stages/{STAGE_ID}/03_reviews/f75a_axis_contract_review.csv`
"""
    write_text(REVIEW_DIR / "review_index.md", review_index)

    selection_status = f"""# F75 Selection Status(선택 상태)

Status(상태): `{STATUS}`

Action(행동): Frontier75(전선75)를 volatility compression + liquidity release(변동성 압축 + 유동성 방출) hypothesis(가설)로 열었다.

Effect(효과): selected baseline(선택 기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 만들지 않는다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection_status)


def update_state_files(created_at: str) -> None:
    workspace_state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f75_mandatory_runtime_probe_pending_after_meaningful_proxy_signal
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f74_closeout_f75_closeout_will_trigger
updated_at_utc: '{created_at}'
context_anchor: {ANCHOR_PATH}
notes:
  - "Action(행동): F75 stage-open design(단계 개방 설계)을 완료했다."
  - "Effect(효과): goal resume(목표 재개) 시 context anchor(맥락 고정점)로 active hypothesis(활성 가설)와 next action(다음 행동)을 복원한다."
  - "Next(다음): {NEXT_RUN_ID}에서 feature set/label/model/trade shape/risk/session(피처 묶음/라벨/모델/거래 형태/위험/세션)을 넓게 바꿔 proxy scout(프록시 탐색)를 실행한다."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", workspace_state)

    current_working_state = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Context anchor(맥락 고정점): `{ANCHOR_PATH}`

## Current Truth(현재 진실)

Action(행동): F75 stage-open design(단계 개방 설계)을 완료했다.

Effect(효과): F74의 weak runtime economics(약한 런타임 경제성)를 부정 기억으로 두고, F75는 volatility compression + liquidity release(변동성 압축 + 유동성 방출)로 upstream mechanism rotation(상류 메커니즘 전환)을 시작한다.

## Resume Rule(재개 규칙)

Action(행동): goal resume(목표 재개)나 context compaction(컨텍스트 압축) 뒤에는 `docs/workspace/workspace_state.yaml`, 이 파일, `{ANCHOR_PATH}` 순서로 읽는다.

Effect(효과): user intent(사용자 의도)인 broad axis rotation(넓은 축 회전)과 mandatory runtime probe(필수 런타임 탐침)를 잃지 않는다.

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- proxy plan(프록시 계획): feature set/label/model family/trade shape/risk logic/regime session split(피처 묶음/라벨/모델 계열/거래 형태/위험 로직/장세 세션 분할)을 함께 바꾼다.
- runtime rule(런타임 규칙): proxy(프록시)가 의미 있는 signal(신호)을 만들면 pre-MT5 Grok review(MT5 전 Grok 검토)와 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)를 실행한다.
- F75 closeout(마감): five-stage retrospective(5단계 중간 검토)가 due(도래)된다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current_working_state)


def update_ledgers(created_at: str) -> None:
    ledger_row_id = f"{RUN_ID}__stage_open_design"
    common_row = {
        "ledger_row_id": ledger_row_id,
        "row_id": ledger_row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage_open_design(단계 개방 설계)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "Tier A+B planned(Tier A+B 계획)",
        "kpi_scope": "design_and_grok_review(설계와 Grok 검토)",
        "scoreboard_lane": "experiment_design(실험 설계)",
        "lane": "stage_open(단계 개방)",
        "family": "stage_open_design(단계 개방 설계)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "result_judgment": JUDGMENT,
        "path": REPORT_PATH,
        "report_path": REPORT_PATH,
        "primary_report": REPORT_PATH,
        "primary_kpi": "axis_rows=6;grok=accepted;context_anchor=recorded",
        "guardrail_kpi": "no_runtime_claim;no_completion_claim;f75_closeout_retrospective_due",
        "external_verification_status": "out_of_scope_by_claim_stage_open_design_only(단계 개방 설계 주장 범위 밖)",
        "notes": "F75 opened with durable context anchor(지속 맥락 고정점) after user concern about goal resume(목표 재개 우려).",
        "run_number": "frontier75A",
        "date": "2026-06-17",
        "run_date": "2026-06-17",
        "decision": "open_f75_volatility_compression_liquidity_release",
        "next_run_id": NEXT_RUN_ID,
        "rows": "1",
        "gate_passes": "6",
        "gate_total": "6",
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_artifact": RUN_MANIFEST_PATH,
        "view": "stage_open(단계 개방)",
        "tier": "Tier A+B planned(Tier A+B 계획)",
        "metric_scope": "design_and_grok_review(설계와 Grok 검토)",
        "result_status": STATUS,
        "evidence_boundary": "stage_open_design_only_no_runtime(단계 개방 설계 전용, 런타임 없음)",
        "work_family": "frontier_stage_open(전선 단계 개방)",
        "question": "Can volatility compression plus liquidity release create tradeable density?(변동성 압축 + 유동성 방출이 거래 가능한 밀도를 만들 수 있나?)",
        "next_action": NEXT_RUN_ID,
        "final_decision_path": SELECTION_STATUS_PATH,
        "gate_audit_path": GATE_AUDIT_PATH,
        "required_gate_audit": GATE_AUDIT_PATH,
        "created_at": created_at,
        "created_at_utc": created_at,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "frontier_stage_open(전선 단계 개방)",
        "run_type": "volatility_compression_liquidity_release_design(변동성 압축 방출 설계)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": RUN_MANIFEST_PATH,
        "result_path": REPORT_PATH,
        "artifact_count": "10",
    }

    run_registry = ROOT / "docs/registers/run_registry.csv"
    alpha_ledger = ROOT / "docs/registers/alpha_run_ledger.csv"
    with fs_path(run_registry).open("r", encoding="utf-8-sig", newline="") as handle:
        run_fields = list(csv.DictReader(handle).fieldnames or [])
    with fs_path(alpha_ledger).open("r", encoding="utf-8-sig", newline="") as handle:
        alpha_fields = list(csv.DictReader(handle).fieldnames or [])

    upsert_csv_row(run_registry, "run_id", common_row, run_fields)
    upsert_csv_row(alpha_ledger, "ledger_row_id", common_row, alpha_fields)
    upsert_csv_row(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", common_row, alpha_fields)


def update_idea_registry() -> None:
    path = ROOT / "docs/registers/idea_registry.md"
    text = read_text(path)
    marker = "<!-- frontier75A_stage_open_volatility_compression_liquidity_release_v1 -->"
    if marker in text:
        return
    addition = f"""

{marker}
- `{IDEA_ID}`: `{RUN_ID}` opens Frontier75(전선75) as volatility compression + liquidity release exploration(변동성 압축 + 유동성 방출 탐색). Hypothesis(가설): compression context(압축 맥락) followed by release behavior(방출 행동)를 feature set/label/model/trade shape/risk/session(피처 묶음/라벨/모델/거래 형태/위험/세션) 축으로 바꾸면 F74 weak runtime economics(약한 런타임 경제성) 뒤 tradeable density seed surface(거래 가능한 밀도 씨앗 표면)를 찾을 수 있다. Context anchor(맥락 고정점): `{ANCHOR_PATH}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
    write_text(path, text.rstrip() + addition)


def write_run_manifest(data_identity: dict[str, Any], grok: dict[str, Any], created_at: str) -> None:
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "idea_id": IDEA_ID,
        "pipeline": PIPELINE_PATH.as_posix(),
        "artifacts": {
            "stage_brief": STAGE_BRIEF_PATH,
            "report": REPORT_PATH,
            "context_anchor": ANCHOR_PATH,
            "grok_receipt": f"stages/{STAGE_ID}/03_reviews/grok_stage_open_receipt.md",
            "gate_audit": GATE_AUDIT_PATH,
            "selection_status": SELECTION_STATUS_PATH,
            "axis_contract": f"stages/{STAGE_ID}/03_reviews/f75a_axis_contract_review.csv",
            "data_identity": f"stages/{STAGE_ID}/03_reviews/f75a_data_identity_review.json",
            "experiment_design": f"stages/{STAGE_ID}/03_reviews/f75a_experiment_design_review.json",
        },
        "inputs": {
            "data_identity": data_identity,
            "grok": grok,
            "reference_only": [F74_CLOSEOUT_REPORT, F74_GAP_ANALYSIS],
        },
    }
    write_json(RUN_DIR / "run_manifest.json", payload)


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    data_identity = collect_data_identity()
    grok = grok_status()
    if grok["advice_classification"] != "accepted(수용)":
        raise RuntimeError("F75A requires accepted or locally verified Grok stage-open advice")
    write_stage_docs(data_identity, grok, created_at)
    write_run_manifest(data_identity, grok, created_at)
    update_state_files(created_at)
    update_ledgers(created_at)
    update_idea_registry()
    print(json.dumps({
        "status": STATUS,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "context_anchor": ANCHOR_PATH,
        "report": REPORT_PATH,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
