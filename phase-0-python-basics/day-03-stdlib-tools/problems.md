# Day 3 — 연습 문제 (Practice Problems)

컴프리헨션, collections, heapq, itertools, bisect 를 활용하는 실전 문제 모음.

---

## 🟢 문제 1 — Last Stone Weight (최대 힙 / max-heap)

| 항목 | 내용 |
|------|------|
| 출처 | LeetCode |
| 번호 | 1046 |
| 링크 | https://leetcode.com/problems/last-stone-weight/ |
| 카테고리 | 자료구조, 우선순위 큐, heapq (max-heap) |
| 난이도 | 🟢 Easy |

### 문제 요약

돌(stone) 무게 배열 `stones`가 주어진다. 매 턴 가장 무거운 두 돌 `y ≥ x`를 골라:
- `y == x` → 둘 다 소멸
- `y > x` → 무게 `y - x`인 돌이 남음

더 이상 돌이 1개 이하가 될 때까지 반복 후, 마지막 남은 돌의 무게를 반환하라 (없으면 0).

### 💭 힌트

- Python `heapq`는 **최소 힙**이므로 **부호 반전(-x)** 으로 최대 힙 구현
- 매 반복: `y = -heappop(h)`, `x = -heappop(h)` → 차이 `y-x > 0`이면 `-heappush(h, -(y-x))`
- 반복문 조건: `while len(h) > 1:`
- 시간 복잡도: O(N log N)

---

## 🟢 문제 2 — Top K Frequent Elements (Counter + heapq)

| 항목 | 내용 |
|------|------|
| 출처 | LeetCode |
| 번호 | 347 |
| 링크 | https://leetcode.com/problems/top-k-frequent-elements/ |
| 카테고리 | 해시, Counter, heapq |
| 난이도 | 🟢 Medium |

### 문제 요약

정수 배열 `nums`와 정수 `k`가 주어질 때, **빈도 상위 k개의 원소**를 반환하라. 순서는 무관.

예: `nums = [1,1,1,2,2,3], k = 2` → `[1, 2]`

### 💭 힌트

- `Counter(nums).most_common(k)` 한 줄로 해결 가능 (내부적으로 `heapq.nlargest` 사용)
- 또는 `Counter(nums)` → `heapq.nlargest(k, cnt, key=cnt.get)` 패턴
- 시간 복잡도: O(N log k) — N개 원소 중 k개만 힙으로 관리
- **리스트 컴프리헨션**으로 결과 추출: `[x for x, _ in cnt.most_common(k)]`

---

## 🟡 문제 3 — 모의고사 (완전탐색 + itertools.cycle)

| 항목 | 내용 |
|------|------|
| 출처 | 프로그래머스 (Programmers) |
| 번호 | 42840 |
| 링크 | https://school.programmers.co.kr/learn/courses/30/lessons/42840 |
| 카테고리 | 완전탐색, 규칙성, itertools.cycle |
| 난이도 | 🟡 Level 1 |

### 문제 요약

세 수포자가 각자의 패턴으로 찍은 답과 정답 배열을 비교해, **가장 많이 맞힌 수포자 번호**를 오름차순으로 반환하라.

- 수포자 1 패턴: `[1, 2, 3, 4, 5]` 반복
- 수포자 2 패턴: `[2, 1, 2, 3, 2, 4, 2, 5]` 반복
- 수포자 3 패턴: `[3, 3, 1, 1, 2, 2, 4, 4, 5, 5]` 반복

### 💭 힌트

- `itertools.cycle(pattern)` 으로 패턴을 무한 반복하는 이터레이터 생성
- 또는 `answers[i] == pattern[i % len(pattern)]` 인덱스 나머지(%) 방식
- `Counter` 또는 단순 리스트로 각 수포자 점수 집계 → `max()` 로 최고 점수
- 리스트 컴프리헨션으로 최고 점수와 같은 수포자 번호 필터링

---

## 🟡 문제 4 — 더 맵게 (heapq + 조건 반복)

| 항목 | 내용 |
|------|------|
| 출처 | 프로그래머스 (Programmers) |
| 번호 | 42626 |
| 링크 | https://school.programmers.co.kr/learn/courses/30/lessons/42626 |
| 카테고리 | 자료구조, 우선순위 큐, heapq |
| 난이도 | 🟡 Level 2 |

### 문제 요약

음식 스코빌 지수 배열 `scoville`과 기준 `K`가 주어진다.
스코빌 지수가 K 미만인 음식이 있으면, 가장 맵지 않은 두 음식을 섞는다:
- 새 스코빌 = `가장 안 매운 것 + (두 번째로 안 매운 것 × 2)`

모든 음식의 스코빌을 K 이상으로 만드는 **최소 혼합 횟수**를 반환하라 (불가능하면 -1).

### 💭 힌트

- `heapq.heapify(scoville)` 로 최소 힙 구성 → O(N)
- `while h[0] < K and len(h) >= 2:` 조건으로 반복
- `heappop` 두 번 → 계산 후 `heappush` → 카운트 증가
- 반복 후 `h[0] < K` 이면 불가능 → `-1` 반환
- 시간 복잡도: O(N log N)

---

## ⚫ 문제 5 — 베스트앨범 (Counter + defaultdict + 정렬)

| 항목 | 내용 |
|------|------|
| 출처 | 프로그래머스 (Programmers) — 카카오 스타일 해시 문제 |
| 번호 | 42579 |
| 링크 | https://school.programmers.co.kr/learn/courses/30/lessons/42579 |
| 카테고리 | 해시, Counter, defaultdict, 정렬 |
| 난이도 | ⚫ Level 3 |

### 문제 요약

스트리밍 사이트에서 장르별 **베스트 앨범**을 구성한다.
- 장르 내 **재생 횟수 합이 많은 장르**부터 수록
- 장르 내 **재생 횟수가 많은 곡**부터 최대 2곡 수록
- 재생 횟수 같으면 **고유 번호(인덱스) 낮은 곡** 먼저

`genres`, `plays` 배열이 주어질 때 수록 곡들의 **고유 번호 배열**을 반환하라.

### 💭 힌트

- `defaultdict(list)` 로 `genre_songs[장르] = [(재생수, 인덱스), ...]` 구성
- `Counter` 또는 `defaultdict(int)` 로 장르별 총 재생수 집계
- 총 재생수 내림차순으로 장르 정렬 → 각 장르에서 최대 2곡 추출
- 정렬 key: `sorted(genre_songs[g], key=lambda x: (-x[0], x[1]))` (재생수 내림, 인덱스 오름)

```
예시:
genres = ["classic", "pop", "classic", "classic", "pop"]
plays  = [500, 600, 150, 800, 2500]

장르별 총재생수: classic=1450, pop=3100
순서: pop(3100) > classic(1450)
pop 곡: (2500, 4), (600, 1) → [4, 1]
classic 곡: (800, 3), (500, 0) → [3, 0]
결과: [4, 1, 3, 0]
```

---

## 📌 문제별 관련 개념 요약

| 문제 | 출처 | 핵심 개념 | 복잡도 |
|------|------|-----------|--------|
| LC 1046 Last Stone Weight | LeetCode Easy | heapq max-heap (부호 반전) | O(N log N) |
| LC 347 Top K Frequent | LeetCode Medium | Counter + heapq.nlargest | O(N log k) |
| PGS 모의고사 | 프로그래머스 Lv.1 | itertools.cycle 또는 %, 리스트 컴프리헨션 | O(N) |
| PGS 더 맵게 | 프로그래머스 Lv.2 | heapq min-heap, 조건 반복 | O(N log N) |
| PGS 베스트앨범 | 프로그래머스 Lv.3 | defaultdict + Counter + 다중 키 정렬 | O(N log N) |

→ 해설 및 다중 접근 방식 비교: `solutions.py` 참고
