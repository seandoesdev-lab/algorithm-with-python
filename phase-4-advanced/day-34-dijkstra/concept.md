---
day: 34
phase: 4-advanced
title: 최단 경로 - 다익스트라 (Dijkstra's Shortest Path)
category: [그래프, 최단 경로, 다익스트라, 우선순위 큐, 그리디]
difficulty: 중급
status: done
prev: "[[day-33-dp-lis-lcs/concept|Day 33 — 부분 수열 DP (LIS·LCS)]]"
next: "[[day-35-bellman-floyd/concept|Day 35 — 벨만-포드·플로이드-워셜]]"
related:
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
  - "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-21-greedy/concept|Day 21 — 그리디 (Greedy)]]"
  - "[[day-31-dp/concept|Day 31 — 동적 계획법 입문]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-35-bellman-floyd/concept|Day 35 — 벨만-포드·플로이드-워셜]]"
sources:
  - https://leetcode.com/problems/network-delay-time/
  - https://leetcode.com/problems/cheapest-flights-within-k-stops/
  - https://leetcode.com/problems/path-with-minimum-effort/
  - https://leetcode.com/problems/swim-in-rising-water/
  - https://leetcode.com/problems/shortest-path-in-binary-matrix/
  - https://school.programmers.co.kr/learn/courses/30/lessons/12978
  - https://docs.python.org/3/library/heapq.html
tags: [phase/4, topic/graph, topic/shortest-path, topic/dijkstra, topic/priority-queue, topic/greedy]
---

# Day 34 — 최단 경로: 다익스트라 (Dijkstra's Shortest Path)

> [!abstract] 한눈 요약 (TL;DR)
> **다익스트라(Dijkstra)** 는 **가중치가 있는 그래프**에서 한 **출발점(single source)** 으로부터 나머지 모든 정점까지의 **최단 거리**를 구하는 대표 알고리즘이다. 핵심 아이디어는 [[day-21-greedy/concept|그리디(Day 21)]]다 — "**아직 확정 안 된 정점 중 현재 거리가 가장 짧은 것**을 매번 골라 확정하고, 그 정점을 거쳐 이웃들의 거리를 갱신(relaxation, 완화)한다". 이 "가장 짧은 것 먼저"를 빠르게 뽑기 위해 [[day-12-heap/concept|힙·우선순위 큐(Day 12)]]를 쓰며, 그 결과 시간복잡도는 **O((V+E) log V)** 다. [[day-26-bfs/concept|BFS(Day 26)]]가 **모든 간선의 가중치가 1일 때의 최단 경로**였다면, 다익스트라는 그것을 **가중치가 제각각인 그래프**로 확장한 것이다. 단 **결정적 전제 하나** — 다익스트라는 **음수 간선(negative edge)이 없을 때만** 정답을 보장한다. 음수 간선이 있으면 [[day-35-bellman-floyd/concept|벨만-포드(Day 35)]]로 넘어가야 한다. 최단 경로 문제는 "지도 위 최소 시간/비용", "격자에서 가장 힘 안 드는 길", "신호 전파 시간"처럼 코테·실무 어디에나 나오는 필수 골격이다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **문제 정의.** 정점(vertex/node) V개, 간선(edge)마다 **양의 가중치(weight)** 가 붙은 그래프에서, 출발점 `s`로부터 각 정점까지 **가중치 합이 최소인 경로**의 길이를 구한다. 예: 도시가 정점, 도로가 간선, 도로 주행 시간이 가중치라면 "출발 도시에서 각 도시까지 최소 주행 시간"이다.
>
> **물이 퍼지는 비유 (파동 확산).** 출발점에 물을 붓는다고 상상하자. 물은 사방으로 퍼지되 **간선의 가중치만큼 시간이 걸려** 흐른다. 어떤 정점에 **물이 처음 도달하는 순간의 시각** = 그 정점까지의 최단 거리다. BFS가 모든 간선을 "1초"로 보고 동심원처럼 퍼진다면, 다익스트라는 간선마다 흐르는 속도가 달라 **"가장 먼저 물이 닿을 정점"을 우선순위 큐로 골라가며** 퍼진다.
>
> **그리디가 통하는 이유 (핵심 통찰).** "지금까지 확정된 것들 밖에서 거리가 최소인 정점 `u`"를 골랐다고 하자. 모든 간선이 **양수**라면, 아직 확정 안 된 다른 정점을 **경유해서** `u`에 더 짧게 도달하는 길은 **존재할 수 없다**(경유하려면 이미 `u`의 현재 거리보다 먼 정점을 지나야 하고, 거기서 양수를 더 더하므로 반드시 더 커진다). 그래서 `u`의 현재 거리를 **최종 확정**해도 안전하다. 이 "한 번 뽑으면 확정" 성질이 다익스트라를 그리디로 만들며, **음수 간선이 있으면 이 논리가 깨진다**(더 먼 정점을 지나 음수로 되돌아와 더 짧아질 수 있으므로).
>
> **완화(Relaxation).** 다익스트라의 유일한 갱신 연산이다. 정점 `u`를 확정할 때, 각 이웃 `v`에 대해 `dist[u] + w(u,v) < dist[v]` 이면 `dist[v]`를 줄인다. "u를 거쳐 가는 게 더 짧으면 갱신"이라는 이 한 줄이 벨만-포드·SPFA까지 모든 최단 경로 알고리즘의 공통 심장이다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 우선순위 큐 기반 다익스트라 (실전 표준).**
> 배열 `dist[]`를 모두 무한대(INF)로, 출발점만 0으로 둔다. 최소 힙에 `(0, 출발점)`을 넣고 반복한다.
> ```
> 1. 힙에서 (d, u) = 현재 거리가 가장 작은 정점을 꺼낸다.
> 2. d > dist[u] 이면(이미 더 짧은 길로 확정됨) 버린다.   # "지연 삭제(lazy deletion)"
> 3. u의 각 이웃 v, 가중치 w에 대해:
>       if dist[u] + w < dist[v]:      # 완화(relaxation)
>           dist[v] = dist[u] + w
>           힙에 (dist[v], v) push
> 4. 힙이 빌 때까지 반복. 끝나면 dist[] = 최단 거리.
> ```
> ```
>     (A)--4-->(B)          시작 = A
>      |       / |          dist 초기화: A=0, B=C=D=INF
>      1     2   5
>      |   /     |          힙: [(0,A)]
>      v v       v
>     (C)--1--->(D)
>
>   pop (0,A) : B<-4, C<-1                    힙 [(1,C),(4,B)]
>   pop (1,C) : D<-1+1=2, B<-min(4,1+2)=3     힙 [(2,D),(3,B),(4,B*)]
>   pop (2,D) : 이웃 갱신 없음                 힙 [(3,B),(4,B*)]
>   pop (3,B) : D<-min(2,3+5)=2 (변화 없음)    힙 [(4,B*)]
>   pop (4,B*): 4 > dist[B]=3 -> 버림(지연 삭제)
>   결과 dist = {A:0, B:3, C:1, D:2}
> ```
>
> **(B) 왜 "지연 삭제"인가.** 파이썬 `heapq`는 원소의 **우선순위 갱신(decrease-key)** 을 직접 지원하지 않는다. 그래서 거리가 줄면 **새 (거리, 정점) 쌍을 그냥 새로 push**하고, 나중에 꺼냈을 때 `d > dist[u]`면 **버린다**. 힙에 한 정점이 여러 번 들어갈 수 있지만, 총 push 횟수는 간선 수에 비례(≤ E)하므로 복잡도는 그대로 O(E log V)다. 이것이 파이썬 다익스트라의 정석 패턴이다.
>
> **(C) 격자(grid) 위의 다익스트라.** 2차원 격자에서는 "정점 = 칸 `(r,c)`", "간선 = 상하좌우 이동"으로 본다. `dist`를 2차원 배열로 두고 힙에 `(거리, r, c)`를 넣는다. 이동 비용이 칸마다 다르면(예: 지형 높이차) 다익스트라, 모두 1이면 BFS로 충분하다.
>
> **(D) 최소최대(minimax) 경로 변형.** "경로상 **간선 가중치들의 합**"이 아니라 "경로상 **최댓값을 최소화**"하는 문제(예: Path With Minimum Effort, Swim in Rising Water)도 다익스트라 골격 그대로다. 완화 식에서 `dist[u] + w` 대신 **`max(dist[u], w)`** 를 쓰면 된다. "비용을 어떻게 누적하느냐"만 바꾸면 같은 뼈대가 재사용된다.
>
> **(E) 경로 복원(reconstruction).** 거리뿐 아니라 "어떤 길로 갔는지"가 필요하면, 완화할 때마다 `parent[v] = u`를 기록하고 도착점에서 `parent`를 거꾸로 따라 올라가 뒤집는다([[day-32-dp-knapsack/concept|Day 32]]의 선택 복원과 같은 방식).
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. V=정점 수, E=간선 수.
>
> | 구현 | 시간복잡도 | 공간 | 비고 |
> |---|---|---|---|
> | 다익스트라 (배열 스캔) | O(V²) | O(V) | 밀집 그래프(E≈V²)에 유리 |
> | **다익스트라 (힙)** | **O((V+E) log V)** | O(V+E) | 희소 그래프 표준, 코테 기본 |
> | BFS (모든 간선 = 1) | O(V+E) | O(V+E) | 가중치 없을 때 최단 경로 |
> | 0-1 BFS (가중치 0/1) | O(V+E) | O(V+E) | 덱(deque)으로 힙 대체 |
> | 벨만-포드 (음수 허용) | O(V·E) | O(V) | 음수 간선/음수 사이클 판별 |
>
> > **왜 log V가 붙나.** 각 간선을 완화할 때마다 힙에 push/pop이 일어나고(최대 E번), 힙 연산 하나가 O(log(힙 크기)) = O(log V)다. 따라서 E log V가 지배항. 정점 초기화·pop까지 합쳐 O((V+E) log V).
> >
> > **배열 스캔 O(V²) vs 힙 O(E log V).** 간선이 아주 많은 **밀집 그래프**(E ≈ V²)에서는 O(V²)가 오히려 O(V² log V)보다 빠를 수 있다. 하지만 코테 대부분은 **희소 그래프**라 힙 구현이 표준이다. "V, E 규모부터 확인"하는 습관([[day-16-big-o/concept|Day 16]]).
> >
> > **BFS로 충분한 경우를 놓치지 마라.** 모든 간선 가중치가 같으면(특히 1) 힙 없이 **BFS가 O(V+E)** 로 더 빠르고 코드도 짧다. 가중치가 0과 1뿐이면 **0-1 BFS**(덱 앞/뒤 삽입)로 힙을 없앨 수 있다. 다익스트라를 반사적으로 쓰기 전에 "가중치가 다양한가?"를 먼저 물어라.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"가중치가 다른가?"를 가장 먼저 물어라.** 가중치 없음/모두 동일 → [[day-26-bfs/concept|BFS]]. 가중치 0·1만 → 0-1 BFS(덱). 양의 가중치 다양 → **다익스트라**. 음수 간선 존재 → [[day-35-bellman-floyd/concept|벨만-포드]]. 이 분기가 알고리즘을 통째로 정한다.
> - **파이썬은 `decrease-key` 대신 "그냥 새로 push + 지연 삭제".** `heapq`에는 우선순위 갱신이 없으니, 완화 때마다 새 쌍을 push하고 꺼낼 때 `d > dist[u]`면 버리는 게 정석.
>   - 참고: [Python `heapq` 공식 문서](https://docs.python.org/3/library/heapq.html)
> - **튜플은 (거리, 정점) 순서로.** 힙은 튜플의 **첫 원소로 정렬**하므로 거리를 반드시 앞에 둔다. `(dist, node)` 순서를 뒤집으면 엉뚱한 기준으로 정렬된다.
> - **`if d > dist[u]: continue` 를 절대 빼지 마라.** 이 한 줄이 낡은(stale) 항목을 걸러 중복 처리를 막는다. 빼도 답은 맞지만 불필요한 재방문으로 느려지고, minimax 변형에선 틀릴 수도 있다.
> - **INF는 충분히 크게.** 가능한 최대 경로 합보다 크게 잡되 오버플로 걱정 없는 `float('inf')`가 파이썬에선 안전하고 편하다.
> - **minimax 변형은 완화 식만 바꾼다.** 합 최소화면 `d + w`, "경로 최댓값 최소화"면 `max(d, w)`. 뼈대는 동일 — 하나 익히면 응용이 열린다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **음수 간선이 있으면 다익스트라는 틀린다.** 그리디 확정 논리("한 번 뽑으면 최단 확정")가 음수에서 깨진다. 더 먼 정점을 지나 음수로 되돌아와 더 짧아질 수 있기 때문. 음수 간선 → **[[day-35-bellman-floyd/concept|벨만-포드]]**, 음수 **사이클**이면 최단 경로 자체가 정의되지 않는다(−∞).
> 2. **`heapq`는 최소 힙만 제공한다.** 최댓값 우선이 필요하면 부호를 뒤집어(`-값`) 넣는다. 다익스트라는 최소 힙이 정확히 맞는다.
> 3. **`decrease-key`는 없다 — push 중복을 허용하고 지연 삭제하라.** 방문 표시(visited)로 막으려다 오히려 갱신을 놓치는 버그가 흔하다. `dist[]` 비교(`d > dist[u]`)로 거르는 게 안전하다.
> 4. **`dist[u]` 확정 시점.** 힙에서 `u`를 처음(가장 작은 거리로) 꺼내는 순간이 확정이다. 그 이후 나오는 같은 `u`는 낡은 항목 — 반드시 `d > dist[u]`로 버려야 한다.
> 5. **간선 방향성·양방향 처리.** 무방향 그래프면 `graph[a].append((b,w))` 와 `graph[b].append((a,w))` **둘 다** 넣어야 한다. 프로그래머스 '배달'처럼 양방향 도로에서 한쪽만 넣으면 조용히 오답.
> 6. **중복 간선·자기 루프.** 같은 두 정점 사이에 가중치가 다른 간선이 여러 개일 수 있다. 인접 리스트에 전부 넣어도 완화가 자연히 최솟값을 고르므로 문제없지만, 인접 **행렬**로 저장하면 최솟값만 남겨야 한다.
> 7. **BFS를 다익스트라로 오버킬하지 마라.** 가중치가 전부 1인데 힙을 쓰면 불필요하게 log 배 느리다. 반대로 가중치가 다른데 BFS를 쓰면 **틀린다**(BFS는 간선 수 최소화지 가중치 합 최소화가 아니다).
> 8. **도달 불가(unreachable) 처리.** 끝났을 때 `dist[v]`가 여전히 INF면 그 정점은 도달 불가다. 답을 낼 때 `-1` 등으로 변환하는 걸 잊으면 INF가 그대로 새어 나간다(Network Delay Time 함정).
> 9. **제약이 붙은 최단 경로는 상태를 확장한다.** "최대 K번 경유" 같은 제약(Cheapest Flights)은 정점만으로 부족하고 `(정점, 사용한 경유 수)`를 상태로 삼거나 벨만-포드식 K회 완화를 써야 한다. 순수 다익스트라로는 제약을 못 건다.

> [!example]- 예제 코드 (Examples)
> ```python
> import heapq
> from collections import deque
>
> INF = float("inf")
>
> # (1) 다익스트라 - 우선순위 큐 (인접 리스트, 1-indexed)
> def dijkstra(graph, start, n):
>     dist = [INF] * (n + 1)
>     dist[start] = 0
>     pq = [(0, start)]                 # (거리, 정점)
>     while pq:
>         d, u = heapq.heappop(pq)
>         if d > dist[u]:               # 낡은 항목 -> 지연 삭제
>             continue
>         for v, w in graph[u]:
>             nd = d + w
>             if nd < dist[v]:          # 완화(relaxation)
>                 dist[v] = nd
>                 heapq.heappush(pq, (nd, v))
>     return dist
>
> # (2) 경로 복원 (parent 추적)
> def dijkstra_path(graph, start, end, n):
>     dist = [INF] * (n + 1)
>     parent = [-1] * (n + 1)
>     dist[start] = 0
>     pq = [(0, start)]
>     while pq:
>         d, u = heapq.heappop(pq)
>         if d > dist[u]:
>             continue
>         for v, w in graph[u]:
>             if d + w < dist[v]:
>                 dist[v] = d + w
>                 parent[v] = u
>                 heapq.heappush(pq, (dist[v], v))
>     if dist[end] == INF:
>         return INF, []
>     path, cur = [], end
>     while cur != -1:
>         path.append(cur)
>         cur = parent[cur]
>     return dist[end], path[::-1]
>
> # (3) BFS - 모든 간선 가중치가 1일 때의 최단 경로 (힙 불필요)
> def bfs_shortest(graph, start, n):
>     dist = [-1] * (n + 1)
>     dist[start] = 0
>     q = deque([start])
>     while q:
>         u = q.popleft()
>         for v in graph[u]:
>             if dist[v] == -1:
>                 dist[v] = dist[u] + 1
>                 q.append(v)
>     return dist
>
> # (4) minimax 변형 - 경로상 최대 간선을 최소화
> def dijkstra_minimax(graph, start, n):
>     worst = [INF] * (n + 1)
>     worst[start] = 0
>     pq = [(0, start)]
>     while pq:
>         d, u = heapq.heappop(pq)
>         if d > worst[u]:
>             continue
>         for v, w in graph[u]:
>             nd = max(d, w)            # 합이 아니라 최댓값
>             if nd < worst[v]:
>                 worst[v] = nd
>                 heapq.heappush(pq, (nd, v))
>     return worst
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> BFS(가중치 1) 대비 → 표준 다익스트라 → 기출 → minimax 변형 → 제약 최단 경로 순으로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Shortest Path in Binary Matrix | [LeetCode #1091](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | 🟢기초 | BFS(가중치 1) 대비 |
> | 2 | Network Delay Time | [LeetCode #743](https://leetcode.com/problems/network-delay-time/) | 🟡중급 | 표준 다익스트라 |
> | 3 | 배달 | [프로그래머스 #12978](https://school.programmers.co.kr/learn/courses/30/lessons/12978) | ⚫기출 | 무방향 다익스트라 |
> | 4 | Path With Minimum Effort | [LeetCode #1631](https://leetcode.com/problems/path-with-minimum-effort/) | 🟡중급 | minimax 격자 다익스트라 |
> | 5 | Cheapest Flights Within K Stops | [LeetCode #787](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | 🔴심화 | 제약(K경유) 최단 경로 |
> | 6 | Swim in Rising Water | [LeetCode #778](https://leetcode.com/problems/swim-in-rising-water/) | ⚫기출 | minimax 다익스트라 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 그래프 모델링(정점·간선·가중치), 표준 다익스트라와 BFS/minimax/제약 변형의 완화 식 차이, 도달 불가 처리와 지연 삭제, 프로그래머스/LeetCode 시그니처별 구현: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-33-dp-lis-lcs/concept|Day 33 — 부분 수열 DP (LIS·LCS)]] — DP 골격(배낭·부분 수열)을 마무리하고, 이번엔 그래프 위의 최적화인 최단 경로로 넘어온다. 완화(relaxation)는 DP의 "더 나은 부분해로 갱신"과 같은 사고다
- ➡️ **다음(next):** [[day-35-bellman-floyd/concept|Day 35 — 벨만-포드·플로이드-워셜]] — 다익스트라가 못 푸는 음수 간선(벨만-포드)과 모든 쌍 최단 경로(플로이드-워셜)로 최단 경로 삼총사를 완성한다
- 🧭 **관련(related):**
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 인접 리스트/행렬, 정점·간선 모델링이 다익스트라의 입력 토대
  - [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — 다익스트라는 "가중치가 있는 BFS". 모든 간선이 1이면 BFS가 곧 최단 경로
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — "현재 가장 가까운 정점 먼저 꺼내기"를 O(log V)로 만드는 핵심 자료구조
  - [[day-21-greedy/concept|Day 21 — 그리디 (Greedy)]] — "매번 최단 정점을 확정"하는 그리디 선택이 다익스트라 정당성의 근거(단, 음수 없을 때만)
  - [[day-31-dp/concept|Day 31 — 동적 계획법 입문]] — 완화(relaxation)는 "더 짧은 부분 경로로 갱신"하는 DP식 최적 부분 구조의 그래프 버전
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — O((V+E) log V)와 O(V²)를 V·E 규모로 판별해 구현을 고르는 사고의 토대
  - [[day-35-bellman-floyd/concept|Day 35 — 벨만-포드·플로이드-워셜]] — 다음 주제. 음수 간선·모든 쌍 최단 경로로 확장
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]
