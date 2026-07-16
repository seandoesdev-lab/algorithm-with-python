---
day: 28
phase: 3-search-graph
title: 그래프 표현과 순회 (Graph Representation & Traversal)
category: [그래프, 자료구조, 탐색, 인접리스트, 인접행렬]
difficulty: 중급
status: done
prev: "[[day-27-backtracking/concept|Day 27 — 백트래킹 (Backtracking)]]"
next: "[[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]]"
related:
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
  - "[[day-27-backtracking/concept|Day 27 — 백트래킹 (Backtracking)]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]]"
  - "[[day-30-review/concept|Day 30 — 개념 집중기 종합 복습]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/lessons/43162
  - https://school.programmers.co.kr/learn/courses/30/lessons/43164
  - https://leetcode.com/problems/find-if-path-exists-in-graph/
  - https://leetcode.com/problems/find-center-of-star-graph/
  - https://leetcode.com/problems/find-the-town-judge/
  - https://leetcode.com/problems/number-of-provinces/
  - https://leetcode.com/problems/number-of-islands/
  - https://leetcode.com/problems/keys-and-rooms/
  - https://leetcode.com/problems/clone-graph/
  - https://leetcode.com/problems/all-paths-from-source-to-target/
  - https://docs.python.org/3/library/collections.html#collections.defaultdict
  - https://docs.python.org/3/library/collections.html#collections.deque
tags: [phase/3, topic/graph, topic/adjacency-list, topic/adjacency-matrix, topic/traversal, topic/search]
---

# Day 28 — 그래프 표현과 순회 (Graph Representation & Traversal)

> [!abstract] 한눈 요약 (TL;DR)
> **그래프(Graph)** 는 **정점(vertex/node)** 들과 그들을 잇는 **간선(edge)** 으로 이루어진, 세상에서 가장 일반적인 관계 자료구조다. 도로망·SNS 친구 관계·웹 링크·작업 의존성이 전부 그래프다. 코테에서 그래프 문제의 승부는 **① 입력을 어떤 자료구조로 "표현(represent)"할 것인가** 와 **② 그 위를 어떻게 "순회(traverse)"할 것인가** 두 단계로 갈린다. 표현의 양대 방법은 **인접 리스트(adjacency list)** — 각 정점이 자기 이웃 목록을 들고 있는 방식, 대부분의 코테 정답 — 과 **인접 행렬(adjacency matrix)** — `matrix[u][v]=1`로 연결을 표시하는 방식, 정점 수가 작고 간선이 촘촘할 때 유리 — 이다. 순회는 이미 배운 [[day-25-dfs/concept|DFS(Day 25)]]와 [[day-26-bfs/concept|BFS(Day 26)]]를 그대로 얹으면 되지만, **핵심은 "무한 루프를 막는 방문 표시(visited)"** 다 — 트리와 달리 그래프에는 **사이클(cycle)** 이 있어서 방문 체크를 빼면 같은 정점을 영원히 맴돈다. 이 표현+순회 골격 위에서 **연결 요소(connected components) 세기**(프로그래머스 네트워크), **두 정점의 연결성 판정**, **도달 가능한 정점 찾기** 같은 대표 유형이 쏟아진다. **"~들이 서로 연결되어 있나 / 몇 개의 무리인가 / A에서 B로 갈 수 있나"** 가 보이면 그래프를 떠올려라.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **그래프는 "점(정점)과 선(간선)으로 관계를 그린 그림"이다.** 정점 집합 V와 간선 집합 E로 `G = (V, E)`라 쓴다. 트리도 그래프의 특수한 경우(사이클 없고 연결된 그래프)이고, 우리가 [[day-25-dfs/concept|DFS]]·[[day-26-bfs/concept|BFS]]에서 다룬 격자(grid)도 "상하좌우로 이웃과 연결된 그래프"다. 즉 그래프는 지금까지 배운 탐색들이 살던 **무대 그 자체**다.
>
> **일상 비유 — 지하철 노선도.** 역(station)이 정점, 역과 역을 잇는 선로가 간선이다. "강남역에서 홍대입구역까지 갈 수 있나?"는 **연결성(connectivity)**, "몇 정거장 만에 가나?"는 **최단 경로**, "이 노선도가 몇 개의 서로 끊긴 노선망으로 나뉘나?"는 **연결 요소(connected component)** 문제다. 노선도를 종이에 그리는 방식이 "표현", 손가락으로 역을 따라가 보는 것이 "순회"다.
>
> **그래프를 나누는 축(용어 정리).**
> - **방향(directed) vs 무방향(undirected):** 간선에 화살표가 있나? 팔로우 관계(A→B)는 방향 그래프, 친구 관계(A—B)는 무방향. **무방향 간선 `(u, v)`는 인접 리스트에 양쪽으로 두 번 넣는다**(`adj[u].append(v)` 와 `adj[v].append(u)`). 이걸 한 번만 넣는 실수가 그래프 버그 1순위.
> - **가중치(weighted) vs 무가중치(unweighted):** 간선에 비용/거리가 붙나? 오늘은 무가중치 중심(가중치·최단 경로는 Phase 4에서).
> - **사이클(cycle):** 출발 정점으로 되돌아오는 경로가 있나? 그래프엔 흔히 있고, 이것이 트리와의 결정적 차이이자 **visited가 반드시 필요한 이유**다.
>
> **정점의 차수(degree).** 한 정점에 붙은 간선 수. 방향 그래프에서는 **진입 차수(in-degree, 들어오는 화살표 수)** 와 **진출 차수(out-degree, 나가는 화살표 수)** 를 구분한다. "마을의 재판관 찾기"(진입 N-1, 진출 0) 같은 문제가 차수만으로 풀린다.

> [!gear]- 2. 동작 원리 (How It Works)
> 그래프 문제는 **(1) 입력을 표현으로 바꾸기 → (2) 그 위를 순회하기** 두 단계다. 각 단계의 표준 코드를 정리한다.
>
> **(A) 간선 목록(edge list)을 인접 리스트로 — 코테의 90%.**
> ```
> from collections import defaultdict
> def build_adj(n, edges, directed=False):
>     adj = defaultdict(list)              # 또는 [[] for _ in range(n)]
>     for u, v in edges:
>         adj[u].append(v)
>         if not directed:                 # 무방향이면 양방향으로!
>             adj[v].append(u)
>     return adj
> ```
> `defaultdict(list)`를 쓰면 "없는 키" 걱정 없이 바로 `append`할 수 있다. 정점이 `0..n-1`로 조밀하면 `[[] for _ in range(n)]` 리스트가 더 빠르다.
>
> **(B) 인접 리스트 vs 인접 행렬 — 그림으로.**
> ```
>  그래프:  0 --- 1
>           |     |
>           2 --- 3
>
>  인접 리스트(adjacency list)       인접 행렬(adjacency matrix)
>    0: [1, 2]                          0 1 2 3
>    1: [0, 3]                        0 [0 1 1 0]
>    2: [0, 3]                        1 [1 0 0 1]
>    3: [1, 2]                        2 [1 0 0 1]
>                                     3 [0 1 1 0]
>  공간 O(V+E), 이웃 순회 빠름       공간 O(V^2), "u-v 연결?" O(1)
> ```
>
> **(C) DFS 순회 — 재귀(스택). visited로 사이클 차단.**
> ```
> def dfs(u, adj, visited):
>     visited[u] = True
>     for nxt in adj[u]:
>         if not visited[nxt]:             # 이 한 줄이 무한 루프를 막는다
>             dfs(nxt, adj, visited)
> ```
>
> **(D) BFS 순회 — 큐(deque). 방문 처리는 "큐에 넣는 순간".**
> ```
> from collections import deque
> def bfs(start, adj, n):
>     visited = [False] * n
>     q = deque([start]); visited[start] = True
>     while q:
>         u = q.popleft()
>         for nxt in adj[u]:
>             if not visited[nxt]:
>                 visited[nxt] = True      # 꺼낼 때가 아니라 "넣을 때" 표시(중복 삽입 방지)
>                 q.append(nxt)
> ```
>
> **(E) 연결 요소(connected components) 세기 — 대표 응용.** 모든 정점을 훑으며, 아직 방문 안 한 정점을 만나면 카운트를 +1하고 그 정점에서 도달 가능한 전부를 순회로 표시한다.
> ```
> def count_components(n, adj):
>     visited = [False] * n
>     count = 0
>     for s in range(n):
>         if not visited[s]:
>             count += 1                   # 새 무리 발견
>             dfs(s, adj, visited)         # 이 무리 전체를 방문 처리
>     return count
> ```
> "프로그래머스 네트워크"가 정확히 이 골격이다. 컴퓨터=정점, 연결=간선, 네트워크 수=연결 요소 수.
>
> **(F) 격자 = 암시적 그래프(implicit graph).** 격자 문제(섬의 개수 등)는 인접 리스트를 명시적으로 만들지 않는다. 대신 각 칸 `(r, c)`가 정점, **상하좌우 네 방향**이 간선이다. `dr, dc = (-1,1,0,0), (0,0,-1,1)`로 이웃을 즉석에서 계산한다.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> 그래프 순회의 시간은 **정점과 간선을 각각 상수 번 훑는 O(V + E)** 가 기준이다(V=정점 수, E=간선 수). 단, 이 값은 **표현 방식에 따라 달라진다** — 인접 행렬로 이웃을 찾으면 정점마다 V칸을 훑어야 해서 O(V^2)가 된다.
>
> | 연산 | 인접 리스트 | 인접 행렬 | 설명 |
> |---|---|---|---|
> | 공간 | O(V + E) | O(V^2) | 리스트는 실제 간선만, 행렬은 모든 쌍 |
> | 간선 (u,v) 존재? | O(deg(u)) | O(1) | 행렬은 `m[u][v]` 한 번에 |
> | u의 모든 이웃 순회 | O(deg(u)) | O(V) | 행렬은 없는 이웃도 다 훑음 |
> | 전체 DFS/BFS 순회 | O(V + E) | O(V^2) | 코테 대부분은 리스트가 유리 |
>
> > **왜 순회가 O(V + E)인가.** DFS/BFS는 각 정점을 딱 한 번 방문하고(visited 덕분), 각 정점에서 자기 간선들을 한 번씩 따라간다. 모든 정점의 차수 합 = 2E(무방향)이므로, 정점 방문 O(V) + 간선 순회 O(E) = **O(V + E)**. 이것이 "그래프를 한 번 훑는" 최적 비용이다.
> >
> > **언제 인접 행렬을 쓰나.** ① 정점 수 V가 작을 때(대략 V <= 500~1000, V^2가 감당되면), ② 간선이 매우 촘촘(dense)해서 E ~ V^2일 때, ③ "u와 v가 직접 연결됐나?"를 O(1)로 자주 물어야 할 때. 프로그래머스 "네트워크"는 입력이 이미 인접 행렬 형태(`computers[i][j]`)로 주어진다. **반대로 정점이 많고 간선이 성긴(sparse) 대부분의 경우는 인접 리스트가 정답.**
> >
> > **공간복잡도.** 표현 자체가 인접 리스트 O(V+E) / 인접 행렬 O(V^2). 여기에 순회용 `visited` O(V), DFS 재귀 스택 O(V)(최악, 일자형 그래프), BFS 큐 O(V)가 더해진다. 정점이 수십만이면 DFS 재귀는 `RecursionError` 위험이 있어 BFS(반복)나 명시적 스택을 고려([[day-25-dfs/concept|Day 25]] 참고).

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"연결 / 무리 / 그룹 / 도달 가능 / 네트워크"는 그래프 신호다.** "몇 개의 그룹으로 나뉘나"(연결 요소), "A에서 B로 갈 수 있나"(연결성), "모두 방문할 수 있나"(도달성)가 보이면 인접 리스트 구축 + DFS/BFS를 떠올려라.
>   - 참고: [프로그래머스 DFS/BFS 문제집](https://school.programmers.co.kr/learn/courses/30/parts/12421)
> - **무방향 간선은 반드시 양쪽에 넣어라.** `adj[u].append(v)` 만 하고 `adj[v].append(u)` 를 빠뜨리면 절반의 연결이 사라져 답이 통째로 틀린다. 그래프 문제 오답 1순위. "친구의 친구"는 서로 친구다.
> - **`visited`는 트리엔 없어도 되지만 그래프엔 필수다.** 트리는 사이클이 없어 부모만 피하면 되지만, 일반 그래프는 사이클이 있어 방문 체크를 빼면 무한 루프에 빠진다. 순회 코드를 쓸 때 가장 먼저 `visited`부터 준비하라.
> - **BFS는 "큐에 넣을 때" 방문 표시하라.** "꺼낼 때" 표시하면 같은 정점이 큐에 여러 번 들어가 시간·메모리가 폭발하거나 최단 거리가 틀린다. 넣는 즉시 `visited=True`가 정석([[day-26-bfs/concept|Day 26]]).
> - **`defaultdict(list)`로 인접 리스트를 간결하게.** 없는 키를 자동으로 빈 리스트로 만들어 주어 `if key not in adj` 분기가 사라진다. 정점 라벨이 문자열(공항 코드 등)이거나 조밀하지 않을 때 특히 편하다.
> - **격자 문제는 그래프를 "그리지 말고" 방향 배열로.** `dr, dc = (-1,1,0,0),(0,0,-1,1)`을 zip으로 돌면 상하좌우 이웃이 나온다. 경계 검사 `0 <= nr < R and 0 <= nc < C`를 잊지 마라.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **트리 ⊂ DAG ⊂ 일반 그래프.** 트리는 "사이클 없고 연결된 무방향 그래프"(정점 V개, 간선 V-1개), DAG(directed acyclic graph)는 "사이클 없는 방향 그래프". 오늘의 순회 코드는 이 셋 모두에 그대로 쓰인다. 관계를 이해하면 [[day-11-tree-basics/concept|Day 11 트리]]와 [[day-29-tree-traversal/concept|Day 29]]가 그래프의 특수 사례로 꿰어진다.
> 2. **무방향 간선 = 인접 리스트에 두 번.** (팁에서도 강조) 이걸 놓치면 연결 요소 개수·경로 판정이 전부 틀린다. 방향 그래프면 한 번만, 무방향이면 반드시 양방향.
> 3. **`visited` 없는 순회 = 무한 루프.** 사이클이 있는 그래프에서 방문 체크를 빼면 `A->B->A->B...`를 영원히 돈다. `RecursionError`(DFS) 또는 메모리 초과(BFS)로 터진다. 순회의 대전제다.
> 4. **인접 리스트 vs 행렬을 제약으로 골라라.** V가 크고(수만~) 간선이 성기면 리스트(공간 O(V+E)). V가 작고(수백) 조밀하거나 "직접 연결?"을 자주 물으면 행렬(O(V^2)). 잘못 고르면 메모리 초과(행렬로 V=10만) 또는 시간 초과(리스트에서 반복 연결 확인).
> 5. **정점 라벨을 인덱스로 정규화하라.** 정점이 `1..n`으로 오면 크기 `n+1` 배열을 쓰거나 -1 해서 0-기반으로 맞춘다. 문자열/임의 ID면 `dict`로 정수 인덱스에 매핑. 오프바이원(off-by-one)으로 배열 범위를 벗어나는 실수가 잦다.
> 6. **연결 요소 세기는 "모든 정점에서 시도"해야 한다.** 한 정점에서만 순회하면 그 정점이 속한 무리만 방문한다. `for s in range(n): if not visited[s]:` 로 **끊긴 무리들까지 빠짐없이** 새 순회를 시작해야 전체 개수가 나온다.
> 7. **방향 그래프의 도달성 != 무방향의 연결성.** 방향 그래프에서 "A에서 B로 가는 길"이 있어도 "B에서 A"는 없을 수 있다. 무방향에서 연결 요소를 세듯 방향 그래프를 다루면 오답. 문제가 방향인지 무방향인지 먼저 확정하라.
> 8. **차수(degree)만으로 풀리는 문제가 있다.** 모든 정점을 순회하지 않고 **진입/진출 차수 카운트**만으로 답이 나오는 유형(마을의 재판관: in=N-1, out=0 / 스타 그래프 중심: 모든 간선에 등장). 순회 전에 "차수로 충분한가"를 먼저 의심하라.
> 9. **DFS 재귀 깊이 한계.** 정점이 수만 개인 일자형(선형) 그래프를 DFS로 재귀 순회하면 파이썬 기본 한도 1000을 넘겨 `RecursionError`. `sys.setrecursionlimit()`을 올리거나, 애초에 BFS/명시적 스택으로 순회하라.
>   - 참고: [collections.deque (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.deque)

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import defaultdict, deque
>
> # 1) 간선 목록 -> 인접 리스트 (무방향이면 양방향)
> def build_adj(n, edges, directed=False):
>     adj = [[] for _ in range(n)]
>     for u, v in edges:
>         adj[u].append(v)
>         if not directed:
>             adj[v].append(u)
>     return adj
>
> # 2) DFS 순회 (재귀) - visited로 사이클 차단
> def dfs(u, adj, visited, order):
>     visited[u] = True
>     order.append(u)
>     for nxt in adj[u]:
>         if not visited[nxt]:
>             dfs(nxt, adj, visited, order)
>
> # 3) BFS 순회 (큐) - 넣을 때 방문 표시
> def bfs(start, adj, n):
>     visited = [False] * n
>     q = deque([start]); visited[start] = True
>     order = []
>     while q:
>         u = q.popleft()
>         order.append(u)
>         for nxt in adj[u]:
>             if not visited[nxt]:
>                 visited[nxt] = True
>                 q.append(nxt)
>     return order
>
> # 4) 연결 요소(connected components) 개수 - 반복 DFS
> def count_components(n, adj):
>     visited = [False] * n
>     count = 0
>     for s in range(n):
>         if not visited[s]:
>             count += 1
>             stack = [s]; visited[s] = True
>             while stack:
>                 u = stack.pop()
>                 for nxt in adj[u]:
>                     if not visited[nxt]:
>                         visited[nxt] = True
>                         stack.append(nxt)
>     return count
>
> # 5) 격자 = 암시적 그래프 (섬의 개수)
> def num_islands(grid):
>     if not grid:
>         return 0
>     R, C = len(grid), len(grid[0])
>     seen = [[False] * C for _ in range(R)]
>     dr, dc = (-1, 1, 0, 0), (0, 0, -1, 1)
>     cnt = 0
>     for i in range(R):
>         for j in range(C):
>             if grid[i][j] == "1" and not seen[i][j]:
>                 cnt += 1
>                 q = deque([(i, j)]); seen[i][j] = True
>                 while q:
>                     r, c = q.popleft()
>                     for d in range(4):
>                         nr, nc = r + dr[d], c + dc[d]
>                         if (0 <= nr < R and 0 <= nc < C
>                                 and not seen[nr][nc] and grid[nr][nc] == "1"):
>                             seen[nr][nc] = True
>                             q.append((nr, nc))
>     return cnt
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 그래프 표현(인접 리스트/행렬)과 순회(DFS/BFS)를 익히는 대표 문제를 기초→중급→심화로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | 번호 | 문제 | 출처 | 난이도 | 형태 |
> |---|---|---|---|---|
> | 1 | Find Center of Star Graph | [LeetCode #1791](https://leetcode.com/problems/find-center-of-star-graph/) | 🟢기초 | 표현·차수 이해 |
> | 2 | Find if Path Exists in Graph | [LeetCode #1971](https://leetcode.com/problems/find-if-path-exists-in-graph/) | 🟢기초 | 인접리스트 + 연결성 |
> | 3 | Find the Town Judge | [LeetCode #997](https://leetcode.com/problems/find-the-town-judge/) | 🟢기초 | 진입/진출 차수 |
> | 4 | Number of Provinces | [LeetCode #547](https://leetcode.com/problems/number-of-provinces/) | 🟡중급 | 인접행렬 + 연결요소 |
> | 5 | Number of Islands | [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | 🟡중급 | 격자 암시적 그래프 |
> | 6 | Keys and Rooms | [LeetCode #841](https://leetcode.com/problems/keys-and-rooms/) | 🟡중급 | 도달 가능성 DFS |
> | 7 | Clone Graph | [LeetCode #133](https://leetcode.com/problems/clone-graph/) | 🟡중급 | 인접리스트 복제 |
> | 8 | All Paths From Source to Target | [LeetCode #797](https://leetcode.com/problems/all-paths-from-source-to-target/) | 🟡중급 | DAG 모든 경로 |
> | 9 | 네트워크 | [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162) | 🟡중급 | 연결 요소 개수 |
> | 10 | 여행경로 | [프로그래머스 #43164](https://school.programmers.co.kr/learn/courses/30/lessons/43164) | 🔴심화 | 인접리스트 DFS 사전순 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근(DFS vs BFS, 인접 리스트 vs 행렬, 차수 카운트 vs 순회) 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-27-backtracking/concept|Day 27 — 백트래킹 (Backtracking)]] — 상태 공간을 트리로 보고 가지치기 DFS를 돌렸다면, 오늘은 그 무대인 그래프 자체를 표현하고 순회한다
- ➡️ **다음(next):** [[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]] — 트리는 사이클 없는 특수 그래프. 오늘의 순회를 전위/중위/후위 순회로 특화한다
- 🧭 **관련(related):**
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 그래프 순회의 두 엔진 중 하나. 오늘은 그 DFS가 뛰노는 무대(인접 리스트/행렬)를 정식으로 세운다
  - [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — 다른 순회 엔진. 큐 기반 순회를 그래프 표현 위에 얹어 최단 거리·연결성으로 확장
  - [[day-27-backtracking/concept|Day 27 — 백트래킹 (Backtracking)]] — 여행경로처럼 그래프 위에서 모든 경로를 DFS로 나열하는 문제에서 백트래킹과 만난다
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 트리는 간선 V-1개짜리 사이클 없는 그래프. 그래프 표현의 특수 사례로 다시 본다
  - [[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]] — 그래프 순회를 트리에 특화. 부모 회피로 visited를 대신할 수 있는 이유를 오늘 배운 사이클 개념으로 이해
  - [[day-30-review/concept|Day 30 — 개념 집중기 종합 복습]] — 완전탐색·DFS·BFS·백트래킹·그래프를 한자리에서 통합 정리
- 🗺️ **지도(MOC):** [[Phase-3 MOC]] · [[00 Algorithm MOC]]
