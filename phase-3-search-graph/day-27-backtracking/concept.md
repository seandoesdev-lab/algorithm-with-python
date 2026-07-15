---
day: 27
phase: 3-search-graph
title: 백트래킹 (Backtracking)
category: [탐색, 백트래킹, 완전탐색, 가지치기]
difficulty: 중급
status: done
prev: "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
next: "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
related:
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-24-brute-force/concept|Day 24 — 완전 탐색]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
  - "[[day-30-review/concept|Day 30 — 개념 집중기 종합 복습]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/lessons/12952
  - https://school.programmers.co.kr/learn/courses/30/lessons/42839
  - https://school.programmers.co.kr/learn/courses/30/lessons/84512
  - https://school.programmers.co.kr/learn/courses/30/lessons/87946
  - https://leetcode.com/problems/subsets/
  - https://leetcode.com/problems/permutations/
  - https://leetcode.com/problems/combinations/
  - https://leetcode.com/problems/combination-sum/
  - https://leetcode.com/problems/generate-parentheses/
  - https://leetcode.com/problems/word-search/
  - https://leetcode.com/problems/n-queens/
  - https://docs.python.org/3/library/itertools.html
tags: [phase/3, topic/backtracking, topic/search, topic/brute-force, topic/pruning]
---

# Day 27 — 백트래킹 (Backtracking)

> [!abstract] 한눈 요약 (TL;DR)
> **백트래킹(Backtracking)** 은 **"부분해(partial solution)를 한 단계씩 쌓아 나가다가, 이대로는 절대 답이 될 수 없다고 판단되는 순간 즉시 되돌아가(backtrack) 다른 선택을 시도"** 하는 탐색 기법이다. 본질은 [[day-24-brute-force/concept|완전 탐색(Day 24)]] — 모든 후보를 빠짐없이 검사한다 — 이지만, **가망 없는 가지(branch)를 미리 잘라내는 가지치기(pruning)** 로 탐색 공간을 극적으로 줄인다는 점이 결정적이다. 엔진은 [[day-25-dfs/concept|DFS(Day 25)]]와 [[day-22-recursion/concept|재귀(Day 22)]]이며, **백트래킹 ⊂ DFS** — "상태 공간 트리(state-space tree)를 DFS로 훑되, 유망성(promising) 검사로 조기 포기하는 DFS"가 정확한 정의다. 코드의 심장은 **선택(choose) → 재귀(explore) → 되돌리기(undo)** 3박자다. 코테에서 백트래킹은 ① **부분집합·조합·순열 전수 생성**(subsets, combinations, permutations), ② **제약 만족 문제**(N-Queens, 스도쿠, 격자 단어 찾기), ③ **합/목표 조건을 만족하는 조합 나열**(combination sum) 등 "모든 경우를 만들되 불가능한 건 빨리 버려야 하는" 문제에 압도적으로 나온다. 시간복잡도는 최악에는 지수(exponential)지만, 가지치기가 실전 성능을 좌우한다. **"가능한 모든 조합/순열/배치를 구하라"** 가 보이면 백트래킹을 떠올려라.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **백트래킹은 "일단 해 보고, 안 되면 무르는(undo) 완전 탐색"이다.** 문제의 해를 여러 개의 결정(decision)으로 나누고, 결정을 하나씩 내리며 부분해를 키워 나간다. 각 단계에서 **"지금까지의 선택이 유효한가(promising)"** 를 검사해, 유효하면 더 깊이 들어가고, 유효하지 않으면 그 선택을 취소하고 다음 후보로 넘어간다. 완성된 부분해가 조건을 모두 만족하면 정답으로 기록한다.
>
> **일상 비유 — 미로에서 실을 풀며 걷기(테세우스의 실).** 갈림길마다 한 길을 골라 실을 풀며 전진한다. 막다른 길(dead end)을 만나면 **실을 되감으며(backtrack)** 마지막 갈림길로 돌아와 아직 안 가본 다른 길을 택한다. 여기서 "실을 되감는 행위"가 백트래킹의 **undo(원상 복구)** 이고, "이 길은 벽으로 막혀 있으니 들어가지 않는다"가 **가지치기(pruning)** 다. 완전 탐색이 "모든 길을 끝까지 다 걸어 본다"면, 백트래킹은 "막힐 게 뻔한 길은 애초에 들어가지 않는다".
>
> **완전 탐색과 무엇이 다른가.** 순수 완전 탐색은 모든 후보를 **끝까지 만든 뒤** 조건을 검사한다(generate-then-test). 백트래킹은 **만드는 도중에** 조건 위반을 감지하면 즉시 멈춘다(prune-as-you-build). 예컨대 N-Queens에서 완전 탐색은 N개의 퀸을 모두 놓은 8^8가지 배치를 만든 뒤 충돌을 검사하지만, 백트래킹은 퀸 하나를 놓을 때마다 "이전 퀸과 충돌하는가"를 검사해 충돌하면 그 자리에서 접는다. 만들어지는 배치의 수가 수천 배 줄어든다.
>
> **핵심 3요소.** ① **상태(state)** — 지금까지의 부분해(선택한 원소 리스트, 놓은 퀸의 위치 등), ② **선택지(choices)** — 현재 단계에서 시도할 후보들, ③ **유망성 검사(pruning)** — "이 선택으로 계속 가면 답이 될 가능성이 있는가". 이 셋이 백트래킹 코드의 뼈대다.

> [!gear]- 2. 동작 원리 (How It Works)
> 백트래킹의 표준 골격은 **선택(choose) → 재귀(explore) → 되돌리기(undo)** 다. 재귀 함수가 상태 공간 트리를 DFS로 내려가며, 한 선택을 시도하고, 돌아오면 그 선택을 취소해 형제 가지(sibling branch)에 영향이 남지 않게 한다.
>
> **(A) 표준 골격 — choose / explore / undo.**
> ```
> def backtrack(state):
>     if is_solution(state):        # 1) 완성된 해인가?
>         record(state)             #    정답 기록(보통 복사본 append)
>         return
>     for choice in candidates(state):
>         if not promising(state, choice):   # 2) 가지치기: 가망 없으면 건너뜀
>             continue
>         apply(state, choice)      # 3) choose: 선택을 상태에 반영
>         backtrack(state)          # 4) explore: 그 선택 위에서 더 깊이
>         undo(state, choice)       # 5) undo: 선택 취소(원상 복구)
> ```
> `undo`가 백트래킹의 정체성이다. `apply` 후 재귀에서 돌아오면 반드시 그 변경을 되돌려, 같은 깊이의 다음 후보가 "깨끗한 상태"에서 시작하게 한다. 이 대칭(append↔pop, add↔remove, 표시↔해제)이 무너지면 형제 가지가 서로 오염된다.
>
> **(B) 부분집합(subsets) — "포함/불포함" 이진 결정.** 각 원소를 넣을지 말지 두 갈래로 분기한다.
> ```
> def subsets(nums):
>     res, path = [], []
>     def dfs(i):
>         if i == len(nums):
>             res.append(path[:])          # 복사본(얕은 복사) 기록
>             return
>         dfs(i + 1)                       # 원소 i 불포함
>         path.append(nums[i])             # choose: 포함
>         dfs(i + 1)
>         path.pop()                       # undo
>     dfs(0)
>     return res                           # 2^n개
> ```
>
> **(C) 순열(permutations) — used 배열로 중복 사용 차단.** 매 자리마다 아직 안 쓴 원소를 하나씩 놓는다.
> ```
> def permute(nums):
>     res, path, used = [], [], [False] * len(nums)
>     def dfs():
>         if len(path) == len(nums):
>             res.append(path[:]); return
>         for i in range(len(nums)):
>             if used[i]:
>                 continue                 # 이미 쓴 원소는 가지치기
>             used[i] = True; path.append(nums[i])   # choose
>             dfs()                                    # explore
>             path.pop(); used[i] = False              # undo
>     dfs()
>     return res                           # n!개
> ```
>
> **(D) 조합(combinations) — start 인덱스로 순서 고정.** "뒤로만 고른다"로 (1,2)와 (2,1)의 중복을 원천 차단한다.
> ```
> def combine(n, k):
>     res, path = [], []
>     def dfs(start):
>         if len(path) == k:
>             res.append(path[:]); return
>         for x in range(start, n + 1):    # start부터만 → 오름차순 조합
>             path.append(x)               # choose
>             dfs(x + 1)                   # 다음은 x보다 큰 것만
>             path.pop()                   # undo
>     dfs(1)
>     return res
> ```
>
> **(E) 상태 공간 트리 그림 — subsets([1,2]) DFS 순회.**
> ```
>                 []                     (i=0)
>            /(불포함)      \(포함 1)
>          []                [1]         (i=1)
>       /(x2)  \(+2)      /(x2)  \(+2)
>      []      [2]       [1]     [1,2]   (i=2, 해 기록)
>
> 기록 순서: [] -> [2] -> [1] -> [1,2]
> ```
> 각 리프(leaf)가 완성된 부분집합이고, 트리를 DFS로 내려가며 `path`를 쌓고(내려갈 때) 되돌린다(올라올 때).
>
> **(F) 가지치기(pruning)가 핵심인 예 — N-Queens.** 퀸을 행 단위로 한 개씩 놓되, 열·두 대각선의 사용 여부를 집합으로 관리해 충돌하면 즉시 접는다.
> ```
> def solve(n):
>     cols, diag, anti = set(), set(), set()   # 열, ↘대각(r-c), ↙대각(r+c)
>     res = [0]
>     def place(r):
>         if r == n:
>             res[0] += 1; return
>         for c in range(n):
>             if c in cols or (r - c) in diag or (r + c) in anti:
>                 continue                     # 가지치기
>             cols.add(c); diag.add(r - c); anti.add(r + c)   # choose
>             place(r + 1)                                    # explore
>             cols.discard(c); diag.discard(r - c); anti.discard(r + c)  # undo
>     place(0)
>     return res[0]
> ```

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> 백트래킹의 시간은 **"상태 공간 트리의 노드 수 × 노드당 작업량"** 이다. 가지치기가 없으면 완전 탐색과 같은 지수 규모이고, 가지치기가 좋을수록 실제 방문 노드가 줄어 빨라진다(최악 복잡도는 그대로여도 실전은 극적으로 빨라짐).
>
> | 문제 유형 | 해의 개수(하한) | 시간복잡도(대략) | 설명 |
> |---|---|---|---|
> | 부분집합(subsets) | 2^n | O(2^n x n) | 각 부분집합을 복사해 기록하니 x n |
> | 순열(permutations) | n! | O(n! x n) | n!개 각각 길이 n을 복사 |
> | 조합 nCk(combinations) | nCk | O(nCk x k) | start로 중복 제거 후 조합 수만큼 |
> | N-Queens | 배치 수 | O(N!)보다 훨씬 작음 | 열·대각 가지치기로 대폭 감소 |
> | 조합 합(combination sum) | 가변 | 지수 | 남은 목표<0이면 가지치기 |
>
> > **왜 지수인가.** 각 단계에서 여러 선택으로 분기하므로 트리의 노드 수가 깊이에 대해 지수적으로 늘어난다. 부분집합은 원소마다 2갈래라 2^n, 순열은 첫 자리 n개 × 둘째 n-1개 × … = n!. 이것은 "출력해야 하는 답의 개수" 자체가 지수/팩토리얼이라 **알고리즘을 아무리 개선해도 피할 수 없는 하한**이다(전수 생성 문제의 본질).
> >
> > **가지치기는 최악 복잡도를 바꾸지 못한다 — 실전 상수를 바꾼다.** N-Queens의 최악 상한은 여전히 크지만, 열·대각선 충돌을 미리 걸러 실제로 방문하는 노드가 급감한다. 코테에서 "완전 탐색은 시간초과, 백트래킹은 통과"가 갈리는 지점이 바로 이 가지치기다. **좋은 가지치기 = 빠른 백트래킹.**
> >
> > **공간복잡도.** 재귀 깊이만큼의 호출 스택 O(깊이) + 현재 부분해 `path` O(깊이) + used/방문 집합 O(n). 보통 **O(n)** (해를 모두 저장하는 출력 공간은 별도로 O(해의 개수 × 해의 길이)). DFS 기반이므로 [[day-25-dfs/concept|Day 25]]처럼 재귀 깊이가 크면 `RecursionError`에 유의.
> >
> > **itertools로 대체 가능한 경우.** 단순 조합/순열/곱집합은 표준 라이브러리 `itertools.permutations / combinations / product`가 C 구현이라 더 빠르고 간결하다. **가지치기·제약 조건이 없으면 itertools, 있으면 직접 백트래킹.**

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"모든 경우의 수를 구하라 / 가능한 조합·순열·배치를 나열하라"는 백트래킹 신호다.** "모든 부분집합", "가능한 모든 순서", "조건을 만족하는 모든 방법", "퀸을 배치하는 경우의 수"가 보이면 상태 공간 트리 + choose/explore/undo를 떠올려라.
>   - 참고: [프로그래머스 완전탐색 문제집](https://school.programmers.co.kr/learn/courses/30/parts/12230)
> - **정답을 기록할 때 반드시 "복사본"을 넣어라.** `res.append(path)`는 같은 리스트의 참조를 넣는 것이라, 이후 `path`가 바뀌면 이미 넣은 답까지 함께 바뀐다(전부 마지막 상태가 됨). `res.append(path[:])` 또는 `list(path)`로 **얕은 복사(shallow copy)** 를 넣어야 한다. 백트래킹 버그 1순위.
> - **`undo`는 `choose`의 정확한 역연산이어야 한다.** `append`↔`pop`, `add`↔`discard`, `used[i]=True`↔`used[i]=False`. 상태를 건드리는 모든 곳에 짝을 맞춰라. 하나라도 빠지면 형제 가지가 오염된다.
> - **조합에는 `start` 인덱스, 순열에는 `used` 배열.** 순서가 중요하지 않으면(조합) `start`로 "뒤로만 고르기", 순서가 중요하면(순열) `used`로 "안 쓴 것만 고르기". 이 둘의 구분이 중복 제거의 핵심이다.
> - **가지치기는 "빠를수록, 위쪽 노드일수록" 이득이 크다.** 트리 상단에서 큰 가지를 자르면 그 아래 전체가 사라진다. combination sum에서 배열을 정렬해 두고 "남은 목표 < 현재 후보"면 이후 모두 건너뛰는 것이 대표적. 가지치기 조건을 재귀 진입 직후·후보 루프 안 최대한 이른 지점에 둬라.
> - **중복 원소가 있는 순열/조합은 "같은 깊이에서 같은 값 스킵"으로 중복 제거.** 정렬 후 `if i > start and nums[i] == nums[i-1]: continue` 패턴(Subsets II / Combination Sum II). 순수 백트래킹의 흔한 심화 포인트.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **백트래킹 ⊂ DFS ⊂ 완전 탐색.** 백트래킹은 "가지치기하는 DFS"이고, DFS는 상태 공간을 훑는 완전 탐색의 한 방식이다. 셋의 포함 관계를 이해하면 [[day-24-brute-force/concept|Day 24]]·[[day-25-dfs/concept|Day 25]]와 오늘이 하나로 꿰어진다. "새로운 알고리즘"이 아니라 "DFS + 조기 포기"다.
> 2. **정답 기록은 복사본으로.** (팁에서도 강조) `res.append(path[:])`. 참조를 그대로 넣으면 모든 답이 동일해지는 치명적 버그. 2차원 결과(N-Queens 보드 등)는 깊은 복사(각 행 복사)가 필요할 수 있다.
> 3. **choose와 undo는 반드시 짝을 이룬다.** 재귀에서 돌아온 뒤 상태를 원복하지 않으면, 같은 레벨의 다음 후보가 이전 선택의 잔재를 물려받아 틀린 답·중복 답이 나온다. 격자 문제의 `visited[r][c]=True` 뒤에는 반드시 `visited[r][c]=False`.
> 4. **가지치기 없는 백트래킹은 완전 탐색과 같아 시간초과 위험.** 제약이 있는 문제(N-Queens, 스도쿠, combination sum)에서 유망성 검사를 빼면 지수 공간을 전부 방문해 TLE. **문제의 제약을 최대한 이른 시점에 검사**하는 것이 통과의 핵심.
> 5. **재귀 깊이 한계.** 파이썬 기본 재귀 한도는 1000. 깊이가 크면 `import sys; sys.setrecursionlimit(...)`. 단 백트래킹은 깊이가 대개 입력 크기 n 수준이라 문제되는 경우는 드물다(오히려 폭이 지수라 시간이 병목).
> 6. **가지치기와 정답 조건을 혼동하지 마라.** "지금 상태가 완성된 정답인가"(is_solution)와 "이 상태에서 계속 갈 가치가 있는가"(promising)는 다른 검사다. 전자는 기록·return, 후자는 continue. 둘을 섞으면 답을 놓치거나 잘못 자른다.
> 7. **순서 유무로 조합 vs 순열을 정확히 골라라.** "(1,2)와 (2,1)이 같은가?" 같으면 조합(start), 다르면 순열(used). 문제를 잘못 모델링하면 답 개수가 통째로 틀린다. 프로그래머스 [소수 찾기(#42839)](https://school.programmers.co.kr/learn/courses/30/lessons/42839)는 자릿수 순열로 수를 만들어 소수를 세는 순열형이다.
> 8. **제약 검사를 O(1)로 만드는 자료구조를 써라.** N-Queens에서 매번 보드 전체를 훑어 충돌을 검사하면 느리다. 열·↘대각(r-c)·↙대각(r+c)을 **집합(set)** 으로 관리하면 충돌 검사·표시·해제가 모두 O(1). 이 최적화가 실전 속도를 좌우한다.
> 9. **가지치기·제약이 없으면 `itertools`가 정답.** 순수 조합/순열/곱집합 전수 생성은 `itertools.combinations/permutations/product`가 더 빠르고 버그가 없다. 직접 백트래킹은 "생성 도중 조건으로 가지를 쳐야 할 때"만 이득이다. 도구를 상황에 맞게 골라라.
>   - 참고: [itertools (Python 공식 문서)](https://docs.python.org/3/library/itertools.html)

> [!example]- 예제 코드 (Examples)
> ```python
> # 1) 부분집합 (subsets) - 포함/불포함 이진 결정, 2^n개
> def subsets(nums):
>     res, path = [], []
>     def dfs(i):
>         if i == len(nums):
>             res.append(path[:])          # 복사본 기록
>             return
>         dfs(i + 1)                       # 불포함
>         path.append(nums[i])             # choose(포함)
>         dfs(i + 1)                       # explore
>         path.pop()                       # undo
>     dfs(0)
>     return res
>
> # 2) 순열 (permutations) - used 배열, n!개
> def permutations(nums):
>     res, path, used = [], [], [False] * len(nums)
>     def dfs():
>         if len(path) == len(nums):
>             res.append(path[:])
>             return
>         for i in range(len(nums)):
>             if used[i]:
>                 continue                 # 가지치기: 이미 쓴 원소
>             used[i] = True; path.append(nums[i])   # choose
>             dfs()                                    # explore
>             path.pop(); used[i] = False              # undo
>     dfs()
>     return res
>
> # 3) 조합 nCk (combinations) - start로 오름차순 고정
> def combinations(n, k):
>     res, path = [], []
>     def dfs(start):
>         if len(path) == k:
>             res.append(path[:])
>             return
>         # 가지치기: 남은 후보가 부족하면 중단
>         for x in range(start, n - (k - len(path)) + 2):
>             path.append(x)               # choose
>             dfs(x + 1)                   # explore(x보다 큰 것만)
>             path.pop()                   # undo
>     dfs(1)
>     return res
>
> # 4) N-Queens - 열/대각선 집합으로 O(1) 가지치기
> def n_queens_count(n):
>     cols, diag, anti = set(), set(), set()
>     count = 0
>     def place(r):
>         nonlocal count
>         if r == n:
>             count += 1
>             return
>         for c in range(n):
>             if c in cols or (r - c) in diag or (r + c) in anti:
>                 continue                 # 충돌 → 가지치기
>             cols.add(c); diag.add(r - c); anti.add(r + c)   # choose
>             place(r + 1)                                     # explore
>             cols.discard(c); diag.discard(r - c); anti.discard(r + c)  # undo
>     place(0)
>     return count
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 부분집합·순열·조합의 기본형부터 제약 만족(N-Queens, 격자 단어 찾기)까지 백트래킹의 대표 패턴을 골고루 담았다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | 번호 | 문제 | 출처 | 난이도 | 형태 |
> |---|---|---|---|---|
> | 1 | Subsets | [LeetCode #78](https://leetcode.com/problems/subsets/) | 🟢기초 | 부분집합 생성 |
> | 2 | Permutations | [LeetCode #46](https://leetcode.com/problems/permutations/) | 🟡중급 | 순열 생성(used) |
> | 3 | Combinations | [LeetCode #77](https://leetcode.com/problems/combinations/) | 🟡중급 | 조합 생성(start) |
> | 4 | Combination Sum | [LeetCode #39](https://leetcode.com/problems/combination-sum/) | 🟡중급 | 합 조건 + 가지치기 |
> | 5 | Generate Parentheses | [LeetCode #22](https://leetcode.com/problems/generate-parentheses/) | 🟡중급 | 유효성 가지치기 |
> | 6 | 소수 찾기 | [프로그래머스 #42839](https://school.programmers.co.kr/learn/courses/30/lessons/42839) | 🟡중급 | 자릿수 순열 + 소수 |
> | 7 | 모음사전 | [프로그래머스 #84512](https://school.programmers.co.kr/learn/courses/30/lessons/84512) | 🟡중급 | 사전순 DFS 생성 |
> | 8 | 피로도 | [프로그래머스 #87946](https://school.programmers.co.kr/learn/courses/30/lessons/87946) | 🟡중급 | 방문 순열 완전탐색 |
> | 9 | Word Search | [LeetCode #79](https://leetcode.com/problems/word-search/) | 🟡중급 | 격자 백트래킹(visited 원복) |
> | 10 | N-Queens | [LeetCode #51](https://leetcode.com/problems/n-queens/) | 🔴심화 | 제약 만족 + 대각선 가지치기 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근(직접 백트래킹 vs itertools, start vs used, 가지치기 유무) 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — 최단 거리를 보장하는 너비 우선 탐색. 백트래킹은 그 짝인 깊이 우선 탐색에 가지치기를 더한 것
- ➡️ **다음(next):** [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 인접 리스트/행렬로 그래프를 표현하고 그 위에 DFS/BFS/백트래킹을 얹어 정리한다
- 🧭 **관련(related):**
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 백트래킹은 곧 "가지치기하는 DFS"다. choose/explore/undo가 DFS의 진입/재귀/반환과 정확히 대응
  - [[day-24-brute-force/concept|Day 24 — 완전 탐색]] — 백트래킹의 본질은 완전 탐색. "만든 뒤 검사"를 "만들며 검사(조기 포기)"로 바꾼 것
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 백트래킹은 재귀의 "선택→되돌리기" 구조 위에 세워진다. 재귀 호출/반환이 트리 탐색을 자동화
  - [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — 탐색 순서(스택/재귀 vs 큐)의 대비. 최단은 BFS, 전수 생성·제약 만족은 백트래킹
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 상태 공간을 그래프로 보는 관점을 정리하며 탐색 삼총사를 통합
  - [[day-30-review/concept|Day 30 — 개념 집중기 종합 복습]] — 완전탐색·DFS·BFS·백트래킹을 한자리에서 비교·정리
- 🗺️ **지도(MOC):** [[Phase-3 MOC]] · [[00 Algorithm MOC]]
