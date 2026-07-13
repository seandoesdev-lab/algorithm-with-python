# 매일 Day 콘텐츠 생성 루틴 (Obsidian MCP)

대상 Vault: **deepdive** (옵시디언 MCP `list-available-vaults`로 확인).
프로젝트 폴더: Vault 안의 `algorithm-with-python/`.
작성 양식: [[Day-Template]] (`templates/Day-Template.md`).

## 도구 사용 원칙 (중요)
- 노트/파일 작성은 **옵시디언 MCP**를 사용한다:
  - `mcp__obsidian__create-note` (vault="deepdive", folder="algorithm-with-python/<phase>/<day-folder>", filename=...)
  - 읽기 `mcp__obsidian__read-note`, 수정 `mcp__obsidian__edit-note`(append/prepend/replace), 검색 `mcp__obsidian__search-vault`.
- **폴백:** 옵시디언 MCP 서버가 불안정/미연결이면, 동일한 Vault 경로(`E:/deepDive/algorithm-with-python/...`)에 파일을 직접 기록한다. 결과물(디스크의 .md/.py)은 동일하다.

## 수행 절차
1. `algorithm-with-python/curriculum.md`를 읽고 위에서부터 첫 번째 `⬜ 예정` Day를 찾는다.
   - 없으면(개념 집중기 종료): 직전 Day들을 보고 다음 유형/기출 주제를 정해 curriculum 2단계 표에 새 행을 추가한 뒤 그 Day를 대상으로 한다.
2. 해당 Day 상태를 `🛠 생성중`으로 바꾼다.
3. 해당 Day 폴더에 4개 파일을 생성한다.
   - **concept.md** — [[Day-Template]] 양식을 그대로 따른다:
     - YAML 프론트매터: `day, phase, title, category[], difficulty, status:done, prev, next, related[], sources[], tags[]`
     - 콜아웃 9종(순서 고정, 접힘 `-`): `[!abstract] 한눈 요약` / `[!note]- 정의·직관` / `[!gear]- 동작 원리` / `[!chart]- 복잡도(표)` / `[!tip]- 팁(WebSearch 출처)` / `[!warning]- 필수 상식` / `[!example]- 예제([examples.py](examples.py))` / `[!question]- 연습문제([problems.md](problems.md))` / `[!check]- 해설([solutions.py](solutions.py))`
     - 끝에 `## 🔗 관계` 섹션: 이전(prev)/다음(next)/관련(related, 각 한 줄 이유)/지도([[Phase-N MOC]] · [[00 Algorithm MOC]]).
     - 개념 집중기(Phase 0~3)에서는 모든 콜아웃을 매우 자세히 채운다(개발자 필수 상식 포함).
   - **examples.py / problems.md / solutions.py** — 기존 규칙대로.
4. **문서 관계 정의(필수):**
   - 프론트매터 `prev`(이전 Day)·`next`(다음 Day)·`related`(개념 연관 Day, 아직 없는 Day로도 링크)를 채운다. 링크 형식 `[[day-XX-폴더명/concept|Day XX — 주제]]`.
   - `tags`에 `phase/N`, `topic/<주제>` 부여.
   - 해당 Phase MOC(`Phase-N MOC.md`)와 `00 Algorithm MOC.md`의 목록에 이 Day 링크를 추가한다(`mcp__obsidian__edit-note` append 또는 직접 수정).
5. `examples.py`와 `solutions.py`를 `PYTHONIOENCODING=cp949 python <파일>`로 실행해 에러가 없는지 확인한다.
6. Day 상태를 `✅ 완료`로, `README.md` 체크박스를 `- [x]`로 갱신한다.
7. **git 커밋(필수).** 모든 파일 생성·진도 갱신을 마친 뒤 자동으로 커밋한다:
   `git add -A && git commit -m "feat: add Day NN - <주제>"`.
   - 커밋 메시지 끝에 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` 한 줄을 포함한다.
   - 기본 브랜치(main)에 직접 커밋한다(이 저장소는 매일 콘텐츠를 main에 누적하는 학습 저널이다).
   - 원격 push는 사용자가 요청할 때만 한다.

## 품질 기준
- 한국어 설명 + 핵심 용어 영어 병기.
- 코드는 표준 라이브러리만.
- **문제 출처는 프로그래머스(programmers.co.kr)·LeetCode(leetcode.com)만.** 백준 등 stdin 기반·삼성 SW역량 미사용. 번호·링크는 WebSearch로 실제 확인.
- solutions.py는 플랫폼 시그니처(LeetCode `class Solution` / 프로그래머스 `def solution`)에 assert 자체 테스트. 가능하면 한 문제 다중 접근 + 복잡도 비교.
- **cp949 콘솔 안전:** `.py`의 `print` 출력 문자열에 cp949 미지원 문자(em대시 —, 박스선 ═, ✓, ✗, 이모지) 금지 → `=`/`-`/`O`/`X` 같은 ASCII. (한글 OK. 이모지·특수기호는 `.md`에만.)

## 참고
- 진도 단일 출처는 `curriculum.md`.
- 환경에 따라 Write/Bash 전 "Fact-Forcing Gate"가 사실 확인을 요구할 수 있다(작업 요약 + 파일 역할 제시 후 재시도).
