---
day: 30
phase: 3-search-graph
title: 개념 집중기 종합 복습 (Final Review)
category: [복습, 종합, 의사결정, 자료구조, 알고리즘, 탐색]
difficulty: 중급
status: done
prev: "[[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용 (Tree Traversal)]]"
next: "[[day-31-problem-drilling/concept|Day 31 — 문제 풀이기 시작 (Problem Drilling)]]"
related:
  - "[[day-15-review/concept|Day 15 — 자료구조 종합 복습]]"
  - "[[day-23-review/concept|Day 23 — 알고리즘 기초 복습]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-24-brute-force/concept|Day 24 — 완전 탐색]]"
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
  - "[[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]]"
  - "[[day-31-problem-drilling/concept|Day 31 — 문제 풀이기 시작]]"
sources:
  - https://leetcode.com/problems/valid-anagram/
  - https://leetcode.com/problems/two-sum/
  - https://leetcode.com/problems/valid-parentheses/
  - https://leetcode.com/problems/binary-search/
  - https://leetcode.com/problems/number-of-islands/
  - https://leetcode.com/problems/merge-intervals/
  - https://leetcode.com/problems/top-k-frequent-elements/
  - https://leetcode.com/problems/course-schedule/
  - https://school.programmers.co.kr/learn/courses/30/lessons/43165
  - https://school.programmers.co.kr/learn/courses/30/lessons/43162
  - https://docs.python.org/3/library/collections.html
  - https://wiki.python.org/moin/TimeComplexity
tags: [phase/3, topic/review, topic/final-review, topic/decision-making, topic/cheatsheet]
---

# Day 30 — 개념 집중기 종합 복습 (Final Review)

> [!abstract] 한눈 요약 (TL;DR)
> **개념 집중기(Phase 0~3, Day 01~29)의 마지막 정거장**이다. 지난 29일 동안 배운 것을 한 줄로 압축하면 이렇다 — **"입력을 보고 자료구조를 고르고, 문제의 신호를 보고 알고리즘 기법을 고르고, Big-O로 시간 안에 도는지 검산한다."** 이 노트는 새 개념을 배우는 날이 아니라, 흩어진 무기들을 **하나의 의사결정 지도(decision map)** 로 묶어 "문제를 읽는 즉시 후보가 떠오르는 반사신경"을 만드는 날이다. 세 층위로 정리한다. **① 자료구조 선택** — "무엇을 저장·조회하나?"(순서=리스트/덱, 빠른 존재 확인=set/dict, 최대·최소 반복 추출=heap, 후입선출=stack, 선입선출=queue). **② 알고리즘 기법 선택** — "이미 정렬/단조인가?"(정렬+값찾기=이분 탐색, 정렬+짝찾기=투 포인터, 연속 구간=슬라이딩 윈도우, 국소 최적=그리디, 반으로 쪼갬=분할정복). **③ 탐색 선택** — "상태 공간을 어떻게 훑나?"(모두 시도=완전 탐색, 깊이 우선=DFS, 최단·층별=BFS, 가지치기 조합=백트래킹, 관계=그래프/트리 순회). 그리고 모든 선택의 최종 심판은 언제나 **Big-O**다. 오늘의 10문제는 특정 기법 하나가 아니라 **"어떤 무기를 꺼낼지 판단"** 을 훈련하도록 Phase 0~3 전 범위를 섞었다. 내일(Day 31)부터 시작될 **문제 풀이기(problem drilling)** 를 위한 마지막 근육 다지기다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **종합 복습의 본질은 "암기 복습"이 아니라 "인덱스 재구축"이다.** 지금까지 29일은 무기를 하나씩 벼려 온 시간이었다. 스택·큐·해시·힙·트리(자료구조), 정렬·이분 탐색·투 포인터·슬라이딩 윈도우·그리디·분할정복(기법), 완전 탐색·DFS·BFS·백트래킹·그래프/트리 순회(탐색). 각각은 잘 알아도, 문제 앞에서 **"지금 뭘 꺼내지?"** 하고 멈춘다면 아직 실전 준비가 안 된 것이다.
>
> **일상 비유 — 공구함을 정리하는 정비공.** 초보 정비공은 렌치·드라이버·플라이어를 다 쓸 줄 안다. 하지만 숙련공과의 차이는 *고장 난 부품을 보는 순간 어떤 공구를 집을지가 몸에 배어 있다는 것*이다. 오늘은 새 공구를 사는 날이 아니라, 이미 가진 공구를 **"이 증상엔 이 공구"라는 라벨과 함께 서랍에 재배치**하는 날이다. Day 15(자료구조 복습)와 Day 23(알고리즘 복습)이 각 서랍을 정리했다면, 오늘은 **서랍 전체를 관통하는 마스터 인덱스**를 만든다.
>
> **세 개의 질문으로 압축되는 개념 집중기.** 어떤 코테 문제든 이 세 질문의 조합으로 풀린다.
> - **"무엇을 저장하고 어떻게 꺼내는가?"** → 자료구조 선택 ([[day-15-review/concept|Day 15]])
> - **"이미 정렬/단조인가, 답을 어떻게 좁히는가?"** → 알고리즘 기법 선택 ([[day-23-review/concept|Day 23]])
> - **"상태 공간을 어떻게 탐색하는가?"** → 완전 탐색·DFS·BFS·백트래킹 선택 (Phase 3)
>
> 그리고 세 질문 위에 **"이 방법이 입력 한계 안에서 도는가?"** 라는 Big-O의 심판이 항상 얹힌다. 이 네 겹이 개념 집중기의 전부다.

> [!gear]- 2. 동작 원리 (How It Works) — 마스터 의사결정 지도
> 문제를 읽을 때 아래 세 표를 *체크리스트*처럼 위에서 아래로 훑는다. 신호가 잡히면 그 후보부터 의심한다.
>
> **(A) 자료구조 선택 — "무엇을 저장·조회하나?"**
> ```
> 이런 요구가 보이면...                          ->  자료구조         복잡도 핵심
> ------------------------------------------------------------------------------
> "순서 유지 + 끝에서 추가/삭제"                  ->  list            append/pop O(1)
> "양쪽 끝에서 넣고 빼기", "슬라이딩 윈도우"       ->  collections.deque  양끝 O(1)
> "존재 여부/중복 제거를 빠르게"                  ->  set             in/add O(1) 평균
> "키->값 매핑, 빈도수 세기"                      ->  dict / Counter  조회 O(1) 평균
> "후입선출(LIFO), 괄호/되돌리기/DFS"             ->  list를 stack으로  push/pop O(1)
> "선입선출(FIFO), BFS/대기열"                    ->  deque를 queue로  O(1)
> "매번 최소/최대를 뽑아야 함", "K번째"           ->  heapq           push/pop O(log n)
> "구간 합을 여러 번 질의"                        ->  prefix sum      전처리 후 질의 O(1)
> ```
>
> **(B) 알고리즘 기법 선택 — "이미 정렬/단조인가?"**
> ```
> 문제 문장의 신호...                            ->  기법             전제/복잡도
> ------------------------------------------------------------------------------
> "정렬돼 있다 + 특정 값 위치/존재"               ->  이분 탐색        정렬됨 / O(log n)
> "...할 수 있는 최소/최대 K는?"                  ->  정답 이분 탐색   답이 단조 / O(n log W)
> "정렬된 두 수의 합/짝, 양 끝에서 좁혀"          ->  투 포인터        대개 정렬됨 / O(n)
> "연속 부분배열/부분문자열의 최대·최소·개수"      ->  슬라이딩 윈도우  연속 구간 / O(n)
> "매 순간 최선을 골라도 되나 (구간/배정)"        ->  그리디(+정렬)    교환 논증 / O(n log n)
> "반으로 나눠 풀고 합친다 (병합/정렬)"           ->  분할정복         균등 분할 / O(n log n)
> ```
>
> **(C) 탐색 선택 — "상태 공간을 어떻게 훑나?" (Phase 3의 핵심)**
> ```
> 이런 문제가 보이면...                          ->  탐색             특징
> ------------------------------------------------------------------------------
> "모든 경우를 다 시도, N이 작다(<= ~20)"        ->  완전 탐색        정확하지만 지수적
> "경로/영역을 끝까지 파고든다, 연결 요소"        ->  DFS(재귀/스택)   깊이 우선, 경로 복원
> "최단 거리/최소 횟수/층별(가중치 1)"           ->  BFS(큐)          가까운 것부터, 최단 보장
> "조합/순열 + 조건 위반 시 되돌림(가지치기)"     ->  백트래킹         DFS + prune, 부분해 취소
> "정점-간선 관계, 인접 리스트"                  ->  그래프 순회      visited 필수(사이클)
> "사이클 없는 특수 그래프, 전위/중위/후위"       ->  트리 순회        부모 회피(visited 불필요)
> ```
>
> **세 층위가 결합되는 것이 실전이다.** 진짜 문제는 세 표에서 하나씩 뽑아 조합된다:
> - **섬의 개수** = 그리드를 **완전 탐색**하며 각 섬을 **DFS/BFS**로 지우기 + `visited` 관리.
> - **Top K 빈출** = **dict/Counter** 로 빈도 집계 + **heap** 으로 상위 K 추출.
> - **강의실/구간 병합** = **정렬** + **그리디** + (때때로) **heap**.
> - **타겟 넘버** = 부호 조합 **완전 탐색/DFS** (N<=20이라 2^20 허용).
> - **네트워크(연결 요소 수)** = **그래프 표현** + **DFS/BFS** 로 컴포넌트 세기.
>
> **선택의 최종 관문은 언제나 Big-O.** 기법을 골랐으면 입력 상한을 넣어 실제 연산 수를 어림하라. `n <= 10^5`에 `O(n^2)`면 `10^10`으로 시간 초과(TLE), `O(n log n)`이면 약 `1.7*10^6`으로 통과. 선택 오류의 90%는 복잡도 오판이다([[day-16-big-o/concept|Day 16]]). 실행 가능한 통합 예제: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity) — 개념 집중기 마스터 치트시트
> 면접·코테 직전 5분 컷으로 훑는 통합 표. (n = 입력 크기, V = 정점, E = 간선)
>
> **자료구조 연산 복잡도**
> | 자료구조 | 대표 연산 | 시간 | 비고 |
> |---|---|---|---|
> | list | 인덱싱 / append / pop() | O(1) | 중간 삽입·삭제·`in`은 O(n) |
> | deque | 양끝 append/pop | O(1) | 큐·덱·슬라이딩 윈도우 |
> | set / dict | in / add / 조회 | O(1) 평균 | 최악 O(n)(해시 충돌) |
> | heapq | push / pop | O(log n) | peek(최소)은 `h[0]` O(1) |
> | prefix sum | 구간 합 질의 | O(1) | 전처리 O(n) |
>
> **알고리즘 기법 복잡도**
> | 기법 | 시간 | 공간 | 전제 |
> |---|---|---|---|
> | 정렬 | O(n log n) | O(n) | 비교 가능(Timsort 안정) |
> | 이분 탐색 | O(log n) | O(1) | **정렬됨** |
> | 투 포인터 | O(n) | O(1) | 대개 정렬됨 |
> | 슬라이딩 윈도우 | O(n) | O(k) | 연속 구간 |
> | 그리디 | O(n log n) | O(1) | 교환 논증 |
> | 분할정복(병합형) | O(n log n) | O(n) | 균등 분할 |
>
> **탐색·그래프 복잡도**
> | 탐색 | 시간 | 공간 | 비고 |
> |---|---|---|---|
> | 완전 탐색(부분집합) | O(2^n) | O(n) | N 작을 때만 |
> | 완전 탐색(순열) | O(n!) | O(n) | N<=~10 |
> | DFS / BFS | O(V+E) | O(V) | 인접 리스트 기준 |
> | 백트래킹 | O(가지 수) | O(깊이) | 가지치기로 실제로는 훨씬 적음 |
> | 트리 순회 | O(N) | O(H)~O(W) | H=높이, W=최대 폭 |
>
> > **핵심 직관 1 — "O(1) 조회가 문을 연다".** set/dict의 O(1) 존재 확인은 O(n^2) 이중 루프를 O(n)으로 떨어뜨리는 가장 흔한 최적화다(Two Sum, 중복 확인, 방문 체크). 코테 최적화의 절반은 "이걸 해시로 O(1)에 조회할 수 있나?"에서 나온다.
> >
> > **핵심 직관 2 — "정렬 O(n log n)이 문을 연다".** 정렬 뒤에 이분 탐색·투 포인터·그리디가 붙는다. O(n^2)가 한계를 넘으면 "정렬로 O(n log n)에 떨어뜨릴 수 있나?"를 가장 먼저 의심하라([[day-17-sorting/concept|Day 17]]).
> >
> > **핵심 직관 3 — "그래프 순회는 O(V+E)".** DFS도 BFS도 각 정점·간선을 한 번씩만 보므로 O(V+E)로 동일하다. 차이는 *순서*(깊이 vs 너비)와 *공간 형태*(스택 vs 큐)이지 복잡도가 아니다. 최단 거리(무가중치)가 필요하면 BFS를 고른다([[day-26-bfs/concept|Day 26]]).
> >
> > **입력 크기 → 허용 복잡도 역산표.** `n<=10^6`→O(n)·O(n log n) / `n<=10^5`→O(n log n) / `n<=10^4`→O(n^2) 가능 / `n<=500`→O(n^3) / `n<=20`→O(2^n) 완전 탐색 / `n<=10`→O(n!) 순열. **문제의 제약(constraints)이 곧 알고리즘 힌트다.**

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **문제를 읽을 때 "제약(constraints)부터" 본다.** N의 상한이 알고리즘을 거의 결정한다. N<=20이면 출제자가 "완전 탐색/비트마스킹 해도 된다"고 허락한 것이고, N=10^5면 "O(n log n) 안에 풀라"는 신호다. 제약을 먼저 읽는 습관이 기법 선택 속도를 바꾼다.
>   - 참고: [Python TimeComplexity (공식 위키)](https://wiki.python.org/moin/TimeComplexity)
> - **"세 개의 질문"을 소리 내어 물어라.** ① 무엇을 저장·조회? ② 이미 정렬/단조? ③ 상태 공간을 어떻게 훑나? 막힐 때 이 셋을 순서대로 던지면 대부분 후보가 좁혀진다.
> - **DFS vs BFS 한 줄 구별.** "경로 자체·모든 조합·연결 요소"면 DFS, "최단 거리·최소 횟수·층별"이면 BFS. 최단 거리에 DFS를 쓰면 모든 경로를 다 봐야 해 느리다.
>   - 참고: [Number of Islands (LeetCode #200)](https://leetcode.com/problems/number-of-islands/)
> - **"빈도수/그룹핑"이 보이면 반사적으로 Counter/dict.** 애너그램, Top K, 중복 문자, 그룹 분류는 전부 해시 집계 한 방으로 시작한다.
>   - 참고: [Top K Frequent Elements (LeetCode #347)](https://leetcode.com/problems/top-k-frequent-elements/)
> - **복습은 "다시 읽기"가 아니라 "백지 인출"로.** Day 15·23·오늘의 표를 덮고 빈 종이에 세 의사결정 표를 직접 재현해 보라. 인출(retrieval)이 재읽기보다 기억을 훨씬 강하게 굳힌다.
> - **막히면 항상 완전 탐색으로 내려가라.** 어떤 기법도 안 떠오르면 "일단 모두 시도"하는 브루트포스로 정답의 기준선(baseline)을 잡고, 거기서 중복 제거·가지치기·메모이제이션으로 최적화한다([[day-24-brute-force/concept|Day 24]]).

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **제약이 알고리즘을 결정한다.** 코테에서 가장 먼저 볼 것은 예제가 아니라 N·값의 상한이다. N<=20→완전 탐색/비트마스킹, N<=10^5→O(n log n), N<=10^6→O(n). 이 역산이 안 되면 맞는 아이디어도 TLE로 죽는다([[day-16-big-o/concept|Day 16]]).
> 2. **해시(set/dict)의 O(1)은 "평균"이다.** 대부분 O(1)이지만 최악은 O(n). 코테에선 평균으로 충분하나, 키로 쓸 값은 **불변(hashable)** 이어야 한다(list는 키 불가, tuple은 가능). 방문 체크·중복 제거·빈도 집계의 표준 도구.
> 3. **DFS의 재귀 깊이 한계.** 파이썬 기본 재귀 한도는 1000. 깊은 그래프/치우친 트리에서 재귀 DFS는 `RecursionError`로 터진다. `sys.setrecursionlimit(10**6)`으로 올리거나 명시적 스택 반복으로 바꿔라([[day-25-dfs/concept|Day 25]]).
> 4. **BFS만이 무가중치 최단 거리를 보장한다.** 큐로 층별 확장하므로 목표를 처음 만나는 순간이 최단이다. DFS는 최단을 보장하지 않는다. 가중치가 있으면 BFS가 아니라 다익스트라(Phase 4 예정)를 써야 한다([[day-26-bfs/concept|Day 26]]).
> 5. **그래프엔 visited가 필수, 트리엔 부모 회피면 충분.** 일반 그래프는 사이클이 있어 `visited` 없이는 무한 루프. 트리는 사이클이 없어 부모만 피하면 된다. 이 차이를 놓치면 그래프 순회가 무한 반복하거나 트리에서 불필요한 배열을 쓴다([[day-28-graph/concept|Day 28]]·[[day-29-tree-traversal/concept|Day 29]]).
> 6. **그리디는 "증명 없으면 의심".** 그럴듯해도 반례가 있으면 틀린다. 작은 반례를 손으로 만들고, 안 깨지면 교환 논증으로 확신하라. 애매하면 완전 탐색→DP로 내려가는 안전망을 생각한다([[day-21-greedy/concept|Day 21]]).
> 7. **이분 탐색의 3대 버그.** ① 경계(`lo<=hi` vs `lo<hi`) ② 중앙(`(lo+hi)//2`) ③ 갱신(`lo=mid+1`/`hi=mid-1`로 반드시 구간을 좁혀 무한 루프 방지). 정렬 안 된 배열엔 무효. "최소/최대 K"는 **정답 자체를 이분 탐색**([[day-18-binary-search/concept|Day 18]]).
> 8. **백트래킹은 "선택→탐색→취소(원상복구)".** 방문 표시나 부분해에 원소를 넣었으면 재귀 후 반드시 되돌려야(pop/unvisit) 다음 가지가 오염되지 않는다. 이 원상복구를 빼먹는 것이 백트래킹 1위 버그다([[day-27-backtracking/concept|Day 27]]).
> 9. **"모든 노드를 최소 한 번은 봐야 한다"가 하한.** 순회·탐색이 O(V+E)/O(N)인 이유. 이보다 빠를 수 없다. 반대로 전처리(정렬·해시·prefix sum)를 한 번 해두면 이후 질의를 O(1)~O(log n)로 낮춰 전체가 빨라진다. **"한 번의 전처리로 여러 번의 질의를 싸게"** 가 최적화의 큰 축이다.
>   - 참고: [collections (Python 공식 문서)](https://docs.python.org/3/library/collections.html)

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import deque, Counter
> import heapq
>
> # (A) 자료구조: 해시로 O(n^2)를 O(n)으로 (Two Sum)
> def two_sum(nums, target):
>     seen = {}                         # 값 -> 인덱스
>     for i, x in enumerate(nums):
>         if target - x in seen:        # O(1) 조회
>             return [seen[target - x], i]
>         seen[x] = i
>     return []
>
> # (B) 기법: 정렬 + 그리디 (구간 병합)
> def merge_intervals(intervals):
>     intervals.sort()                  # 시작점 기준 정렬이 첫 수
>     merged = []
>     for s, e in intervals:
>         if merged and s <= merged[-1][1]:
>             merged[-1][1] = max(merged[-1][1], e)
>         else:
>             merged.append([s, e])
>     return merged
>
> # (C) 탐색: BFS로 무가중치 최단 거리 (그리드)
> def bfs_shortest(grid, start, goal):
>     R, C = len(grid), len(grid[0])
>     q = deque([(start, 0)])
>     seen = {start}
>     while q:
>         (r, c), d = q.popleft()
>         if (r, c) == goal:
>             return d                  # 처음 만나는 순간이 최단
>         for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
>             nr, nc = r+dr, c+dc
>             if 0<=nr<R and 0<=nc<C and grid[nr][nc]==0 and (nr,nc) not in seen:
>                 seen.add((nr, nc))
>                 q.append(((nr, nc), d+1))
>     return -1
>
> # (D) 결합: dict 집계 + heap으로 상위 K (Top K Frequent)
> def top_k_frequent(nums, k):
>     freq = Counter(nums)              # 빈도 집계 O(n)
>     return [x for x, _ in heapq.nlargest(k, freq.items(), key=lambda kv: kv[1])]
>
> # (E) 완전 탐색/DFS: 부호 조합으로 타겟 만들기 (타겟 넘버 골격)
> def count_targets(numbers, target):
>     def dfs(i, total):
>         if i == len(numbers):
>             return 1 if total == target else 0
>         return dfs(i+1, total+numbers[i]) + dfs(i+1, total-numbers[i])
>     return dfs(0, 0)
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 개념 집중기 전 범위(Phase 0~3)를 섞은 종합 세트. 각 문제 옆에 "어떤 무기 신호인지"를 표시했다. 뒤로 갈수록 자료구조·기법·탐색이 결합된다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 무기(신호) |
> |---|---|---|---|---|
> | 1 | Valid Anagram | [LeetCode #242](https://leetcode.com/problems/valid-anagram/) | 🟢기초 | 해시/Counter |
> | 2 | Two Sum | [LeetCode #1](https://leetcode.com/problems/two-sum/) | 🟢기초 | 해시 O(1) 조회 |
> | 3 | Valid Parentheses | [LeetCode #20](https://leetcode.com/problems/valid-parentheses/) | 🟢기초 | 스택 |
> | 4 | Binary Search | [LeetCode #704](https://leetcode.com/problems/binary-search/) | 🟢기초 | 이분 탐색 |
> | 5 | Number of Islands | [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | 🟡중급 | 완전탐색+DFS/BFS |
> | 6 | Merge Intervals | [LeetCode #56](https://leetcode.com/problems/merge-intervals/) | 🟡중급 | 정렬+그리디 |
> | 7 | Top K Frequent Elements | [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/) | 🟡중급 | 해시+힙 |
> | 8 | Course Schedule | [LeetCode #207](https://leetcode.com/problems/course-schedule/) | 🟡중급 | 그래프 사이클(DFS/BFS) |
> | 9 | 타겟 넘버 ^target-number | [프로그래머스 #43165](https://school.programmers.co.kr/learn/courses/30/lessons/43165) | ⚫기출 | 완전탐색/DFS |
> | 10 | 네트워크 ^network | [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162) | ⚫기출 | 그래프 연결요소(DFS/BFS) |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제를 "세 개의 질문"으로 분해해 무기를 고르는 과정과 다중 접근(DFS vs BFS, 정렬 vs 해시, 힙 vs 정렬)을 복잡도와 함께 비교한다. 기출 "타겟 넘버"의 DFS/완전 탐색과 "네트워크"의 연결 요소 세기(DFS·BFS·Union-Find 관점) 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용 (Tree Traversal)]] — 트리 순회로 Phase 3의 개별 개념이 끝났다. 오늘은 Phase 0~3 전체를 하나의 의사결정 지도로 통합한다
- ➡️ **다음(next):** [[day-31-problem-drilling/concept|Day 31 — 문제 풀이기 시작 (Problem Drilling)]] — 개념 학습을 마치고, 유형·난이도별 기출 문제 풀이 중심의 2단계로 전환한다
- 🧭 **관련(related):**
  - [[day-15-review/concept|Day 15 — 자료구조 종합 복습]] — "무엇을 저장·조회하나" 서랍. 오늘 마스터 인덱스의 첫 번째 층
  - [[day-23-review/concept|Day 23 — 알고리즘 기초 복습]] — "이미 정렬/단조인가" 서랍. 오늘 마스터 인덱스의 두 번째 층
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 모든 선택의 최종 심판. 제약→복잡도 역산의 근거
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — O(1) 조회로 O(n^2)를 O(n)으로 낮추는 최적화의 핵심 무기
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — "매번 최소/최대 추출"의 표준 도구, Top K의 엔진
  - [[day-24-brute-force/concept|Day 24 — 완전 탐색]] — 막히면 내려갈 기준선. 정당성 검증의 baseline
  - [[day-25-dfs/concept|Day 25 — DFS]] — 경로·연결 요소·조합 탐색의 축
  - [[day-26-bfs/concept|Day 26 — BFS]] — 무가중치 최단 거리·층별 탐색의 축
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 관계를 정점·간선으로. visited의 필요성
  - [[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]] — 사이클 없는 특수 그래프. 부모 회피 순회
  - [[day-31-problem-drilling/concept|Day 31 — 문제 풀이기 시작]] — 오늘 다진 판단 근육으로 실전 기출을 푼다
- 🗺️ **지도(MOC):** [[Phase-3 MOC]] · [[00 Algorithm MOC]]
