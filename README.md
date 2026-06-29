# 파이썬 알고리즘 with 매일 학습 (Algorithm with Python)

파이썬 알고리즘·자료구조를 **기초부터 대기업 공채 코딩테스트 기출까지** 매일 한 단계씩 학습하는 저장소입니다.

## 학습 방법

1. **1단계 개념 집중기 (Day 1~30, 약 한 달):** 자료구조·핵심 알고리즘 개념을 매우 자세하게 학습합니다.
2. **2단계 문제 풀이기 (Day 31~):** 매일 유형·난이도별 문제를 풀고, 대기업 기출로 실전 감각을 키웁니다.

매일 하나의 Day 폴더에는 4개의 파일이 있습니다.

| 파일 | 내용 |
|---|---|
| `concept.md` | 개념 설명 (한국어 + 영어 용어 병기) |
| `examples.py` | 실행 가능한 예제 코드 |
| `problems.md` | 난이도·카테고리별 연습문제 (출처 링크 포함) |
| `solutions.py` | 해설 — 여러 접근 방식을 코드로 비교 |

## 자동 생성

매일 아침 8시, Claude 스케줄 루틴이 [curriculum.md](curriculum.md)에서 다음 Day를 찾아 자동으로 콘텐츠를 생성합니다.

## 전체 로드맵

- **Phase 0** 파이썬 코테 기초 (Day 1~5)
- **Phase 1** 자료구조 기초 (Day 6~15)
- **Phase 2** 알고리즘 기초 (Day 16~23)
- **Phase 3** 탐색·그래프 (Day 24~30)
- **Phase 4** 심화 알고리즘 (Day 31~, 문제 풀이기에 통합)
- **Phase 5** 대기업 코테 실전 (지속)

전체 일자별 목록은 [curriculum.md](curriculum.md)를 참고하세요.

## 진도 체크리스트

### Phase 0. 파이썬 코테 기초
- [x] Day 01 — 빠른 입출력 (Fast I/O)
- [x] Day 02 — 자료형과 컬렉션 (Types & Collections)
- [x] Day 03 — 컴프리헨션·표준 라이브러리
- [x] Day 04 — 문자열 다루기
- [x] Day 05 — 수학·진법·비트 기초

### Phase 1. 자료구조 기초
- [x] Day 06 — 배열과 동적 리스트
- [x] Day 07 — 스택
- [x] Day 08 — 큐와 덱
- [x] Day 09 — 해시 (dict/set)
- [x] Day 10 — 연결 리스트
- [x] Day 11 — 트리 기본
- [x] Day 12 — 힙·우선순위 큐
- [x] Day 13 — 해시맵 응용
- [x] Day 14 — 누적 합
- [x] Day 15 — 자료구조 종합 복습

### Phase 2. 알고리즘 기초
- [x] Day 16 — 시간복잡도와 Big-O
- [ ] Day 17 — 정렬
- [ ] Day 18 — 이분 탐색
- [ ] Day 19 — 투 포인터
- [ ] Day 20 — 슬라이딩 윈도우
- [ ] Day 21 — 그리디
- [ ] Day 22 — 재귀와 분할정복
- [ ] Day 23 — 알고리즘 기초 복습

### Phase 3. 탐색·그래프
- [ ] Day 24 — 완전 탐색
- [ ] Day 25 — DFS
- [ ] Day 26 — BFS
- [ ] Day 27 — 백트래킹
- [ ] Day 28 — 그래프 표현과 순회
- [ ] Day 29 — 트리 순회·응용
- [ ] Day 30 — 개념 집중기 종합 복습

### 2단계 — 문제 풀이기 (Day 31~)
- 스케줄 루틴이 진행하며 추가합니다.

## 디렉토리 구조

```
.
├─ README.md
├─ curriculum.md
├─ phase-0-python-basics/ ~ phase-5-real-coding-test/
├─ templates/day-template/
├─ utils/io_helper.py
└─ scripts/daily_prompt.md
```
