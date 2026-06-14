---
day: 3
phase: phase-0-python-basics
title: 컴프리헨션·표준 라이브러리 (Comprehension & Stdlib)
category: [표준라이브러리]
difficulty: 기초
status: done
prev: [[day-02-collections/concept|Day 02 — 자료형과 컬렉션]]
next: [[day-04-strings/concept|Day 04 — 문자열 다루기]]
related:
  - "[[day-02-collections/concept|Day 02 — 자료형과 컬렉션]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
sources:
  - https://leetcode.com/problems/last-stone-weight/
  - https://leetcode.com/problems/top-k-frequent-elements/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42840
  - https://school.programmers.co.kr/learn/courses/30/lessons/42626
  - https://school.programmers.co.kr/learn/courses/30/lessons/42579
tags: [phase/0, topic/stdlib]
---

# Day 03 — 컴프리헨션·표준 라이브러리 (Comprehension & Stdlib)

> [!abstract] 한눈 요약 (TL;DR)
> 컴프리헨션은 for+append보다 10~30% 빠른 단행 컬렉션 생성 문법이고, 제너레이터 표현식은 지연 평가로 메모리를 절약한다. `collections`(deque·Counter·defaultdict), `heapq`(최소 힙), `itertools`(순열·조합·누적합), `bisect`(이진 탐색)는 코딩 테스트에서 반복적으로 등장하는 핵심 표준 라이브러리다.

> [!note]- 1. 정의와 직관
>
> ### 학습 목표
>
> - 리스트/딕셔너리/셋 컴프리헨션과 제너레이터 표현식의 문법 및 메모리 동작 방식을 이해한다.
> - `collections` 모듈(deque, Counter, defaultdict), `heapq`, `itertools`, `bisect` 의 핵심 API를 익힌다.
> - 각 자료구조·함수의 시간 복잡도(time complexity)를 알고, 코딩 테스트에서 언제 어떤 것을 쓸지 판단한다.
> - 최소 힙(min-heap) 원리와 최대 힙(max-heap) 구현 방법을 설명할 수 있다.
>
> ### 컴프리헨션 (Comprehension)
>
> 컴프리헨션은 반복 가능한(iterable) 객체로부터 새로운 컬렉션을 **한 줄로** 만드는 Python 문법이다.
>
> **리스트 컴프리헨션**: CPython 인터프리터 내부에서 `LIST_APPEND` 바이트코드 명령 하나로 처리되어, 일반 for 루프의 `LOAD_ATTR`(append 속성 조회) + `CALL_FUNCTION` 오버헤드가 없어 10~30% 빠르다.
>
> **딕셔너리 컴프리헨션**: `{k: v for k, v in ...}` 형태로 키-값 쌍을 한 줄로 생성.
>
> **셋 컴프리헨션**: `{expr for x in ...}` 형태로 중복 없는 집합을 한 줄로 생성.
>
> **중첩 컴프리헨션**: `[val for row in matrix for val in row]` — 2D 행렬을 평탄화(flatten).
>
> ### 제너레이터 표현식 (Generator Expression)
>
> | 구분 | 리스트 컴프리헨션 | 제너레이터 표현식 |
> |------|-------------------|-------------------|
> | 메모리 | **모든 원소를 즉시 메모리에 적재** | **지연 평가(lazy evaluation)** — 원소를 요청할 때만 생성 |
> | 반환 타입 | `list` | `generator` 객체 |
> | 재사용 | 여러 번 순회 가능 | **한 번만** 순회 가능(소진되면 빈 반복자) |
>
> 100만 개짜리 리스트가 필요 없고 `sum()` 이나 `max()` 등 한 번만 소비하면 된다면 제너레이터로 메모리를 절약한다: `total = sum(x**2 for x in range(1_000_000))`
>
> ### collections 모듈
>
> **deque**: 양방향 큐(double-ended queue). `appendleft`/`popleft` 모두 O(1). BFS(너비 우선 탐색)에서 큐로 반드시 사용해야 한다 — `list.pop(0)`은 O(n).
>
> **Counter**: 원소의 **빈도(frequency)**를 세는 딕셔너리 서브클래스. `most_common(k)` 로 상위 k개 반환. Counter끼리 덧셈/뺄셈/교집합/합집합 연산 가능.
>
> **defaultdict**: 존재하지 않는 키에 접근할 때 **기본값을 자동 생성**하는 딕셔너리. `KeyError` 없이 그래프 인접 리스트, 단어 빈도 세기 등에 활용.
>
> ### heapq — 최소 힙 (Min-Heap)
>
> Python의 `heapq` 모듈은 **리스트를 최소 힙(min-heap)으로** 다룬다. 힙(heap)은 부모 노드가 항상 자식보다 작거나 같은 완전 이진 트리(complete binary tree)다.
>
> **최대 힙 구현**: `heapq`는 최소 힙만 지원한다. 최대 힙을 구현하려면 값을 넣을 때 **부호를 반전(-x)**하면 된다.
>
> **우선순위 큐**: 튜플 `(우선순위, 값)`을 넣으면 첫 번째 원소 기준으로 정렬된다.
>
> ### itertools
>
> 반복 관련 이터레이터를 생성하는 표준 라이브러리. **제너레이터 기반**이라 메모리 효율이 좋다.
>
> - `permutations(n, r)`: 순열 — 순서 있음, 중복 없음. P(n,r) = n!/(n-r)!
> - `combinations(n, r)`: 조합 — 순서 없음, 중복 없음. C(n,r) = n!/(r!(n-r)!)
> - `product`: 데카르트 곱(Cartesian Product). `repeat=k`로 중복 순열 구현.
> - `accumulate`: 누적 연산 (기본: 누적 합). 구간 합, 구간 곱에 활용.
>
> ### bisect — 이진 탐색 삽입
>
> **정렬된 리스트**에 대해 O(log n)으로 삽입 위치를 찾거나 원소를 삽입한다.
> - `bisect_left(a, x)`: x와 같은 값이 있을 때 그 **왼쪽(앞)** 인덱스 반환
> - `bisect_right(a, x)`: x와 같은 값이 있을 때 그 **오른쪽(뒤)** 인덱스 반환
> - **활용**: 값이 x인 원소의 개수 = `bisect_right(a, x) - bisect_left(a, x)`

> [!gear]- 2. 동작 원리
>
> ### 컴프리헨션 vs for 루프 — CPython 바이트코드 수준
>
> ```python
> # 리스트 컴프리헨션 — LIST_APPEND 바이트코드 1개
> squares = [x**2 for x in range(10)]
>
> # 딕셔너리 컴프리헨션 — 키와 값을 뒤집기
> word_len = {w: len(w) for w in ["apple", "banana", "cherry"]}
> inv = {v: k for k, v in word_len.items()}
>
> # 셋 컴프리헨션 — 중복 자동 제거
> unique_lens = {len(w) for w in ["apple", "banana", "cherry"]}  # {5, 6}
>
> # 중첩 컴프리헨션 — 2D 행렬 평탄화
> matrix = [[1,2,3],[4,5,6],[7,8,9]]
> flat = [val for row in matrix for val in row]
> ```
>
> ### deque 내부 동작
>
> ```python
> from collections import deque
>
> dq = deque([1, 2, 3])
> dq.appendleft(0)   # [0, 1, 2, 3]  — O(1)
> dq.append(4)       # [0, 1, 2, 3, 4]  — O(1)
> dq.popleft()       # 0 반환, [1, 2, 3, 4]  — O(1)
>
> # maxlen: 슬라이딩 윈도우(sliding window) 구현
> window = deque(maxlen=3)   # 최대 3개 유지; 초과 시 반대쪽 자동 제거
> ```
>
> ### Counter 연산
>
> ```python
> from collections import Counter
>
> c = Counter("abracadabra")
> # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})
> c.most_common(2)   # [('a', 5), ('b', 2)]
> c['z']             # 0 — KeyError 없음
>
> c1 = Counter("aab")
> c2 = Counter("abc")
> c1 + c2   # Counter({'a': 3, 'b': 2, 'c': 1})
> c1 - c2   # Counter({'a': 1})  — 양수만 남음
> ```
>
> ### defaultdict 패턴
>
> ```python
> from collections import defaultdict
>
> graph = defaultdict(list)   # 그래프 인접 리스트
> graph[1].append(2)          # KeyError 없이 바로 append
> graph[1].append(3)
>
> freq = defaultdict(int)     # 단어 빈도 카운팅
> for ch in "hello":
>     freq[ch] += 1
> ```
>
> ### heapq 동작
>
> ```python
> import heapq
>
> h = []
> heapq.heappush(h, 3); heapq.heappush(h, 1); heapq.heappush(h, 4)
> heapq.heappop(h)    # 1  — 항상 최솟값 반환
>
> # 최대 힙 — 부호 반전
> h = []
> for x in [3, 1, 4, 1, 5]:
>     heapq.heappush(h, -x)
> max_val = -heapq.heappop(h)  # 5
>
> # 우선순위 큐 — (우선순위, 값) 튜플
> tasks = []
> heapq.heappush(tasks, (2, "task B"))
> heapq.heappush(tasks, (1, "task A"))
> heapq.heappop(tasks)   # (1, 'task A')
> ```
>
> ### itertools 동작
>
> ```python
> from itertools import permutations, combinations, product, accumulate
> import operator
>
> list(permutations([1, 2, 3], 2))
> # [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]  — 순서 있음, P(3,2)=6
>
> list(combinations([1, 2, 3], 2))
> # [(1,2),(1,3),(2,3)]  — 순서 없음, C(3,2)=3
>
> list(product([0,1], repeat=3))   # 중복 순열 8가지
>
> list(accumulate([1, 2, 3, 4]))            # [1, 3, 6, 10]  — 누적 합
> list(accumulate([1, 2, 3, 4], operator.mul))  # [1, 2, 6, 24]  — 누적 곱
> ```
>
> ### bisect 동작
>
> ```python
> import bisect
>
> a = [1, 3, 5, 7, 9]
> bisect.bisect_left(a, 5)    # 2
> bisect.bisect_right(a, 5)   # 3
> bisect.insort(a, 6)          # [1, 3, 5, 6, 7, 9]  — 정렬 유지 삽입 O(n) 주의
> ```

> [!chart]- 3. 복잡도 (시간/공간)
>
> | 도구 | 연산 | 시간 복잡도 | 주요 사용 시나리오 |
> |------|------|-------------|-------------------|
> | list comprehension | 생성 | O(n) | 변환된 새 리스트 필요할 때 |
> | generator expression | 소비 | O(1) per step | 한 번만 순회, 메모리 절약 |
> | `deque.appendleft/popleft` | 양끝 삽입/삭제 | **O(1)** | BFS 큐, 슬라이딩 윈도우 |
> | `list.pop(0)` | 앞 삭제 | **O(n)** — 사용 금지 | — |
> | `Counter` | 빈도 집계 | O(n) | 문자 빈도, 애너그램 |
> | `Counter.most_common(k)` | 상위 k개 | O(n log k) | 최빈값 |
> | `defaultdict` | 기본값 조회/생성 | O(1) avg | 그래프 인접 리스트 |
> | `heappush` | 힙 삽입 | O(log n) | 우선순위 큐 |
> | `heappop` | 최솟값 추출 | O(log n) | 다익스트라, k번째 최솟값 |
> | `heapify` | 리스트→힙 변환 | **O(n)** | 초기 힙 구성 |
> | `permutations(n,r)` | 순열 생성 | O(P(n,r)) | 완전탐색 순열 |
> | `combinations(n,r)` | 조합 생성 | O(C(n,r)) | 완전탐색 조합 |
> | `product` | 데카르트 곱 | O(결과 수) | 중복 순열, 격자 탐색 |
> | `accumulate` | 누적 연산 | O(n) | 구간 합, 구간 곱 |
> | `bisect_left/right` | 삽입 위치 탐색 | **O(log n)** | 정렬 리스트 탐색 |
> | `insort` | 정렬 유지 삽입 | O(n) (이동) | 작은 정렬 리스트 유지 |

> [!tip]- 💡 이해를 돕는 팁
>
> 코딩 테스트 준비 시 아래 키워드로 검색하면 실전 정리 글을 찾을 수 있다:
>
> - **"코딩테스트 자주 쓰는 파이썬 표준 라이브러리"**
>   - 참고: https://velog.io/@ledcku/Python-%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8%EC%97%90-%EC%9E%90%EC%A3%BC-%EC%93%B0%EB%8A%94-%ED%91%9C%EC%A4%80-%EB%9D%BC%EC%9D%B4%EB%B8%8C%EB%9F%AC%EB%A6%AC
>
> - **"python heapq 최대힙"**
>   - 참고: https://docs.python.org/ko/3/library/heapq.html (공식 문서 — max-heap 구현 패턴 예시 포함)
>
> - **"파이썬 itertools 조합 순열 코딩테스트"**
>   - 참고: https://docs.python.org/ko/3/library/itertools.html
>
> - **"파이썬 bisect 이진탐색"**
>   - 참고: https://docs.python.org/ko/3/library/bisect.html
>
> 팁: 공식 문서(docs.python.org/ko)는 한국어로 제공되며 코드 예제가 포함돼 있어 학습에 매우 유용하다.

> [!warning]- ⚠️ 개발자 필수 상식
>
> 1. **heapq는 최소 힙뿐** → 최대 힙은 **부호 반전(-x)** 후 push, pop 시 다시 부호 반전.
>    ```python
>    heapq.heappush(h, -x)
>    max_val = -heapq.heappop(h)
>    ```
>
> 2. **리스트 pop(0)은 O(n)** → BFS/큐에서 절대 `list.pop(0)` 쓰지 말고 `deque.popleft()` 사용.
>
> 3. **Counter.most_common(k)** — 인수를 생략하면 모든 원소를 빈도 내림차순으로 반환. k를 지정하면 내부적으로 `heapq.nlargest`를 사용해 O(n log k) 로 동작.
>
> 4. **컴프리헨션이 for+append보다 빠른 이유** — CPython 바이트코드 차원에서 `LIST_APPEND` 명령어 하나로 처리 가능해 `list.append` 속성 조회(LOAD_ATTR) + 함수 호출(CALL_FUNCTION) 오버헤드가 없다. 일반적으로 **10~40% 빠름**.
>
> 5. **combinations vs permutations**:
>    - `combinations([1,2,3], 2)` → `(1,2), (1,3), (2,3)` — 순서 무관, C(3,2)=3가지
>    - `permutations([1,2,3], 2)` → `(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)` — 순서 관련, P(3,2)=6가지
>
> 6. **bisect_left vs bisect_right** 차이: `[1, 2, 2, 3]` 에서 2 검색 시
>    - `bisect_left` → 1 (첫 번째 2의 위치)
>    - `bisect_right` → 3 (마지막 2 다음 위치)
>
> 7. **defaultdict vs dict.setdefault**: 기능상 유사하나 `defaultdict`가 더 간결하고 빠르다. `dict.setdefault(key, []).append(val)` vs `dd[key].append(val)`.
>
> 8. **제너레이터는 한 번만 소비 가능**: `list()` 로 변환하거나 두 번 순회가 필요하면 리스트를 써야 한다.

> [!example]- 예제 코드
>
> ```python
> from collections import deque, Counter, defaultdict
> import heapq
> from itertools import permutations, combinations, accumulate
> import bisect
>
> # 컴프리헨션
> squares = [x**2 for x in range(10)]
> evens   = [x for x in range(20) if x % 2 == 0]
> total   = sum(x**2 for x in range(1_000_000))  # 제너레이터 — 메모리 절약
>
> # Counter
> c = Counter("abracadabra")
> print(c.most_common(2))  # [('a', 5), ('b', 2)]
>
> # heapq — 최대 힙 (부호 반전)
> h = []
> for x in [3, 1, 4, 1, 5]:
>     heapq.heappush(h, -x)
> print(-heapq.heappop(h))  # 5
>
> # bisect — 정렬 리스트에서 탐색
> a = [1, 3, 5, 7, 9]
> print(bisect.bisect_left(a, 5))   # 2
> print(bisect.bisect_right(a, 5))  # 3
> ```
>
> 전체 실행 예제: [examples.py](examples.py)

> [!question]- 연습문제
>
> | # | 문제 | 플랫폼 | 난이도 | 핵심 개념 |
> |---|---|---|---|---|
> | 1 | Last Stone Weight | LeetCode #1046 | 🟢 Easy | heapq max-heap (부호 반전) |
> | 2 | Top K Frequent Elements | LeetCode #347 | 🟢 Medium | Counter + heapq.nlargest |
> | 3 | 모의고사 | 프로그래머스 Lv.1 | 🟡 중급 | itertools.cycle 또는 %, 리스트 컴프리헨션 |
> | 4 | 더 맵게 | 프로그래머스 Lv.2 | 🟡 중급 | heapq min-heap, 조건 반복 |
> | 5 | 베스트앨범 | 프로그래머스 Lv.3 | ⚫ 기출 | defaultdict + Counter + 다중 키 정렬 |
>
> 전체 문제 목록 및 힌트: [problems.md](problems.md)

> [!check]- 해설
>
> 각 문제의 접근법, 복잡도 분석, 다중 풀이 비교는 [solutions.py](solutions.py) 참고.

---
## 🔗 관계 (Relationships)

- ⬅️ 이전: [[day-02-collections/concept|Day 02 — 자료형과 컬렉션]]
- ➡️ 다음: [[day-04-strings/concept|Day 04 — 문자열 다루기]]
- 🧭 관련:
  - [[day-02-collections/concept|Day 02 — 자료형과 컬렉션]] — 기본 자료형 확장 (Counter·defaultdict의 상속 관계)
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — deque의 BFS 활용 심화, 큐 ADT와 원형 큐
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — Counter·defaultdict의 내부 해시 테이블 동작 원리
- 🗺️ 지도: [[Phase-0 MOC]] · [[00 Algorithm MOC]]
