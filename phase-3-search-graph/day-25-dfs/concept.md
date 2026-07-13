---
day: 25
phase: 3-search-graph
title: DFS (깊이 우선 탐색 / Depth-First Search)
category: [탐색, 그래프, DFS]
difficulty: 중급
status: done
prev: "[[day-24-brute-force/concept|Day 24 — 완전 탐색]]"
next: "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
related:
  - "[[day-24-brute-force/concept|Day 24 — 완전 탐색]]"
  - "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-27-backtracking/concept|Day 27 — 백트래킹]]"
  - "[[day-07-stack/concept|Day 07 — 스택]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/parts/12421
  - https://school.programmers.co.kr/learn/courses/30/lessons/43165
  - https://school.programmers.co.kr/learn/courses/30/lessons/43162
  - https://school.programmers.co.kr/learn/courses/30/lessons/43164
  - https://leetcode.com/problems/number-of-islands/
  - https://leetcode.com/problems/max-area-of-island/
  - https://leetcode.com/problems/flood-fill/
  - https://leetcode.com/problems/path-sum/
  - https://leetcode.com/problems/number-of-provinces/
  - https://leetcode.com/problems/keys-and-rooms/
  - https://docs.python.org/3/library/sys.html#sys.setrecursionlimit
tags: [phase/3, topic/dfs, topic/search, topic/graph]
---

# Day 25 — DFS (깊이 우선 탐색 / Depth-First Search)

> [!abstract] 한눈 요약 (TL;DR)
> **DFS(깊이 우선 탐색, Depth-First Search)** 는 그래프·트리를 탐색할 때 **"한 방향으로 갈 수 있는 데까지 끝까지 파고든 뒤, 막히면 되돌아와(backtrack) 다른 길을 시도"** 하는 방법이다. 어제 배운 [[day-24-brute-force/concept|완전 탐색(Day 24)]]을 "상태들이 간선(edge)으로 연결된 그래프" 위에서 체계적으로 수행하는 대표 도구가 바로 DFS다. 핵심 엔진은 [[day-22-recursion/concept|재귀(Day 22)]] 또는 [[day-07-stack/concept|스택(Day 07)]]이며, 한 번 방문한 정점을 다시 방문하지 않도록 하는 **visited(방문 체크)** 가 정확성의 생명줄이다. 코테에서 DFS는 ① **격자(grid)에서 연결된 영역 세기**(섬의 개수, 영역 넓이 — flood fill), ② **그래프의 연결 요소(connected component) 개수**, ③ **경로 존재 여부·모든 경로 탐색**, ④ **사이클 판정** 등에 압도적으로 자주 나온다. 시간복잡도는 인접 리스트 기준 **O(V + E)** (정점 수 + 간선 수)로, 방문 체크만 제대로 하면 모든 정점·간선을 딱 한 번씩만 본다. DFS와 [[day-26-bfs/concept|BFS(Day 26)]]는 "탐색 순서(스택 vs 큐)만 다른 쌍둥이"이며, 최단 거리가 필요 없고 "끝까지 파고들어야 하는" 문제에서는 DFS가 코드가 짧고 자연스럽다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **DFS는 "깊이(depth)를 우선"하는 탐색이다.** 현재 정점(node/vertex)에서 갈 수 있는 이웃(adjacent) 중 하나를 골라 **최대한 깊이 들어가고**, 더 갈 곳이 없으면(막다른 길, dead end) 바로 이전 갈림길로 **되돌아와(backtrack)** 아직 안 가본 다른 이웃으로 다시 깊이 들어간다. 모든 정점을 이렇게 훑을 때까지 반복한다.
>
> **일상 비유 — 미로에서 "한 손으로 벽 짚고 걷기".** 미로에 들어가 오른손을 벽에 대고 계속 걷는다고 하자. 갈림길이 나오면 일단 한 방향으로 끝까지 간다. 막다른 길에 부딪히면 되돌아 나와 아직 안 가본 갈림길로 들어간다. 이렇게 "일단 끝까지, 막히면 되돌아"가 DFS의 본질이다. 반대로 [[day-26-bfs/concept|BFS(Day 26)]]는 "출발점에서 가까운 곳부터 물결처럼 동시에 퍼져 나가는" 방식이라 최단 거리를 자연스럽게 구한다.
>
> **왜 완전 탐색의 그래프 버전인가.** [[day-24-brute-force/concept|Day 24]]에서 부분집합·순열을 "선택 → 재귀 → 되돌리기"로 전부 생성했다. 그 "선택의 나무(state tree)"를 그래프로 보면, 각 상태가 정점이고 "다음 선택"이 간선이다. DFS는 바로 그 상태 공간(state space)을 깊이 우선으로 훑는 것이다. 그래서 DFS를 "그래프 위의 완전 탐색"이라 부른다.
>
> **핵심 3요소.** ① **인접 정보**(그래프를 어떻게 표현할지 — 인접 리스트/격자 좌표), ② **visited**(무한 루프와 중복 작업 차단), ③ **재귀 또는 스택**(되돌아가기를 자동/수동으로 처리). 이 셋이 DFS 코드의 뼈대다.

> [!gear]- 2. 동작 원리 (How It Works)
> DFS는 두 가지로 구현한다: **재귀(recursive)** 와 **명시적 스택(iterative)**. 둘의 탐색 순서는 본질적으로 같다 — 재귀의 호출 스택(call stack)이 스택 자료구조를 대신할 뿐이다.
>
> **(A) 재귀 DFS — 가장 흔하고 짧다.**
> ```
> visited = set()
> def dfs(u):
>     visited.add(u)          # 1) 지금 정점 방문 처리
>     work(u)                 # 2) 필요한 작업(카운트/기록)
>     for v in graph[u]:      # 3) 이웃들을 하나씩
>         if v not in visited:
>             dfs(v)          # 4) 안 가본 이웃으로 깊이 들어감
> ```
> 함수가 자기 자신을 부르며 "더 깊이" 내려가고, 이웃을 다 보면 `return` 하며 자동으로 "되돌아온다". 되돌아가기(backtrack)를 파이썬 호출 스택이 공짜로 처리해 준다.
>
> **(B) 스택 DFS — 재귀 깊이 한계를 피할 때.**
> ```
> def dfs(start):
>     stack = [start]
>     visited = {start}
>     while stack:
>         u = stack.pop()          # LIFO: 가장 최근 것을 꺼냄
>         work(u)
>         for v in graph[u]:
>             if v not in visited:
>                 visited.add(v)   # push할 때 방문 표시(중복 push 방지)
>                 stack.append(v)
> ```
> `pop()`이 **가장 최근에 넣은 정점**을 꺼내므로(LIFO) 자연히 깊이 우선이 된다. `deque`의 `pop()`(오른쪽)을 써도 된다. BFS와 비교하면 **자료구조만 스택->큐로 바꾸면 BFS**가 된다.
>
> **추적 예시 — 아래 그래프에서 1부터 DFS(이웃은 오름차순 방문).**
> ```
>       1
>      / \
>     2   3
>    / \   \
>   4   5   6
>
> 방문 순서: 1 -> 2 -> 4 -> (4막힘, 되돌아) 5 -> (되돌아) 3 -> 6
> 재귀 호출: dfs(1){ dfs(2){ dfs(4); dfs(5) }; dfs(3){ dfs(6) } }
> ```
>
> **(C) 격자(grid) DFS — 코테 최다 유형.** 2차원 지도에서는 각 칸 `(r, c)`가 정점, 상하좌우 인접 칸이 이웃이다. 방향 벡터로 이웃을 순회한다.
> ```
> dr = [-1, 1, 0, 0]          # 상 하
> dc = [0, 0, -1, 1]          # 좌 우
> def dfs(r, c):
>     visited[r][c] = True
>     for d in range(4):
>         nr, nc = r + dr[d], c + dc[d]
>         if 0 <= nr < R and 0 <= nc < C and not visited[nr][nc] and grid[nr][nc] == 1:
>             dfs(nr, nc)
> ```
> 경계 검사(`0 <= nr < R`)와 방문·조건 검사를 이웃마다 반드시 해야 한다. 섬의 개수·영역 넓이·flood fill이 전부 이 골격의 변형이다.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> DFS는 **모든 정점을 1번, 모든 간선을 1번씩** 본다(visited 덕분). 그래프 표현 방식에 따라 복잡도가 갈린다.
>
> | 대상 / 표현 | 시간복잡도 | 공간복잡도 | 설명 |
> |---|---|---|---|
> | 인접 리스트(adjacency list) | O(V + E) | O(V) | 정점 V개 + 간선 E개를 각 1회. 가장 효율적 |
> | 인접 행렬(adjacency matrix) | O(V^2) | O(V) | 이웃 찾을 때 한 행(V칸)을 전부 훑음 |
> | 격자 R x C | O(R x C) | O(R x C) | 칸 수만큼. 각 칸 상하좌우 상수 개 이웃 |
>
> > **왜 O(V + E)인가.** `dfs(u)`는 정점 u당 딱 한 번 호출된다(visited가 재호출 차단). 각 호출에서 u의 이웃을 훑는데, 모든 정점의 이웃 수를 합하면 간선 수의 2배(무방향)이므로 간선 훑기 총합은 O(E). 따라서 O(V) + O(E) = **O(V + E)**.
> >
> > **공간복잡도의 두 축.** ① `visited` 배열 O(V), ② 재귀 호출 스택 깊이 — 최악의 경우(일자형 그래프/한 줄 격자) O(V)까지 쌓인다. 그래서 정점이 매우 많으면(수만~수십만) **재귀 깊이 초과(RecursionError)** 위험이 있어 스택 DFS나 `sys.setrecursionlimit` 상향이 필요하다.
> >
> > **인접 행렬은 왜 O(V^2)인가.** 이웃을 찾으려면 `matrix[u][0..V-1]` 한 줄을 전부 검사해야 한다. 정점마다 V칸을 보니 V x V = O(V^2). 프로그래머스 [네트워크(#43162)](https://school.programmers.co.kr/learn/courses/30/lessons/43162)가 인접 행렬 입력이라 O(n^2)이다(n<=200이라 충분히 빠름).

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"연결된 덩어리를 세라"는 문제는 DFS/BFS 신호다.** "섬의 개수", "네트워크(연결 요소)의 수", "그림에서 같은 색 영역", "무리(그룹) 개수" 같은 표현이 나오면 격자/그래프 DFS를 떠올려라. 미방문 정점에서 DFS를 시작한 **횟수**가 곧 연결 요소의 수다.
>   - 참고: [프로그래머스 DFS/BFS 문제집](https://school.programmers.co.kr/learn/courses/30/parts/12421)
> - **DFS vs BFS 선택 기준.** "최단 거리/최소 단계"면 [[day-26-bfs/concept|BFS(Day 26)]], 그 외 "존재 여부·전부 방문·모든 경로·사이클"이면 DFS가 대개 더 짧고 자연스럽다. 단순 연결 요소 세기는 둘 다 되므로 편한 쪽을 쓰면 된다.
> - **재귀 깊이 한계를 기억하라.** 파이썬 기본 재귀 한도는 1000이다. 정점이 그보다 많거나 한 줄로 길게 이어지면 `RecursionError`가 난다. 대비책: 코드 상단에 `import sys; sys.setrecursionlimit(10**6)` 또는 스택 기반 반복 DFS로 전환.
>   - 참고: [sys.setrecursionlimit (Python 공식 문서)](https://docs.python.org/3/library/sys.html#sys.setrecursionlimit)
> - **visited는 "언제 표시하느냐"가 관건.** 재귀 DFS는 `dfs(u)` **진입 즉시** 방문 표시, 스택 DFS는 **push하는 순간** 방문 표시(pop할 때 표시하면 같은 정점이 스택에 여러 번 들어가 중복 작업 발생).
> - **방향 벡터(dr, dc)로 격자 이웃을 깔끔하게.** 상하좌우를 `dr=[-1,1,0,0], dc=[0,0,-1,1]`로 묶으면 `if`문 4개를 반복문 하나로 줄여 실수를 막는다. 대각선까지면 8방향으로 확장한다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **visited 없는 DFS는 무한 루프다.** 그래프에 사이클(cycle)이 있으면 방문 체크 없이는 `A -> B -> A -> B ...`로 영원히 돈다. **정점을 방문하면 즉시 표시**하는 것이 DFS의 절대 규칙. (트리는 사이클이 없어 부모만 안 밟으면 되지만, 일반 그래프는 반드시 visited 필요.)
> 2. **파이썬 재귀 한도(기본 1000)를 넘으면 RecursionError.** 정점 수가 크면(수천 이상) 재귀 DFS는 터질 수 있다. `sys.setrecursionlimit` 상향 또는 스택 DFS로 전환. 단, 재귀 한도를 너무 높이면 실제 콜스택 초과로 인터프리터가 죽을 수도 있으니 반복 DFS가 더 안전할 때가 많다.
> 3. **DFS는 최단 경로를 보장하지 않는다.** DFS가 먼저 찾은 경로가 최단이라는 보장은 전혀 없다. 최단 거리·최소 이동 횟수 문제는 반드시 [[day-26-bfs/concept|BFS(Day 26)]](또는 가중치가 있으면 다익스트라)로 풀어야 한다. "DFS로 최단거리" 시도는 대표적 오답 패턴.
> 4. **가중치 없는 그래프에서만 "단계 = 거리"가 성립.** 간선마다 비용이 다르면 DFS/BFS 둘 다 최단 비용을 못 준다(-> 다익스트라/벨만-포드, Phase 4). 오늘 다루는 DFS는 가중치 없는 연결·경로 문제 전용으로 이해하라.
> 5. **격자 문제의 경계 검사(boundary check)를 빠뜨리지 마라.** `0 <= nr < R and 0 <= nc < C`를 이웃 접근 **전에** 검사해야 `IndexError`나 음수 인덱스로 인한 잘못된 순환(파이썬은 `grid[-1]`이 뒤에서 접근되어 조용히 틀림)을 막는다. 격자 DFS 최다 버그.
> 6. **visited를 격자에 직접 표시(값 덮어쓰기)해도 된다.** 별도 visited 배열 대신 방문한 칸의 `grid[r][c]`를 `0`으로 바꾸면 "방문 = 물로 만들기"가 되어 메모리를 아낀다(LeetCode Number of Islands 정석). 단 입력을 변형하므로 원본이 필요하면 복사하거나 별도 visited를 써라.
> 7. **연결 요소(connected component) 개수 = DFS를 새로 시작한 횟수.** 모든 정점을 순회하며 "미방문이면 DFS 시작 + 카운트 +1"을 반복한다. 이 패턴이 "섬의 개수", "네트워크 수", "Number of Provinces"의 공통 뼈대다.
> 8. **재귀 DFS에서 상태 되돌리기(backtrack)가 필요한 경우.** "모든 경로 나열"처럼 경로를 쌓아가는 문제는 `path.append` 후 재귀, 돌아와서 `path.pop`을 해야 한다([[day-24-brute-force/concept|Day 24]]·[[day-27-backtracking/concept|Day 27 백트래킹]]의 undo와 동일). 단순 방문(연결 요소 세기)은 되돌릴 필요가 없다 — 여기서 백트래킹과 순수 순회 DFS가 갈린다.
> 9. **DFS와 백트래킹의 관계.** [[day-27-backtracking/concept|백트래킹(Day 27)]]은 "DFS로 상태 공간을 탐색하되, 가망 없는 가지를 조기 포기(pruning)"하는 것이다. 즉 백트래킹 ⊂ DFS. 오늘 DFS 골격을 확실히 익히면 백트래킹이 그 위의 최적화로 자연스럽게 이어진다.

> [!example]- 예제 코드 (Examples)
> ```python
> import sys
> from collections import defaultdict
>
> # 1) 재귀 DFS (인접 리스트) - 방문 순서 반환
> def dfs_recursive(graph, start):
>     visited, order = set(), []
>     def go(u):
>         visited.add(u)
>         order.append(u)
>         for v in graph[u]:          # 이웃을 정렬해 두면 순서가 결정적
>             if v not in visited:
>                 go(v)
>     go(start)
>     return order
>
> # 2) 스택 DFS (반복) - 재귀 깊이 한계 회피
> def dfs_iterative(graph, start):
>     visited, order = {start}, []
>     stack = [start]
>     while stack:
>         u = stack.pop()             # LIFO
>         order.append(u)
>         for v in sorted(graph[u], reverse=True):  # 재귀와 순서 맞추기
>             if v not in visited:
>                 visited.add(v)      # push 시점에 방문 표시
>                 stack.append(v)
>     return order
>
> # 3) 격자 DFS - 섬(1로 연결된 영역)의 개수
> def count_islands(grid):
>     if not grid:
>         return 0
>     R, C = len(grid), len(grid[0])
>     seen = [[False] * C for _ in range(R)]
>     dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
>     def dfs(r, c):
>         seen[r][c] = True
>         for d in range(4):
>             nr, nc = r + dr[d], c + dc[d]
>             if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc] and grid[nr][nc] == 1:
>                 dfs(nr, nc)
>     count = 0
>     for r in range(R):
>         for c in range(C):
>             if grid[r][c] == 1 and not seen[r][c]:
>                 dfs(r, c)           # 새 섬 발견
>                 count += 1
>     return count
>
> # 4) 연결 요소 개수 (일반 그래프)
> def count_components(n, edges):
>     graph = defaultdict(list)
>     for a, b in edges:
>         graph[a].append(b)
>         graph[b].append(a)
>     visited = set()
>     def go(u):
>         visited.add(u)
>         for v in graph[u]:
>             if v not in visited:
>                 go(v)
>     comp = 0
>     for u in range(n):
>         if u not in visited:
>             go(u)
>             comp += 1
>     return comp
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 격자 DFS(섬/영역), 그래프 연결 요소, 상태 공간 DFS, 트리 DFS를 골고루 담았다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | 번호 | 문제 | 출처 | 난이도 | 형태 |
> |---|---|---|---|---|
> | 1 | Flood Fill | [LeetCode #733](https://leetcode.com/problems/flood-fill/) | 🟢기초 | 격자 DFS(영역 칠하기) |
> | 2 | Number of Islands | [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | 🟡중급 | 격자 DFS(연결 영역 세기) |
> | 3 | Max Area of Island | [LeetCode #695](https://leetcode.com/problems/max-area-of-island/) | 🟡중급 | 격자 DFS(영역 넓이) |
> | 4 | 타겟 넘버 | [프로그래머스 #43165](https://school.programmers.co.kr/learn/courses/30/lessons/43165) | 🟡중급 | 상태 공간 DFS(+/-) |
> | 5 | 네트워크 | [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162) | 🟡중급 | 인접 행렬 연결 요소 |
> | 6 | Number of Provinces | [LeetCode #547](https://leetcode.com/problems/number-of-provinces/) | 🟡중급 | 인접 행렬 연결 요소 |
> | 7 | Path Sum | [LeetCode #112](https://leetcode.com/problems/path-sum/) | 🟢기초 | 트리 DFS(경로 합) |
> | 8 | Keys and Rooms | [LeetCode #841](https://leetcode.com/problems/keys-and-rooms/) | 🟡중급 | 그래프 도달 가능성 |
> | 9 | 여행경로 | [프로그래머스 #43164](https://school.programmers.co.kr/learn/courses/30/lessons/43164) | 🔴심화 | DFS + 백트래킹(경로 구성) |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근(재귀 DFS vs 스택 DFS, visited 배열 vs 격자 덮어쓰기) 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-24-brute-force/concept|Day 24 — 완전 탐색]] — "모든 후보를 빠짐없이"라는 완전 탐색을 그래프/상태 공간 위에서 깊이 우선으로 체계화한 것이 DFS다
- ➡️ **다음(next):** [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — 탐색 순서를 스택->큐로만 바꾼 쌍둥이. 최단 거리는 BFS의 몫
- 🧭 **관련(related):**
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 재귀 DFS의 "깊이 들어가고 되돌아오기"가 곧 재귀 호출/반환이다
  - [[day-07-stack/concept|Day 07 — 스택]] — 반복 DFS의 엔진이 스택(LIFO). 재귀의 호출 스택과 동일 원리
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 트리는 사이클 없는 그래프라 DFS의 가장 단순한 무대(전위/중위/후위 순회가 곧 DFS)
  - [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — DFS와 자료구조만 다른 짝. 언제 무엇을 쓸지 대비해 익힌다
  - [[day-27-backtracking/concept|Day 27 — 백트래킹]] — DFS에 가지치기(pruning)를 더한 최적화. 백트래킹은 DFS의 부분집합
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 인접 리스트/행렬 등 그래프 표현을 정리하고 DFS/BFS를 그 위에 얹는다
- 🗺️ **지도(MOC):** [[Phase-3 MOC]] · [[00 Algorithm MOC]]
