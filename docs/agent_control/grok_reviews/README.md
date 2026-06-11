# Grok Reviews(그록 리뷰)

이 폴더는 Grok Build(그록 빌드)를 external reviewer/coworker(외부 검토자/협업자)로 호출한 결과를 한 곳에서 관리한다.

- review(리뷰)는 YYYY-MM-DD_topic(날짜_주제) 폴더 단위로 분리한다.
- 각 review(리뷰)는 inputs/, prompts/, outputs/, logs/, metadata/를 가진다.
- Grok 결과는 authority(권위)가 아니라 external opinion(외부 의견)이며, Codex가 장부(register, 등록부), 파일시스템(filesystem, 파일시스템), git(깃)으로 재검산한다.
