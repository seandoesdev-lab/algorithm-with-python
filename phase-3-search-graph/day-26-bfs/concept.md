---
day: 26
phase: 3-search-graph
title: BFS (너비 우선 탐색 / Breadth-First Search)
category: [탐색, 그래프, BFS, 최단거리]
difficulty: 중급
status: done
prev: "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
next: "[[day-27-backtracking/concept|Day 27 — 백트래킹]]"
related:
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-24-brute-force/concept|Day 24 — 완전 탐색]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
  - "[[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]]"
sources:
  - https://school.programmers.co.kr/learn/courses/30/parts/12421
  - https://school.programmers.co.kr/learn/courses/30/lessons/1844
  - https://school.programmers.co.kr/learn/courses/30/lessons/43163
  - https://leetcode.com/problems/binary-tree-level-order-traversal/
  - https://leetcode.com/problems/rotting-oranges/
  - https://leetcode.com/problems/01-matrix/
  - https://leetcode.com/problems/shortest-path-in-binary-matrix/
  - https://leetcode.com/problems/word-ladder/
  - https://leetcode.com/problems/open-the-lock/
  - https://docs.python.org/3/library/collections.html#collections.deque
tags: [phase/3, topic/bfs, topic/search, topic/graph, topic/shortest-path]
---

# Day 26 — BFS (너비 우선 탐색 / Breadth-First Search)

> [!abstract] 한눈 요약 (TL;DR)
> **BFS(너비 우선 탐색, Breadth-First Search)** 는 그래프·트리를 탐색할 때 **"출발점에서 가까운 정점부터, 물결이 퍼지듯 같은 거리끼리 한 겹씩(level by level) 방문"** 하는 방법이다. 어제 배운 [[day-25-dfs/concept|DFS(Day 25)]]와 **자료구조만 스택→큐(queue)로 바꾼 쌍둥이**이며, 이 한 가지 차이가 결정적 능력을 만든다 — **가중치 없는(unweighted) 그래프에서 최단 거리(shortest path)·최소 이동 횟수를 정확히 보장**한다. 핵심 엔진은 [[day-08-queue-deque/concept|큐/덱(Day 08)]]의 `collections.deque`이고, DFS와 마찬가지로 한 번 넣은 정점을 다시 넣지 않는 **visited(방문 체크)** 가 정확성과 효율의 생명줄이다. 코테에서 BFS는 ① **격자(grid) 최단 거리**(게임 맵 최단거리, 미로 탈출), ② **여러 출발점에서 동시에 퍼지는 다중 소스 BFS**(썩은 토마토, 벽까지 거리), ③ **트리의 레벨 순회(level order)**, ④ **상태 공간에서 최소 변환 횟수**(단어 변환, 자물쇠 열기) 등에 압도적으로 자주 나온다. 시간복잡도는 DFS와 동일하게 인접 리스트 기준 **O(V + E)**. "최단"이라는 단어가 보이면 BFS를 먼저 떠올려라.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **BFS는 "너비(breadth)를 우선"하는 탐색이다.** 현재 정점의 **모든 이웃을 먼저 다 방문**한 뒤, 그 이웃들의 이웃(2칸 거리)을 방문하고, 다시 그다음 겹(3칸 거리)으로 넘어간다. 즉 **거리가 같은 정점들을 한 겹씩 완전히 처리**하고 다음 겹으로 나아간다.
>
> **일상 비유 — 잔잔한 호수에 던진 돌.** 돌이 떨어진 지점(출발점)에서 동심원(물결)이 사방으로 동시에, 같은 속도로 퍼진다. 1초 뒤 물결이 닿은 곳은 모두 "1칸 거리", 2초 뒤 닿은 곳은 "2칸 거리"다. 목표 지점에 물결이 **처음 닿는 순간의 반지름이 곧 최단 거리**다. 이 "동시에·같은 속도로 퍼진다"는 성질이 BFS가 최단 거리를 보장하는 이유의 전부다. 반대로 [[day-25-dfs/concept|DFS(Day 25)]]는 "한 방향으로 끝까지 파고든 뒤 되돌아오기"라 먼저 찾은 경로가 최단이라는 보장이 전혀 없다.
>
> **왜 큐(FIFO)인가.** "가까운 것부터 먼저" 처리하려면, 먼저 발견한(=더 가까운) 정점을 먼저 꺼내야 한다. 이것이 정확히 **큐(Queue)의 FIFO**(First-In-First-Out, 선입선출) 규칙이다. DFS가 "가장 최근에 넣은 것을 먼저"(스택/LIFO) 꺼내 깊이 우선이 되는 것과 정확히 대칭이다. **DFS의 스택을 큐로 바꾸면 그대로 BFS가 된다.**
>
> **핵심 3요소.** ① **큐**(`deque`, 방문 예정 정점을 거리 순으로 보관), ② **visited**(무한 루프·중복 방문 차단, BFS에서는 **큐에 넣는 순간** 표시), ③ **거리/레벨 관리**(`dist` 배열 또는 큐를 겹 단위로 끊어 세는 방식). 이 셋이 BFS 코드의 뼈대다.

> [!gear]- 2. 동작 원리 (How It Works)
> BFS는 **큐**에 출발점을 넣고 시작해, 큐가 빌 때까지 "꺼내서 이웃을 큐에 넣기"를 반복한다.
>
> **(A) 기본 BFS 골격 — 도달 여부·방문 순서.**
> ```
> from collections import deque
> def bfs(graph, start):
>     visited = {start}            # 큐에 넣는 순간 방문 표시
>     q = deque([start])
>     while q:
>         u = q.popleft()          # FIFO: 가장 먼저 넣은 것을 꺼냄
>         for v in graph[u]:
>             if v not in visited:
>                 visited.add(v)   # enqueue 시점에 표시(중복 삽입 방지)
>                 q.append(v)
> ```
> `popleft()`이 **가장 먼저 넣은 정점**을 꺼내므로(FIFO) 자연히 가까운 것부터 처리된다. `deque`의 `append`(오른쪽 넣기) + `popleft`(왼쪽 꺼내기) 조합이 O(1) 큐다.
>
> **(B) 최단 거리 BFS — dist 배열로 거리 기록.** 이웃을 큐에 넣을 때 "부모 거리 + 1"을 기록한다.
> ```
> def bfs_dist(graph, start):
>     dist = {start: 0}
>     q = deque([start])
>     while q:
>         u = q.popleft()
>         for v in graph[u]:
>             if v not in dist:            # 처음 도달 = 최단
>                 dist[v] = dist[u] + 1
>                 q.append(v)
>     return dist
> ```
> **처음 도달했을 때의 거리가 곧 최단 거리**다(뒤에 더 긴 경로로 다시 와도 이미 방문 처리되어 무시). 이것이 BFS 최단 거리의 정당성이다.
>
> **추적 예시 — 아래 그래프에서 1부터 BFS.**
> ```
>       1
>      / \
>     2   3
>    / \   \
>   4   5   6
>
> 방문 순서: 1 -> 2 -> 3 -> 4 -> 5 -> 6   (겹: [1] [2,3] [4,5,6])
> 거리:      0    1    1    2    2    2
> 큐 변화:   [1] -> [2,3] -> [3,4,5] -> [4,5,6] -> [5,6] -> [6] -> []
> ```
> DFS는 `1 2 4 5 3 6`(깊이 우선)이었지만, BFS는 `1 2 3 4 5 6`(거리 순)이다.
>
> **(C) 격자(grid) BFS — 코테 최다 최단거리 유형.** 각 칸 `(r, c)`가 정점, 상하좌우 인접 칸이 이웃. 목표 칸에 처음 닿는 순간의 거리가 최단 이동 횟수다.
> ```
> dr = [-1, 1, 0, 0]; dc = [0, 0, -1, 1]
> q = deque([(sr, sc)]); dist[sr][sc] = 1     # 문제 정의에 맞춰 시작값 설정
> while q:
>     r, c = q.popleft()
>     for d in range(4):
>         nr, nc = r + dr[d], c + dc[d]
>         if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == 0 and grid[nr][nc] == 1:
>             dist[nr][nc] = dist[r][c] + 1
>             q.append((nr, nc))
> ```
>
> **(D) 레벨 순회 BFS — "한 겹씩" 명시적으로 끊기.** 큐에 든 현재 겹의 크기를 미리 재서 그만큼만 꺼내면 레벨이 분리된다. 트리 레벨 순회·"몇 번째 단계인가"에 쓴다.
> ```
> while q:
>     size = len(q)                 # 지금 큐 = 현재 레벨 전체
>     for _ in range(size):
>         u = q.popleft()
>         ... 이웃을 다음 레벨로 append ...
>     level += 1
> ```
>
> **(E) 다중 소스 BFS(multi-source).** 출발점을 여러 개 **동시에** 큐에 넣고 시작하면, 모든 출발점에서 물결이 함께 퍼진다. "썩은 토마토가 동시에 번짐", "가장 가까운 벽까지 거리"가 대표. 소스가 여러 개라도 전체 O(V + E) 한 번에 끝난다.

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> BFS는 DFS와 완전히 같은 비용이다 — **모든 정점 1번, 모든 간선 1번**씩 본다(visited 덕분). 탐색 순서만 다를 뿐 방문하는 대상은 동일하기 때문이다.
>
> | 대상 / 표현 | 시간복잡도 | 공간복잡도 | 설명 |
> |---|---|---|---|
> | 인접 리스트(adjacency list) | O(V + E) | O(V) | 정점 V개 + 간선 E개를 각 1회. 가장 효율적 |
> | 인접 행렬(adjacency matrix) | O(V^2) | O(V) | 이웃 찾을 때 한 행(V칸)을 전부 훑음 |
> | 격자 R x C | O(R x C) | O(R x C) | 칸 수만큼. 각 칸 상하좌우 상수 개 이웃 |
>
> > **왜 O(V + E)인가.** 각 정점은 큐에 딱 한 번 들어갔다 나온다(visited가 재삽입 차단). 정점을 꺼낼 때 그 이웃을 훑는데, 모든 정점의 이웃 수 합은 간선 수의 2배(무방향)이므로 간선 훑기 총합 O(E). 따라서 O(V) + O(E) = **O(V + E)**. DFS와 동일한 논리.
> >
> > **공간복잡도는 DFS보다 불리할 수 있다.** BFS의 큐에는 **한 레벨의 정점이 통째로** 들어간다. 넓게 퍼지는 그래프(예: 완전 이진 트리의 마지막 레벨)에서는 큐 크기가 O(V/2)까지 커질 수 있어, "폭이 넓고 얕은" 그래프에서는 DFS(스택 깊이 O(높이))보다 메모리를 더 쓴다. 반대로 "좁고 깊은" 그래프에서는 BFS가 메모리 유리.
> >
> > **BFS는 재귀 깊이 문제가 없다.** DFS 재귀는 정점이 많으면 `RecursionError` 위험이 있지만, BFS는 명시적 큐를 쓰는 반복문이라 그런 한계가 없다. 정점이 수십만 개인 격자 최단거리에서 BFS가 안전한 이유 중 하나다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"최단·최소 몇 번·며칠·몇 단계"가 보이면 BFS다.** "최소 이동 횟수", "가장 짧은 경로", "모두 익는 데 며칠", "최소 변환 횟수" 같은 표현은 가중치 없는 최단 거리 신호 → BFS. 반대로 "존재 여부·전부 방문·모든 경로·영역 넓이"는 [[day-25-dfs/concept|DFS(Day 25)]]가 편하다.
>   - 참고: [프로그래머스 DFS/BFS 문제집](https://school.programmers.co.kr/learn/courses/30/parts/12421)
> - **visited는 반드시 "큐에 넣는 순간(enqueue)" 표시.** 꺼낼 때(dequeue) 표시하면 같은 정점이 큐에 여러 번 들어가 시간초과(TLE)·중복 처리가 난다. DFS 스택과 동일한 원칙이지만 BFS에서 실수하면 성능이 눈에 띄게 무너진다.
> - **격자에서 dist 배열이 visited를 겸한다.** `dist[nr][nc]`가 아직 초기값(미방문)일 때만 진입하면, 거리 기록과 방문 체크를 한 번에 처리한다. 단 시작 칸의 거리를 문제 정의(0부터인지 1부터인지)에 맞춰 초기화해야 한다.
> - **다중 소스 BFS는 "출발점을 처음에 다 넣기".** 여러 근원에서 최단 거리를 구할 때 소스마다 따로 BFS를 돌리지 말고, 모든 소스를 거리 0으로 큐에 넣고 한 번에 퍼뜨려라. O(V+E) 한 번으로 끝난다([Rotting Oranges](https://leetcode.com/problems/rotting-oranges/), [01 Matrix](https://leetcode.com/problems/01-matrix/)의 정석).
> - **가중치가 있으면 BFS는 틀린다.** 간선 비용이 다르면 "칸 수 = 거리"가 깨진다 → 다익스트라(Dijkstra, Phase 4). 예외적으로 가중치가 0/1뿐이면 0-1 BFS(덱 양쪽 삽입)로 처리한다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **BFS의 최단 거리 보장은 "가중치 없는 그래프"에서만 성립.** 모든 간선의 비용이 같을 때(=1)만 "먼저 도달 = 최단"이 참이다. 간선마다 비용이 다르면 BFS는 최단 비용을 못 준다 → 다익스트라/벨만-포드(Phase 4). "BFS로 가중치 최단거리" 시도는 대표적 오답.
> 2. **visited는 enqueue 시점에.** (팁에서도 강조) dequeue 시점 표시는 큐 폭발 + 시간초과의 주범. BFS 버그 1순위.
> 3. **큐는 반드시 `collections.deque`.** 파이썬 `list`로 `list.pop(0)`을 하면 앞 원소를 꺼낼 때마다 나머지를 한 칸씩 당기느라 O(n)이 되어, 전체가 O(V^2)로 느려진다(TLE). `deque.popleft()`는 O(1). 이 차이가 통과/시간초과를 가른다.
>   - 참고: [collections.deque (Python 공식 문서)](https://docs.python.org/3/library/collections.html#collections.deque)
> 4. **격자 경계 검사(boundary check)를 이웃 접근 전에.** `0 <= nr < R and 0 <= nc < C`를 반드시 먼저 확인. 파이썬은 `grid[-1]`이 조용히 뒤에서 접근되어 틀린 답을 내니(에러도 안 남) 더 위험하다.
> 5. **레벨(단계) 카운트는 큐를 겹 단위로 끊어라.** "몇 단계 만에 도달"을 셀 때 `size = len(q)`로 현재 레벨 크기를 미리 재고 그만큼만 꺼내는 패턴을 쓰거나, `dist` 배열로 각 정점의 거리를 직접 기록한다. 이 둘을 섞으면 오프바이원(off-by-one) 버그가 난다.
> 6. **도달 불가(unreachable) 처리.** 목표에 끝내 도달 못 하면(큐가 비어도 목표 미방문) 문제 규약대로 -1 등을 반환해야 한다. 게임 맵 최단거리에서 벽에 막혀 못 가면 -1이 정답인 것처럼, "못 감"을 반드시 별도 처리하라.
> 7. **다중 소스 BFS는 소스 여러 개를 동시에 넣는 것.** 각 소스에서 개별 BFS를 V번 돌리면 O(V(V+E))로 폭발한다. 모두 거리 0으로 함께 넣으면 O(V+E) 한 번. 성능 차이가 크다.
> 8. **BFS vs DFS는 "무엇을 묻느냐"로 고른다.** 최단/최소 → BFS. 존재/전부/경로 나열/사이클 → DFS. 단순 연결 요소 세기·도달 여부는 둘 다 되므로 편한 쪽. **자료구조(큐/스택)만 다를 뿐 O(V+E)로 비용은 같다**는 점을 기억하면 선택이 쉬워진다.
> 9. **트리의 레벨 순회 = BFS.** 이진 트리를 "위에서 아래로, 왼→오른쪽" 층별로 출력하는 것이 곧 BFS다([[day-11-tree-basics/concept|Day 11 트리]] · [[day-29-tree-traversal/concept|Day 29 트리 순회]]로 이어짐). DFS의 전위/중위/후위 순회와 대비해 익혀라.

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import deque
>
> # 1) 기본 BFS - 방문 순서 (인접 리스트)
> def bfs_order(graph, start):
>     visited, order = {start}, []
>     q = deque([start])
>     while q:
>         u = q.popleft()             # FIFO
>         order.append(u)
>         for v in graph[u]:
>             if v not in visited:
>                 visited.add(v)      # enqueue 시점에 방문 표시
>                 q.append(v)
>     return order
>
> # 2) 최단 거리 BFS - 각 정점까지 최소 간선 수
> def bfs_dist(graph, start):
>     dist = {start: 0}
>     q = deque([start])
>     while q:
>         u = q.popleft()
>         for v in graph[u]:
>             if v not in dist:       # 처음 도달 = 최단
>                 dist[v] = dist[u] + 1
>                 q.append(v)
>     return dist
>
> # 3) 격자 BFS - 시작(0,0)에서 각 칸까지 최소 이동 횟수
> def grid_shortest(grid):
>     R, C = len(grid), len(grid[0])
>     dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
>     dist = [[-1] * C for _ in range(R)]
>     dist[0][0] = 0
>     q = deque([(0, 0)])
>     while q:
>         r, c = q.popleft()
>         for d in range(4):
>             nr, nc = r + dr[d], c + dc[d]
>             if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1 and grid[nr][nc] == 1:
>                 dist[nr][nc] = dist[r][c] + 1
>                 q.append((nr, nc))
>     return dist
>
> # 4) 다중 소스 BFS - 여러 시작점에서 동시에 퍼지는 최단 거리
> def multi_source_dist(grid, sources):
>     R, C = len(grid), len(grid[0])
>     dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
>     dist = [[-1] * C for _ in range(R)]
>     q = deque()
>     for (sr, sc) in sources:        # 모든 소스를 거리 0으로 함께 넣기
>         dist[sr][sc] = 0
>         q.append((sr, sc))
>     while q:
>         r, c = q.popleft()
>         for d in range(4):
>             nr, nc = r + dr[d], c + dc[d]
>             if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
>                 dist[nr][nc] = dist[r][c] + 1
>                 q.append((nr, nc))
>     return dist
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 격자 최단 거리, 다중 소스 BFS, 트리 레벨 순회, 상태 공간 최소 변환을 골고루 담았다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | 번호 | 문제 | 출처 | 난이도 | 형태 |
> |---|---|---|---|---|
> | 1 | Binary Tree Level Order Traversal | [LeetCode #102](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 🟢기초 | 트리 레벨 순회 BFS |
> | 2 | 게임 맵 최단거리 | [프로그래머스 #1844](https://school.programmers.co.kr/learn/courses/30/lessons/1844) | 🟡중급 | 격자 최단 거리 BFS |
> | 3 | Shortest Path in Binary Matrix | [LeetCode #1091](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | 🟡중급 | 8방향 격자 최단 거리 |
> | 4 | Rotting Oranges | [LeetCode #994](https://leetcode.com/problems/rotting-oranges/) | 🟡중급 | 다중 소스 BFS(시간) |
> | 5 | 01 Matrix | [LeetCode #542](https://leetcode.com/problems/01-matrix/) | 🟡중급 | 다중 소스 BFS(거리) |
> | 6 | 단어 변환 | [프로그래머스 #43163](https://school.programmers.co.kr/learn/courses/30/lessons/43163) | 🟡중급 | 상태 공간 BFS(변환) |
> | 7 | Open the Lock | [LeetCode #752](https://leetcode.com/problems/open-the-lock/) | 🟡중급 | 상태 공간 BFS(자물쇠) |
> | 8 | Word Ladder | [LeetCode #127](https://leetcode.com/problems/word-ladder/) | 🔴심화 | 상태 공간 BFS(최소 변환) |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 다중 접근(dist 배열 vs 레벨 끊기, 단일 소스 vs 다중 소스) 비교 및 코드: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 탐색 순서를 결정하는 자료구조만 스택→큐로 바꾼 쌍둥이. BFS는 최단 거리를 보장한다는 점이 결정적 차이
- ➡️ **다음(next):** [[day-27-backtracking/concept|Day 27 — 백트래킹]] — DFS에 가지치기를 더한 최적화. DFS/BFS 골격을 익힌 뒤 상태 공간 탐색을 정교하게 다룬다
- 🧭 **관련(related):**
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 큐↔스택 대칭. 언제 무엇을 쓸지 짝지어 기억한다
  - [[day-24-brute-force/concept|Day 24 — 완전 탐색]] — BFS는 상태 공간을 "가까운 것부터" 훑는 완전 탐색의 한 형태다
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — BFS의 엔진이 큐(FIFO). `deque.popleft()`의 O(1)이 성능의 핵심
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본]] — 트리의 레벨 순회가 곧 BFS. 사이클 없는 그래프라 visited가 단순해진다
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 인접 리스트/행렬 위에 BFS/DFS를 얹어 그래프 순회를 정리한다
  - [[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]] — 레벨 순회(BFS)와 전위·중위·후위(DFS)를 한자리에서 대비한다
- 🗺️ **지도(MOC):** [[Phase-3 MOC]] · [[00 Algorithm MOC]]
