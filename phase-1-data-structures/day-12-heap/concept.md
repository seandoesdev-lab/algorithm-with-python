---
day: 12
phase: 1-data-structures
title: 힙·우선순위 큐 (Heap & Priority Queue)
category: [자료구조, 힙]
difficulty: 기초
status: done
prev: "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
next: "[[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]]"
related:
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-10-linked-list/concept|Day 10 — 연결 리스트]]"
  - "[[day-17-sorting/concept|Day 17 — 정렬]]"
  - "[[day-21-greedy/concept|Day 21 — 그리디]]"
  - "[[day-26-bfs/concept|Day 26 — BFS]]"
sources:
  - https://docs.python.org/3/library/heapq.html
  - https://leetcode.com/problems/last-stone-weight/
  - https://leetcode.com/problems/kth-largest-element-in-an-array/
  - https://leetcode.com/problems/kth-largest-element-in-a-stream/
  - https://leetcode.com/problems/top-k-frequent-elements/
  - https://leetcode.com/problems/k-closest-points-to-origin/
  - https://leetcode.com/problems/merge-k-sorted-lists/
  - https://leetcode.com/problems/find-median-from-data-stream/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42626
  - https://school.programmers.co.kr/learn/courses/30/lessons/42627
  - https://school.programmers.co.kr/learn/courses/30/lessons/42628
tags: [phase/1, topic/heap]
---

# Day 12 — 힙·우선순위 큐 (Heap & Priority Queue)

> [!abstract] 한눈 요약 (TL;DR)
> **힙(heap)**은 "**항상 최솟값(또는 최댓값)을 O(1)에 보고, O(log n)에 꺼낼 수 있는**" 자료구조다. 정렬을 매번 다시 하지 않고도 **극값(최대/최소)을 빠르게** 얻어야 할 때 쓴다. 내부적으로는 [[day-11-tree-basics/concept|Day 11]]에서 본 **완전 이진 트리(complete binary tree)**를 **배열 하나**로 구현한 것이다. 이 힙으로 만든 큐가 **우선순위 큐(priority queue)** — FIFO가 아니라 "**우선순위가 높은 것부터** 나오는 큐"다. 파이썬은 표준 라이브러리 `heapq`(**최소 힙**)를 제공하며, 최대 힙은 **부호를 뒤집어**(-x) 흉내 낸다. 코테에서는 **Top-K**, **K번째 큰 값**, **다익스트라 최단경로**([[day-26-bfs/concept|Day 26]] 이후), **그리디 스케줄링**([[day-21-greedy/concept|Day 21]]), **두 힙으로 중앙값** 같은 문제에 단골로 등장한다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **힙**은 **부모가 자식보다 항상 우선(작거나 / 크거나)한다**는 단 하나의 규칙(**힙 속성, heap property**)을 지키는 완전 이진 트리다.
> - **최소 힙(min-heap):** 부모 ≤ 자식 → 트리의 **꼭대기(루트)가 전체 최솟값**.
> - **최대 힙(max-heap):** 부모 ≥ 자식 → 루트가 전체 최댓값.
>
> 주의: 힙은 **완전히 정렬된 게 아니다.** "부모-자식" 관계만 정렬돼 있고, **형제(sibling)끼리는 순서가 없다.** 그래서 "최솟값 하나"는 즉시 알지만, "두 번째로 작은 값"은 따로 찾아야 한다. 이 **느슨한 정렬** 덕분에 완전 정렬(O(n log n))보다 삽입/삭제가 싸다(각각 O(log n)).
>
> **일상 비유 — 응급실 진료 순서.** 먼저 온 순서(FIFO 큐)가 아니라 **가장 위급한 환자**부터 부른다. 새 환자가 와도 전체 줄을 다시 세우지 않고, "가장 위급한 사람"만 맨 앞에 유지하면 된다. 이게 정확히 **우선순위 큐**이고, 그 엔진이 힙이다.
>
> | 자료구조 | 꺼내는 순서 | 대표 연산 |
> |---|---|---|
> | 큐(Queue) | 먼저 들어온 것(FIFO) | [[day-08-queue-deque/concept\|Day 08]] |
> | 스택(Stack) | 나중에 들어온 것(LIFO) | [[day-07-stack/concept\|Day 07]] |
> | **우선순위 큐** | **우선순위가 높은 것** | **힙(heap)** |
>
> **"힙 메모리(heap memory)"와는 다른 말이다.** 운영체제·언어의 동적 메모리 영역을 부르는 "힙"은 이 자료구조와 **이름만 같고 무관**하다. 면접 단골 함정.

> [!gear]- 2. 동작 원리 (How It Works)
> **(1) 완전 이진 트리를 배열로** — 포인터 없이 인덱스 계산만으로 부모·자식을 오간다([[day-11-tree-basics/concept|Day 11]]의 배열 표현).
> - 0-기반: 노드 `i`의 왼쪽 자식 `2i+1`, 오른쪽 자식 `2i+2`, 부모 `(i-1)//2`.
>
> ```
> 배열:   [1, 3, 2, 7, 4, 5]      <- 이 한 줄이 힙
> 트리로 보면:
>             1(0)
>           /      \
>         3(1)      2(2)
>        /   \      /
>      7(3)  4(4)  5(5)
> 모든 부모 <= 자식 (최소 힙). 루트(인덱스 0) = 최솟값 1.
> ```
>
> **(2) 삽입(push) — "끝에 넣고 위로(up-heapify / sift-up)"**
> 1. 배열 맨 끝에 새 값을 붙인다(완전 트리 모양 유지).
> 2. 부모와 비교해 규칙을 어기면 **부모와 swap**, 루트까지 반복.
> 트리 높이가 log n 이므로 최대 log n 번 → **O(log n)**.
>
> ```
> push(0): [1,3,2,7,4,5] 끝에 0 추가 -> [1,3,2,7,4,5,0]
>   0(idx6)의 부모는 2(idx2): 0<2 -> swap -> [1,3,0,7,4,5,2]
>   0(idx2)의 부모는 1(idx0): 0<1 -> swap -> [0,3,1,7,4,5,2]  (끝, 루트 도달)
> ```
>
> **(3) 최솟값 삭제(pop) — "루트 빼고, 끝을 올린 뒤 아래로(down-heapify / sift-down)"**
> 1. 루트(최솟값)를 꺼내 답으로 둔다.
> 2. **배열 맨 끝 값을 루트 자리로** 옮긴다(완전 트리 유지).
> 3. 두 자식 중 **더 우선인(작은) 쪽과 비교**해 규칙 위반이면 swap, 잎까지 반복.
> 역시 **O(log n)**.
>
> **(4) `heapify` — 배열을 한 번에 힙으로, O(n)**
> 모든 내부 노드를 **아래에서 위로** sift-down 한다. "하나씩 push 하면 O(n log n)인데 왜 O(n)?" → 깊은 노드는 많지만 sift-down 거리가 짧고, 얕은 노드는 거리가 길지만 수가 적어 합이 O(n)으로 수렴한다(유명한 분석 결과).
>
> **(5) 파이썬 `heapq` 핵심 API** (모두 리스트를 직접 힙으로 사용)
> ```python
> import heapq
> heapq.heappush(h, x)      # 삽입            O(log n)
> heapq.heappop(h)          # 최솟값 제거+반환 O(log n)
> h[0]                      # 최솟값 확인(peek) O(1)
> heapq.heapify(lst)        # 리스트를 제자리 힙으로 O(n)
> heapq.heappushpop(h, x)   # push 후 pop      O(log n) (1회)
> heapq.heapreplace(h, x)   # pop 후 push      O(log n) (1회)
> heapq.nlargest(k, it)     # 큰 k개          O(n log k)
> heapq.nsmallest(k, it)    # 작은 k개        O(n log k)
> ```
>
> **(6) 최대 힙 흉내 — 부호 뒤집기**
> `heapq`엔 최대 힙이 없다. 넣을 때 `-x`, 꺼낼 때 `-result`. (문자열 등 음수가 안 되는 값은 `(-우선순위, 값)` 튜플로.)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> **힙 자체 (원소 n개)**
>
> | 연산 | 시간복잡도 | 설명 |
> |---|---|---|
> | peek(최솟값 확인) | **O(1)** | 항상 `heap[0]` |
> | push(삽입) | **O(log n)** | 끝에 넣고 위로 sift-up |
> | pop(최솟값 제거) | **O(log n)** | 끝을 올리고 아래로 sift-down |
> | heapify(배열→힙) | **O(n)** | 한 번에 구성(push n번 = O(n log n)보다 빠름) |
> | 임의 값 탐색/삭제 | O(n) | 정렬돼 있지 않아 전부 확인해야 함 |
>
> **힙으로 푸는 대표 패턴**
>
> | 문제 패턴 | 시간복잡도 | 비고 |
> |---|---|---|
> | Top-K / K번째 큰 값 (크기 k 힙) | **O(n log k)** | 전체 정렬 O(n log n)보다 우수 |
> | 힙 정렬(heapsort) | O(n log n) | heapify O(n) + pop n번 |
> | k개 정렬 리스트 병합 | O(N log k) | N = 전체 원소 수 |
> | 다익스트라 최단경로 | O((V+E) log V) | 우선순위 큐 사용 |
>
> > **핵심 직관:** "전부 정렬할 필요 없이 **극값만** 빠르게"가 힙의 존재 이유다. **k가 n보다 훨씬 작을 때** 크기 k 힙(O(n log k))이 정렬(O(n log n))을 이긴다.
>
> **공간:** 원소 저장에 O(n). 크기 k 힙 패턴은 O(k)만 사용 → 스트림/대용량에서 메모리 이점.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"가장 큰/작은 것을 반복해서 꺼낸다" → 힙을 의심하라.** "K번째", "Top K", "매번 최소/최대를 고른다(그리디)", "스트림 중앙값"이라는 말이 보이면 거의 힙이다.
>   - 참고: [heapq — Heap queue algorithm (Python docs)](https://docs.python.org/3/library/heapq.html)
>
> - **최대 힙은 `-x`로.** 파이썬 `heapq`는 최소 힙뿐. 숫자는 부호를 뒤집고, 객체는 `(-priority, tie_breaker, obj)` 튜플로 넣는다.
>   - 참고: [Python heapq max-heap (Stack Overflow)](https://stackoverflow.com/questions/2501457/what-do-i-use-for-a-max-heap-implementation-in-python)
>
> - **동점일 때 "비교 불가" 에러를 조심.** `(priority, obj)`에서 priority가 같으면 파이썬이 `obj`끼리 비교하다 `TypeError`를 낼 수 있다. **삽입 순서 카운터**를 가운데 끼워 `(priority, count, obj)`로 만들면 안전하고 **안정 정렬(stable)**까지 된다.
>   - 참고: [PriorityQueue / heapq tie-breaking (Python docs)](https://docs.python.org/3/library/queue.html#queue.PriorityQueue)
>
> - **크기 k 힙의 방향에 주의.** "가장 **큰** k개"를 남기려면 작은 것을 버리는 **최소 힙**, "가장 **작은** k개"를 남기려면 큰 것을 버리는 **최대 힙**을 쓴다. 방향을 거꾸로 잡는 실수가 잦다.
>   - 참고: [Kth Largest Element (LeetCode #215)](https://leetcode.com/problems/kth-largest-element-in-an-array/)
>
> - **"두 힙(two heaps)" 패턴을 외워둬라.** 아래 절반 최대 힙 + 위 절반 최소 힙으로 중앙값/구간 분할 문제를 O(log n)에 처리한다.
>   - 참고: [Find Median from Data Stream (LeetCode #295)](https://leetcode.com/problems/find-median-from-data-stream/)

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **힙은 "정렬"이 아니다.** `heap[0]`만 최솟값이고 나머지는 부분 순서일 뿐. 힙을 그냥 `print`하면 정렬돼 보이지 않는다. 정렬된 결과가 필요하면 pop을 반복하거나 `sorted()`를 쓴다.
>
> 2. **반드시 `heapify` 또는 `heappush`로만 힙을 만든다.** 일반 리스트에 `append`만 하고 `heappop`을 부르면 **힙 속성이 깨져 잘못된 값**이 나온다. `heapq` 함수는 입력이 이미 힙이라고 가정한다.
>
> 3. **파이썬엔 최대 힙·균형 BST가 없다.** 최대 힙은 `-x` 트릭으로, "정렬 상태 유지 + 임의 위치 삽입"은 `bisect`([[day-18-binary-search/concept|Day 18]] 예정)로 우회한다. 이 한계를 모르면 면접에서 막힌다.
>
> 4. **`heappushpop` vs `heapreplace`의 순서 차이.** `heappushpop(h, x)`는 **넣고 빼서**, x가 현재 최소보다 작으면 x가 그대로 나온다. `heapreplace(h, x)`는 **빼고 넣어서**, 항상 기존 최솟값이 먼저 나온다(빈 힙엔 못 씀). 크기 k 유지엔 보통 push 후 조건부 pop이 더 안전.
>
> 5. **peek은 `h[0]`, 빈 힙 접근은 에러.** 비었는지(`if h:`) 확인 후 접근. `heappop([])`은 `IndexError`.
>
> 6. **Top-K엔 정렬 대신 크기 k 힙.** 전체 정렬 O(n log n)은 과하다. k개만 유지하면 O(n log k) + 메모리 O(k). 데이터가 스트림으로 끝없이 들어올 때는 사실상 힙만 가능.
>
> 7. **`heapq`는 스레드 안전하지 않다.** 멀티스레드 환경에선 `queue.PriorityQueue`(내부에 락 + heapq)를 쓴다. 단일 스레드 코테에선 `heapq`가 더 빠르고 간단.
>
> 8. **힙 정렬은 불안정(unstable) 정렬이고 제자리(in-place) 가능.** O(n log n) 보장이지만 동점의 원래 순서를 보장하지 않는다. 정렬 일반은 [[day-17-sorting/concept|Day 17]]에서 다룬다.

> [!example]- 예제 코드 (Examples)
> ```python
> import heapq
>
> # 1) 최소 힙 기본
> h = []
> for x in [5, 1, 8, 3, 2]:
>     heapq.heappush(h, x)     # O(log n)
> print(h[0])                  # 1  (peek, O(1))
> print(heapq.heappop(h))      # 1  (제거+반환)
>
> # 2) 한 번에 힙으로 (O(n))
> data = [5, 1, 8, 3, 2]
> heapq.heapify(data)          # data 가 제자리에서 힙이 됨
> print(data[0])              # 1
>
> # 3) 최대 힙: 부호 뒤집기
> mh = []
> for x in [5, 1, 8]:
>     heapq.heappush(mh, -x)
> print(-heapq.heappop(mh))    # 8 (최댓값)
>
> # 4) 우선순위 큐 (동점 안전: 삽입 순서 카운터)
> pq, cnt = [], 0
> for pr, name in [(2, "email"), (0, "fire"), (2, "report")]:
>     heapq.heappush(pq, (pr, cnt, name)); cnt += 1
> print([heapq.heappop(pq)[2] for _ in range(len(pq))])
> #   -> ['fire', 'email', 'report']
>
> # 5) Top-K / K번째 큰 값 (크기 k 최소 힙, O(n log k))
> def kth_largest(nums, k):
>     h = []
>     for x in nums:
>         heapq.heappush(h, x)
>         if len(h) > k:
>             heapq.heappop(h)   # 작은 것을 버려 k개 유지
>     return h[0]
> print(kth_largest([3, 2, 1, 5, 6, 4], 2))   # 5
>
> # 6) 편의 함수
> print(heapq.nlargest(3, [7, 2, 9, 4, 1]))   # [9, 7, 4]
> print(list(heapq.merge([1, 4], [2, 3, 5]))) # [1, 2, 3, 4, 5]
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> | 번호 | 문제 | 출처 | 난이도 | 카테고리 |
> |---|---|---|---|---|
> | 1 | Last Stone Weight | [LeetCode #1046](https://leetcode.com/problems/last-stone-weight/) | 🟢기초 | 최대 힙 |
> | 2 | Kth Largest Element in an Array | [LeetCode #215](https://leetcode.com/problems/kth-largest-element-in-an-array/) | 🟡중급 | 크기 k 힙 |
> | 3 | Kth Largest Element in a Stream | [LeetCode #703](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | 🟢기초 | 설계·스트림 |
> | 4 | Top K Frequent Elements | [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/) | 🟡중급 | 빈도·Top-K |
> | 5 | K Closest Points to Origin | [LeetCode #973](https://leetcode.com/problems/k-closest-points-to-origin/) | 🟡중급 | 거리·Top-K |
> | 6 | Merge k Sorted Lists | [LeetCode #23](https://leetcode.com/problems/merge-k-sorted-lists/) | 🔴심화 | k-way 병합 |
> | 7 | Find Median from Data Stream | [LeetCode #295](https://leetcode.com/problems/find-median-from-data-stream/) | 🔴심화 | 두 힙·중앙값 |
> | 8 | 더 맵게 | [프로그래머스 #42626](https://school.programmers.co.kr/learn/courses/30/lessons/42626) | 🟡중급 | 최소 힙(기출 빈출) |
> | 9 | 디스크 컨트롤러 | [프로그래머스 #42627](https://school.programmers.co.kr/learn/courses/30/lessons/42627) | 🔴심화 | SJF 스케줄링 |
> | 10 | 이중우선순위큐 | [프로그래머스 #42628](https://school.programmers.co.kr/learn/courses/30/lessons/42628) | 🟡중급 | 두 힙·게으른 삭제 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 힙은 완전 이진 트리를 배열로 구현한 것(부모/자식 인덱스 계산)
- ➡️ **다음(next):** [[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]] — Top-K 문제에서 힙은 종종 해시(빈도 카운트)와 짝지어 쓰인다
- 🧭 **관련(related):**
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 완전 이진 트리·배열 표현이 힙의 토대
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — FIFO 큐를 우선순위 큐로 확장한 것이 힙
  - [[day-10-linked-list/concept|Day 10 — 연결 리스트]] — k개 정렬 리스트 병합(#23)의 입력 자료구조
  - [[day-17-sorting/concept|Day 17 — 정렬]] — 힙 정렬(heapsort)과 O(n log n) 비교
  - [[day-21-greedy/concept|Day 21 — 그리디]] — "매번 최선을 고른다"는 그리디 선택을 힙이 효율적으로 구현
  - [[day-26-bfs/concept|Day 26 — BFS]] — 가중치 그래프 최단경로(다익스트라)에서 우선순위 큐로 일반화
- 🗺️ **지도(MOC):** [[Phase-1 MOC]] · [[00 Algorithm MOC]]
