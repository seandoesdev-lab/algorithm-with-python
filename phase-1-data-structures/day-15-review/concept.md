---
day: 15
phase: 1-data-structures
title: 자료구조 종합 복습 (Data Structures Review)
category: [자료구조, 복습]
difficulty: 중급
status: done
prev: "[[day-14-prefix-sum/concept|Day 14 — 누적 합]]"
next: "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
related:
  - "[[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]]"
  - "[[day-07-stack/concept|Day 07 — 스택]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
  - "[[day-10-linked-list/concept|Day 10 — 연결 리스트]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 누적 합]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
sources:
  - https://leetcode.com/problems/valid-parentheses/
  - https://leetcode.com/problems/implement-queue-using-stacks/
  - https://leetcode.com/problems/two-sum/
  - https://leetcode.com/problems/daily-temperatures/
  - https://leetcode.com/problems/top-k-frequent-elements/
  - https://leetcode.com/problems/kth-largest-element-in-a-stream/
  - https://leetcode.com/problems/reverse-linked-list/
  - https://leetcode.com/problems/maximum-depth-of-binary-tree/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42586
  - https://school.programmers.co.kr/learn/courses/30/lessons/42579
  - https://docs.python.org/3/library/collections.html
  - https://docs.python.org/3/library/heapq.html
tags: [phase/1, topic/review]
---

# Day 15 — 자료구조 종합 복습 (Data Structures Review)

> [!abstract] 한눈 요약 (TL;DR)
> Phase 1에서 다룬 9개 자료구조(배열·스택·큐/덱·해시·연결 리스트·트리·힙·해시맵 패턴·누적합)를 **하나의 의사결정 표로 묶는 날**이다. 개별 자료구조를 "아는 것"과 코테에서 "고르는 것"은 다른 능력이다. 실전에서 점수를 가르는 건 *문제 문장의 신호(signal)* → *알맞은 자료구조*로 1초 만에 매핑하는 반사신경이다. 예: "가장 최근 것부터"=스택, "먼저 온 순서대로"=큐, "있는지/몇 번"=해시, "매 순간 최댓값/최솟값"=힙, "이전보다 큰 다음 원소"=단조 스택, "구간 합 여러 번"=누적합. 이 노트는 각 자료구조의 **핵심 한 줄 정체성 + 복잡도 치트시트 + 선택 신호 + 단골 함정**을 한 화면에 정리하고, 10개의 혼합 문제로 "어떤 자료구조를 꺼낼지" 판단을 훈련한다. Phase 2(알고리즘 기초)로 넘어가기 전, **자료구조 선택 근육**을 굳히는 마지막 정거장이다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **복습(review)의 본질은 "암기"가 아니라 "검색 인덱스 만들기"다.** 자료구조를 따로따로 외우면 문제 앞에서 "음... 뭘 쓰지?" 하고 멈춘다. 잘 복습한 사람은 머릿속에 *(문제의 신호 → 자료구조)* 사전이 있어서, 문장을 읽는 동시에 후보가 떠오른다.
>
> **일상 비유 — 공구함(toolbox).** 망치·드라이버·렌치를 각각 쓸 줄 아는 것과, *눈앞의 나사를 보고 0.5초 만에 십자 드라이버를 집는 것*은 다르다. 숙련공은 도구의 사용법이 아니라 **"이 상황엔 이 도구"라는 매핑**이 몸에 배어 있다. Phase 1의 9개 자료구조가 공구이고, 오늘은 공구를 닦는 게 아니라 *어떤 나사에 어떤 공구인지*를 정리하는 날이다.
>
> 각 자료구조의 **한 줄 정체성**:
> - **배열/리스트(Array/List)** — 인덱스로 O(1) 임의 접근. 모든 것의 기본 바탕.
> - **스택(Stack, LIFO)** — "가장 최근 것"을 먼저. 괄호 짝, 되돌리기, 단조 스택.
> - **큐/덱(Queue/Deque, FIFO)** — "먼저 온 것"을 먼저. BFS, 작업 대기열, 슬라이딩 윈도우 최댓값.
> - **해시(dict/set)** — "있는가? 몇 번인가? 어디 있나?"를 평균 O(1)로.
> - **연결 리스트(Linked List)** — 노드 포인터 재배선으로 O(1) 삽입/삭제(위치를 알 때).
> - **트리(Tree)** — 계층 구조와 분기. 이진 탐색 트리는 정렬된 O(log n) 탐색.
> - **힙(Heap)** — "매 순간 최솟값/최댓값"을 O(log n)에. Top-K, 우선순위 처리.
> - **해시맵 패턴(Hashmap Patterns)** — 빈도수·그룹핑·"본 적 있나"를 한 번 순회로.
> - **누적합(Prefix Sum)** — 전처리 O(n) 후 구간 합 질의 O(1).

> [!gear]- 2. 동작 원리 (How It Works) — 자료구조 선택 의사결정
> 문제를 읽을 때 아래 신호들을 *체크리스트*처럼 훑는다. 신호가 잡히면 그 자료구조부터 의심한다.
> ```
> 문제 문장에서 이런 신호가 보이면...        ->  먼저 떠올릴 자료구조
> ----------------------------------------------------------------------
> "괄호/짝/중첩", "되돌리기", "가장 최근"      ->  스택 (Stack)
> "이전보다 큰/작은 다음 원소", "온도/주가"   ->  단조 스택 (Monotonic Stack)
> "먼저 들어온 순서대로 처리", "대기열"        ->  큐 (Queue / deque)
> "최단 거리(가중치 없음)", "레벨 단위 탐색"   ->  큐 기반 BFS
> "양쪽 끝에서 넣고 뺀다", "회문 검사"         ->  덱 (Deque)
> "중복 제거", "포함 여부", "몇 번 나왔나"      ->  set / dict (해시)
> "두 수의 합/짝 찾기", "본 적 있는 값"        ->  dict (Two Sum 패턴)
> "빈도수 순", "가장 많이 나온", "그룹핑"      ->  Counter + 정렬/힙
> "매번 최솟값/최댓값을 꺼낸다", "Top-K"       ->  힙 (heapq)
> "K번째로 큰/작은", "스트림에서 순위 유지"     ->  크기 K 힙
> "정렬 유지하며 삽입/탐색", "계층/부모-자식"   ->  트리 (BST / 일반 트리)
> "구간 합/평균을 여러 번 묻는다"              ->  누적합 (Prefix Sum)
> "구간마다 +v 갱신 여러 번 후 조회"           ->  차분 배열 + 누적합
> "정중앙 삽입/삭제가 잦다(인덱스 무관)"        ->  연결 리스트
> ```
>
> **두 개 이상이 결합되는 경우가 실전이다.** Phase 1의 진짜 교훈은 자료구조가 *섞인다*는 것:
> - Top-K 빈도 = **해시(Counter)** 로 세고 **힙** 으로 K개 추림.
> - 합이 K인 구간 개수 = **누적합** + **해시맵**.
> - 슬라이딩 윈도우 최댓값 = **덱**(단조 덱).
> - 트리 레벨 순회 = **트리** + **큐**(BFS).
> - LRU 캐시 = **해시맵** + **이중 연결 리스트**.
>
> **선택의 한 줄 기준:** "무엇을, 어느 순서로, 얼마나 빨리 꺼내야 하는가?"를 물어라. *순서가 LIFO면 스택, FIFO면 큐, 우선순위면 힙, 키로 찾으면 해시, 인덱스로 찾으면 배열.*

> [!chart]- 3. 복잡도 (Time / Space Complexity) — Phase 1 마스터 치트시트
> 면접·코테 직전 5분 컷으로 훑는 표. (평균 기준, 해시는 최악 O(n)이지만 실전에선 O(1)로 본다.)
>
> | 자료구조 | 접근/탐색 | 삽입 | 삭제 | 핵심 연산 | 대표 도구 |
> |---|---|---|---|---|---|
> | 배열/리스트 | O(1) 인덱스 / O(n) 값탐색 | 끝 O(1)·중간 O(n) | 끝 O(1)·중간 O(n) | 임의 접근 | `list` |
> | 스택 | O(n) | O(1) push | O(1) pop | LIFO | `list` (append/pop) |
> | 큐 | O(n) | O(1) | O(1) | FIFO | `collections.deque` |
> | 덱 | O(n) | 양끝 O(1) | 양끝 O(1) | 양방향 | `collections.deque` |
> | 해시 set/dict | — | O(1) | O(1) | 멤버십·카운트 | `set` `dict` `Counter` |
> | 연결 리스트 | O(n) | O(1)* | O(1)* | 포인터 재배선 | 직접 구현 |
> | 이진 탐색 트리(균형) | O(log n) | O(log n) | O(log n) | 정렬 탐색 | (Phase 4) |
> | 힙(우선순위 큐) | 최솟값 O(1) | O(log n) | O(log n) pop | Top-K | `heapq` |
> | 누적합 | 구간 합 O(1) | 구축 O(n) | 갱신 O(n) | 구간 질의 | `itertools.accumulate` |
>
> \* 연결 리스트의 O(1)은 **삽입/삭제할 위치(노드)를 이미 알고 있을 때**다. 위치를 찾는 데는 O(n).
>
> > **공간 직관:** 위 자료구조는 모두 원소당 O(1), 전체 O(n) 공간. 누적합·해시는 입력과 별도로 O(n) 보조 배열/테이블을 더 쓴다. 힙은 정렬 없이 부분 순서만 유지해 메모리 효율이 좋다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"리스트로 큐 흉내내지 마라."** `list.pop(0)`은 앞을 빼면 나머지를 한 칸씩 당겨 O(n)이다. FIFO가 필요하면 무조건 `collections.deque`(`popleft()` O(1)). 코테 시간 초과(TLE)의 단골 원인.
>   - 참고: [collections — deque (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.deque)
> - **"Top-K엔 전체 정렬 대신 크기 K 힙."** N개 중 가장 큰 K개는 정렬 O(n log n)보다 크기 K 최소 힙으로 O(n log k)가 빠르다. 단, K가 N에 가까우면 그냥 정렬이 단순하고 충분하다.
>   - 참고: [Top K Frequent Elements (LeetCode #347)](https://leetcode.com/problems/top-k-frequent-elements/)
> - **`Counter`는 빈도수 문제의 스위스 칼.** `Counter(arr)`로 세고, `.most_common(k)`로 상위 K개를 바로 뽑는다. 빈도 그룹핑·아나그램·"가장 많은 것"은 거의 `Counter`.
> - **단조 스택(monotonic stack)을 한 번 익히면 "다음 큰 원소" 류가 전부 풀린다.** Daily Temperatures, 다음 큰 수, 히스토그램 최대 직사각형이 모두 같은 골격이다.
>   - 참고: [Daily Temperatures (LeetCode #739)](https://leetcode.com/problems/daily-temperatures/)
> - **"존재/카운트/위치"가 보이면 반사적으로 해시.** O(n²) 이중 루프가 떠오르면, 한쪽을 dict에 넣어 O(n)으로 떨어뜨릴 수 있는지부터 의심하라(Two Sum 패턴).
>   - 참고: [Two Sum (LeetCode #1)](https://leetcode.com/problems/two-sum/)

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **자료구조 선택은 "꺼내는 순서/기준"이 결정한다.** LIFO→스택, FIFO→큐, 우선순위→힙, 키→해시, 인덱스→배열. 이 한 줄이 Phase 1 전체의 압축이다.
> 2. **`deque`는 큐·스택·덱을 전부 대체한다.** 양끝 O(1) 삽입/삭제. 큐는 `append`/`popleft`, 스택은 `append`/`pop`. 헷갈리면 `deque` 하나로 통일해도 안전하다.
> 3. **해시의 O(1)은 "평균"이다.** 해시 충돌이 심하면 O(n)까지 나빠진다. 또 dict 키는 **불변(immutable)·해시 가능**해야 한다(리스트는 키 불가, 튜플은 가능). 면접 단골.
> 4. **`heapq`는 최소 힙(min-heap)만 제공한다.** 최대 힙이 필요하면 값에 `-`를 붙여 넣거나 `(-priority, item)` 튜플을 쓴다. 또 `heapq`는 리스트를 제자리에서 힙으로 다루므로 `heapify` 후 직접 인덱싱하면 안 된다.
>   - 참고: [heapq (Python 공식 문서)](https://docs.python.org/3/library/heapq.html)
> 5. **연결 리스트의 강점은 "O(1) 삽입/삭제", 약점은 "O(n) 임의 접근".** 인덱스로 자주 접근하면 배열이 낫고, 중간 삽입/삭제가 잦고 포인터를 들고 있으면 연결 리스트가 낫다. 포인터 꼬임(dummy head, 끊기 전에 다음 노드 저장)을 조심하라.
> 6. **트리는 "재귀 또는 스택/큐"로 순회한다.** 깊이(DFS)는 재귀/스택, 레벨(BFS)은 큐. 재귀 깊이가 크면 파이썬 기본 재귀 한도(약 1000)에 걸리니 `sys.setrecursionlimit` 또는 반복(iterative)으로 전환한다.
> 7. **"여러 번 질의"가 핵심 신호다.** 같은 데이터에 질의가 1번이면 전처리(누적합·정렬·해시 구축) 비용이 아깝다. 질의가 많을수록 전처리형 자료구조가 이긴다.
> 8. **시간 초과(TLE)의 90%는 자료구조 오선택.** O(n²)가 한계를 넘으면, "이 연산을 해시/힙/누적합으로 O(1)·O(log n)로 바꿀 수 있나?"를 먼저 묻는다. Phase 2의 Big-O로 이 직관을 수치화한다([[day-16-big-o/concept|Day 16]]).

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import deque, Counter
> import heapq
>
> # 1) 스택: 괄호 짝 맞추기 (LIFO)
> def valid_parentheses(s):
>     pair = {')': '(', ']': '[', '}': '{'}
>     stack = []
>     for ch in s:
>         if ch in '([{':
>             stack.append(ch)
>         else:
>             if not stack or stack.pop() != pair[ch]:
>                 return False
>     return not stack
>
> # 2) 큐(deque): FIFO. list.pop(0) 대신 popleft() 로 O(1).
> q = deque()
> q.append(1); q.append(2)        # 뒤로 넣기
> first = q.popleft()             # 앞에서 빼기 (O(1))
>
> # 3) 해시: Two Sum 을 O(n) 으로 (이중 루프 O(n^2) 회피)
> def two_sum(nums, target):
>     seen = {}                   # 값 -> 인덱스
>     for i, x in enumerate(nums):
>         if target - x in seen:
>             return [seen[target - x], i]
>         seen[x] = i
>     return []
>
> # 4) 힙 + 해시: 가장 빈번한 K 개 (Counter 로 세고 크기 K 힙)
> def top_k_frequent(nums, k):
>     freq = Counter(nums)
>     return [v for v, _ in heapq.nlargest(k, freq.items(), key=lambda kv: kv[1])]
>
> # 5) 단조 스택: 더 따뜻한 날까지 며칠 (다음 큰 원소 패턴)
> def daily_temperatures(temps):
>     ans = [0] * len(temps)
>     stack = []                  # 아직 더 큰 값을 못 만난 인덱스들
>     for i, t in enumerate(temps):
>         while stack and temps[stack[-1]] < t:
>             j = stack.pop()
>             ans[j] = i - j
>         stack.append(i)
>     return ans
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> Phase 1 전 범위를 섞은 세트. 각 문제 옆에 "어떤 자료구조 신호인지"를 표시했다.
>
> | 번호 | 문제 | 출처 | 난이도 | 자료구조 |
> |---|---|---|---|---|
> | 1 | Valid Parentheses | [LeetCode #20](https://leetcode.com/problems/valid-parentheses/) | 🟢기초 | 스택 |
> | 2 | Implement Queue using Stacks | [LeetCode #232](https://leetcode.com/problems/implement-queue-using-stacks/) | 🟢기초 | 스택→큐 |
> | 3 | Two Sum | [LeetCode #1](https://leetcode.com/problems/two-sum/) | 🟢기초 | 해시 |
> | 4 | Reverse Linked List | [LeetCode #206](https://leetcode.com/problems/reverse-linked-list/) | 🟢기초 | 연결 리스트 |
> | 5 | Maximum Depth of Binary Tree | [LeetCode #104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | 🟢기초 | 트리 |
> | 6 | Daily Temperatures | [LeetCode #739](https://leetcode.com/problems/daily-temperatures/) | 🟡중급 | 단조 스택 |
> | 7 | Top K Frequent Elements | [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/) | 🟡중급 | 해시+힙 |
> | 8 | Kth Largest Element in a Stream | [LeetCode #703](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | 🟢기초 | 크기 K 힙 |
> | 9 | 기능개발 | [프로그래머스 #42586](https://school.programmers.co.kr/learn/courses/30/lessons/42586) | 🟡중급 | 큐/스택 |
> | 10 | 베스트앨범 | [프로그래머스 #42579](https://school.programmers.co.kr/learn/courses/30/lessons/42579) | 🟡중급 | 해시+정렬 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근 방식 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-14-prefix-sum/concept|Day 14 — 누적 합]] — Phase 1의 마지막 개별 자료구조. 오늘 전체를 묶는다
- ➡️ **다음(next):** [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — "어떤 자료구조가 왜 빠른가"를 복잡도로 수치화하며 Phase 2 시작
- 🧭 **관련(related):**
  - [[day-06-array-list/concept|Day 06 — 배열과 동적 리스트]] — 모든 자료구조의 바탕
  - [[day-07-stack/concept|Day 07 — 스택]] — LIFO·괄호·단조 스택
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — FIFO·BFS·양방향
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — 멤버십·카운트 O(1)
  - [[day-10-linked-list/concept|Day 10 — 연결 리스트]] — 포인터 재배선
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 계층·분기 구조
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — Top-K·우선순위
  - [[day-13-hashmap-patterns/concept|Day 13 — 해시맵 응용]] — 빈도·그룹핑 패턴
  - [[day-14-prefix-sum/concept|Day 14 — 누적 합]] — 전처리 후 구간 질의 O(1)
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 선택을 정당화하는 복잡도 언어
- 🗺️ **지도(MOC):** [[Phase-1 MOC]] · [[00 Algorithm MOC]]
