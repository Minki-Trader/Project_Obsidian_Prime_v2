# Encoding Guard Update Review(인코딩 방지 규칙 업데이트 검토)

Role(역할): external second opinion(외부 2차 의견) only.

Observed repeated mistakes(관찰된 반복 실수):
- Grok wrapper(그록 래퍼)는 content files(내용 파일)를 썼지만 Windows console(윈도우 콘솔) stdout print failed with UnicodeEncodeError cp949.
- Some copied stage scripts generated mojibake(깨진 문자) in Korean report templates after mechanical copy/rewrite.
- PowerShell path/list operations also hit Windows long-path failures, already covered by long path guard.

Proposed durable rule(제안 지속 규칙):
- Before running Python/Grok commands that may print Korean or Unicode, set PYTHONIOENCODING=utf-8 and PYTHONPATH=.(파이썬 입출력 인코딩/모듈 경로).
- Prefer prompt-file or UTF-8 file artifacts(프롬프트 파일/UTF-8 산출물) for Grok prompts instead of large inline PowerShell here-strings when Korean fidelity matters.
- If apply_patch fails because copied text is mojibake, treat it as encoding repair(인코딩 수리), rewrite function-bounded templates mechanically, then py_compile and inspect generated report artifacts.
- Add this to AGENTS.md and obsidian-environment-reproducibility skill(재현성 스킬), without weakening gates or thresholds.

Question(질문): Is this durable rule acceptable? Any concise wording to add?

Answer briefly with accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요).
