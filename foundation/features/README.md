# Features

Put reusable contract-aligned feature helpers here.

This folder is for shared logic, not stage-local experiments.

## Current Helpers(현재 도우미)

- `session_calendar.py`: converts raw broker-clock timestamp keys(원천 브로커 시계 타임스탬프 키) into event UTC(이벤트 UTC) and New York session time(뉴욕 세션 시간), then computes US cash-session features(미국 정규장 피처).
