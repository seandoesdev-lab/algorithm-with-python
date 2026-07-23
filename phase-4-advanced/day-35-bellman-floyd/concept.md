---
day: 35
phase: 4-advanced
title: 최단 경로 - 벨만-포드·플로이드-워셜 (Bellman-Ford & Floyd-Warshall)
category: [그래프, 최단 경로, 벨만-포드, 플로이드-워셜, 동적 계획법, 음수 간선]
difficulty: 중급
status: done
prev: "[[day-34-dijkstra/concept|Day 34 — 최단 경로: 다익스트라 (Dijkstra)]]"
next: "[[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find)]]"
related:
  - "[[day-34-dijkstra/concept|Day 34 — 최단 경로: 다익스트라 (Dijkstra)]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
  - "[[day-31-dp/concept|Day 31 — 동적 계획법 입문]]"
  - "[[day-21-greedy/concept|Day 21 — 그리디 (Greedy)]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]]"
  - "[[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find)]]"
sources:
  - https://leetcode.com/problems/network-delay-time/
  - https://leetcode.com/problems/cheapest-flights-within-k-stops/
  - https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/
  - https://leetcode.com/problems/course-schedule-iv/
  - https://leetcode.com/problems/evaluate-division/
  - https://school.programmers.co.kr/learn/courses/30/lessons/49191
  - https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
tags: [phase/4, topic/graph, topic/shortest-path, topic/bellman-ford, topic/floyd-warshall, topic/dp]
---

# Day 35 — 최단 경로: 벨만-포드·플로이드-워셜 (Bellman-Ford & Floyd-Warshall)

> [!abstract] 한눈 요약 (TL;DR)
> [[day-34-dijkstra/concept|다익스트라(Day 34)]]가 못 푸는 두 상황을 이 두 알고리즘이 메운다. **벨만-포드(Bellman-Ford)** 는 **음수 간선(negative edge)이 있어도** 한 출발점에서 모든 정점까지의 최단 거리를 구하고, 덤으로 **음수 사이클(negative cycle)** 까지 잡아낸다. 핵심은 딱 한 줄 — "**모든 간선을 훑으며 완화(relaxation)하는 라운드를 V−1번 반복**"하고, V번째 라운드에서도 갱신되면 음수 사이클이다. **플로이드-워셜(Floyd-Warshall)** 은 **모든 정점 쌍(all-pairs)** 사이의 최단 거리를 한 번에 구한다. "**경유지 k를 0..V−1까지 하나씩 열어주며 `dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])`**"라는 3중 for문이 전부다 — 이건 사실상 [[day-31-dp/concept|DP(Day 31)]]다. 셋을 한 줄로 정리하면: **가중치 다양·음수 없음·단일 출발 → 다익스트라 O((V+E)logV)**, **음수 있음·단일 출발 → 벨만-포드 O(V·E)**, **모든 쌍·정점 적음(V≤400) → 플로이드-워셜 O(V³)**. "출발점이 하나인가 전부인가, 음수 간선이 있는가, V가 몇인가" 이 세 질문이 알고리즘을 고른다.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **완화(relaxation) 복습.** 세 최단 경로 알고리즘의 공통 심장은 딱 하나, "u를 거쳐 v로 가는 게 더 짧으면 갱신한다" 즉 `if dist[u] + w(u,v) < dist[v]: dist[v] = dist[u] + w(u,v)`. 다익스트라는 이 완화를 **"가장 가까운 정점부터 그리디하게 한 번씩"** 했다. 벨만-포드와 플로이드-워셜은 완화를 적용하는 **순서·범위**만 다르게 한다.
>
> **벨만-포드 — "무식하게 V−1번 다 훑는다".** 다익스트라는 음수 간선에서 그리디 확정이 깨져 틀린다(더 먼 정점을 지나 음수로 되돌아오면 더 짧아질 수 있으므로). 벨만-포드는 **정점을 확정하지 않는다.** 대신 "모든 간선을 한 바퀴 완화"하는 것을 **라운드**로 삼아 이를 **V−1번** 반복한다. 왜 V−1번? 최단 경로는 사이클이 없으면 **최대 V−1개의 간선**으로 이뤄진다. 한 라운드가 지날 때마다 "정확히 알려진 최단 경로의 간선 수"가 최소 1씩 늘어나므로, V−1 라운드면 모든 최단 경로가 확정된다(수학적 귀납법으로 증명된다).
>
> **음수 사이클을 잡는 방법 (벨만-포드의 특권).** V−1 라운드로 끝났어야 할 완화가 **V번째 라운드에서도 또 줄어든다면**, 그건 "돌수록 짧아지는 길"이 있다는 뜻 — **음수 사이클**이다. 이 경우 최단 거리는 −∞로 발산하므로 "최단 경로가 정의되지 않는다"고 답해야 한다. 다익스트라·플로이드-워셜은 이 판별을 (기본형으로는) 못 한다.
>
> **플로이드-워셜 — "경유지를 하나씩 허락한다".** 질문을 바꾼다. "정점 i에서 j로 갈 때, **경유지로 {0,1,...,k}만 써도 되는 최단 거리**는?" k를 −1(경유 없음, 직행 간선만)에서 시작해 0,1,...,V−1까지 **하나씩 열어준다.** 새 경유지 k가 열리면 각 (i,j)는 "k를 안 쓰던 기존 값"과 "i→k→j로 가는 값" 중 작은 것을 택한다. `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`. 모든 k를 다 열면 dist[i][j]는 모든 경유지를 자유롭게 쓴 진짜 최단 거리다. **"중간 정점 집합"을 한 칸씩 넓히는 DP**라는 게 핵심 통찰이다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 벨만-포드 — V−1 라운드 + 음수 사이클 체크.**
> ```
> dist[] = INF, dist[start] = 0
> repeat V-1 times:                       # 라운드
>     for each edge (u, v, w):
>         if dist[u] != INF and dist[u] + w < dist[v]:
>             dist[v] = dist[u] + w        # 완화
> # 음수 사이클 판별: 한 번 더 돌려서 갱신되면 사이클 존재
> for each edge (u, v, w):
>     if dist[u] != INF and dist[u] + w < dist[v]:
>         return "NEGATIVE CYCLE"
> ```
> ```
>     (0)--1-->(1)          start = 0, V = 3
>      |        |           edges: (0,1,1) (1,2,-2) (0,2,4)
>      4       -2
>      v        v           라운드1: 0->1=1, 1->2=1-2=-1, 0->2=min(4,-1)=-1
>     (2)<------+           라운드2: 변화 없음  -> dist = [0, 1, -1]
> ```
> **조기 종료(early exit).** 어느 라운드에서 **한 번도 갱신이 없으면** 이미 수렴한 것이니 즉시 멈춰도 된다. 실전에서는 이 `updated` 플래그로 평균 속도를 크게 줄인다.
>
> **(B) 왜 "이전 라운드 스냅샷"이 K-제약 문제에서 중요한가.** 순수 벨만-포드는 배열을 제자리(in-place)로 갱신해도 답이 맞다(어차피 V−1 라운드면 수렴). 하지만 [[day-34-dijkstra/concept|Day 34]]의 Cheapest Flights처럼 "**간선 K+1개 이하**"라는 제약이 붙으면, 라운드당 간선이 **정확히 1개씩만** 늘어야 하므로 **직전 라운드의 스냅샷(`snap = dist[:]`)으로만 완화**해야 한다. 제자리 갱신하면 한 라운드에 여러 간선이 연쇄로 늘어나 제약을 어긴다.
>
> **(C) 플로이드-워셜 — 3중 for문(순서가 생명).**
> ```
> dist[i][j] = 간선 가중치 (없으면 INF), dist[i][i] = 0
> for k in range(V):            # 경유지 (반드시 바깥 루프!)
>     for i in range(V):
>         for j in range(V):
>             if dist[i][k] + dist[k][j] < dist[i][j]:
>                 dist[i][j] = dist[i][k] + dist[k][j]
> ```
> ```
>   경유지 k=0을 열기 전:        k=0(정점0 경유 허용) 연 뒤:
>     [0][1]=INF                  1을 0 거쳐 2로:
>     초기 직행 간선만            dist[1][2] = min(직행, dist[1][0]+dist[0][2])
>   k를 0,1,2...로 늘릴수록 더 많은 우회로가 후보에 추가된다.
> ```
> **k가 반드시 가장 바깥 루프여야 한다.** i, j가 바깥이고 k가 안쪽이면, 아직 완성되지 않은 `dist[i][k]`나 `dist[k][j]`를 참조해 틀린다. "경유지를 한 칸씩 늘린다"는 DP 단계가 k이므로 k가 최외곽이다. 이 루프 순서를 뒤집는 것이 플로이드-워셜 최다 실수.
>
> **(D) 플로이드-워셜의 음수 사이클 판별.** 모든 k를 돈 뒤 **어떤 i에 대해 `dist[i][i] < 0`** 이면, i를 지나 자기 자신으로 돌아오며 비용이 줄어드는 음수 사이클이 있다는 뜻이다.
>
> **(E) 도달성·전이 폐포(transitive closure) 변형.** "최단 거리"가 아니라 "i에서 j로 **갈 수 있는가(reachable)**"만 필요하면, `dist`를 boolean으로 두고 완화 식을 **`reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])`** 로 바꾼다. 뼈대는 똑같다(프로그래머스 '순위', Course Schedule IV).
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. V=정점 수, E=간선 수.
>
> | 알고리즘 | 시간복잡도 | 공간 | 음수 간선 | 대상 |
> |---|---|---|---|---|
> | 다익스트라 (힙) | O((V+E) log V) | O(V+E) | ❌ 불가 | 단일 출발 |
> | **벨만-포드** | **O(V·E)** | O(V) | ✅ 가능(사이클 판별) | 단일 출발 |
> | SPFA (벨만-포드 큐 최적화) | 평균 O(E), 최악 O(V·E) | O(V) | ✅ 가능 | 단일 출발 |
> | **플로이드-워셜** | **O(V³)** | O(V²) | ✅ 가능(사이클 판별) | 모든 쌍 |
> | 다익스트라 V회 반복 | O(V·(V+E) log V) | O(V²) | ❌ 불가 | 모든 쌍(음수 없을 때) |
>
> > **벨만-포드 O(V·E).** 라운드 V−1번 × 매 라운드 간선 E개 완화 = O(V·E). 다익스트라의 O((V+E)logV)보다 대체로 느리다 — 그래서 "음수 간선이 없으면 다익스트라"가 원칙이고, 벨만-포드는 음수 간선/사이클 판별이 필요할 때만 쓴다.
> >
> > **플로이드-워셜 O(V³)·O(V²).** 3중 for문이라 V가 조금만 커도 폭발한다. **V ≤ 400~500** 정도(V³ ≈ 10⁸ 이하)가 실전 상한선. 반대로 V가 작고 "모든 쌍"이 필요하면 코드가 5줄이라 압도적으로 간편하다. 공간도 V×V 행렬이라 V가 크면 메모리부터 터진다.
> >
> > **"모든 쌍"을 원할 때 무엇을 쓰나.** 음수 간선이 없고 그래프가 희소(E ≪ V²)하며 V가 크면 **다익스트라를 V번** 돌리는 게 O(V·E logV)로 더 빠를 수 있다. 음수 간선이 있거나 V가 작으면(≤400) 플로이드-워셜이 정답. 규모부터 따지는 습관([[day-16-big-o/concept|Day 16]]).

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **알고리즘 선택 3단 질문.** ① 출발점이 하나인가, 모든 쌍인가? → 모든 쌍이면 **플로이드-워셜**(V 작을 때). ② 음수 간선이 있는가? → 있으면 **벨만-포드**, 없으면 **다익스트라**. ③ V·E 규모가 감당되나? 이 순서로 물으면 거의 자동으로 정해진다.
> - **플로이드-워셜은 "k 먼저"만 외우면 된다.** `for k → for i → for j`. k가 안쪽으로 가면 무조건 틀린다. "경유지를 한 칸씩 개방한다"고 소리 내어 외우자. ([Floyd-Warshall 위키](https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm))
> - **벨만-포드는 "V−1 + 1".** V−1번 완화하고, +1번째에도 줄면 음수 사이클. 이 "+1 라운드"가 다익스트라·플로이드(기본형)에는 없는 벨만-포드만의 무기다.
> - **INF 오버플로 주의.** `dist[u] + w`에서 `dist[u]`가 INF면 더하지 마라(음수 w면 INF가 오염된다). 파이썬은 `float('inf')`라 오버플로는 없지만, `INF + (-3) = INF`가 되어 도달 불가 정점을 실수로 완화하는 버그가 생긴다. **`if dist[u] != INF`** 가드를 붙여라.
> - **플로이드-워셜 초기화.** `dist[i][i] = 0`, 나머지 INF, 간선 있으면 그 가중치. **중복 간선은 최솟값**만 남긴다(`dist[a][b] = min(dist[a][b], w)`).
> - **경로 복원.** 벨만-포드는 `parent[v]=u` 기록, 플로이드-워셜은 `nxt[i][j]=k`를 기록해 재귀로 복원한다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **다익스트라 vs 벨만-포드 vs 플로이드-워셜의 경계.** 음수 없음·단일 출발 → **다익스트라**(가장 빠름). 음수 있음·단일 출발 → **벨만-포드**. 모든 쌍·V 작음 → **플로이드-워셜**. 이 경계를 헷갈리면 오답 아니면 시간 초과다.
> 2. **음수 사이클이면 최단 경로는 정의되지 않는다(−∞).** 사이클을 돌수록 비용이 줄어 하한이 없다. 문제가 "음수 사이클이 있으면 −1/특정 값" 같은 처리를 요구하는지 반드시 확인한다.
> 3. **플로이드-워셜의 k는 반드시 최외곽 루프.** `for k` → `for i` → `for j`. 순서를 바꾸면 미완성 값을 참조해 조용히 틀린다. 코테 단골 실수 1위.
> 4. **INF 가드(`dist[u] != INF`)를 빼면 음수 간선에서 오염된다.** 도달 못 한 정점(INF)에서 음수 간선을 타고 완화하면 INF가 유한값처럼 번진다.
> 5. **K-제약 벨만-포드는 스냅샷 필수.** "간선 K개 이하"류는 직전 라운드 배열(`snap = dist[:]`)로만 완화해야 라운드당 간선이 1개씩 는다. 제자리 갱신은 제약을 어긴다([[day-34-dijkstra/concept|Day 34]] Cheapest Flights).
> 6. **무방향 그래프의 음수 간선은 곧 음수 사이클.** 무방향 간선 (u,v,−w)은 u↔v를 왕복하면 −2w로 발산한다. 벨만-포드의 음수 간선 예제는 대부분 **방향 그래프**임을 전제한다.
> 7. **플로이드-워셜 = DP.** 점화식 `d_k[i][j] = min(d_{k-1}[i][j], d_{k-1}[i][k]+d_{k-1}[k][j])`에서 k 차원을 제자리 갱신으로 없앤 것. [[day-31-dp/concept|Day 31]]의 "차원 압축"과 같은 사고다.
> 8. **도달성/전이 폐포도 같은 뼈대.** boolean OR/AND로 바꾸면 "누가 누구에게 도달 가능한가"(순위, Course Schedule IV), max/min·곱으로 바꾸면 최소최대·비율 전파(Evaluate Division)까지 확장된다.
> 9. **SPFA는 최악이 벨만-포드와 같다.** 큐 최적화 SPFA가 평균은 빠르지만 최악 O(V·E)라 "SPFA is dead"라는 말이 나온다. 안전하게는 정직한 벨만-포드나 (음수 없으면) 다익스트라.

> [!example]- 예제 코드 (Examples)
> ```python
> INF = float("inf")
>
> # (1) 벨만-포드: 단일 출발 최단 거리 + 음수 사이클 판별
> def bellman_ford(n, edges, start):
>     dist = [INF] * n
>     dist[start] = 0
>     for _ in range(n - 1):            # V-1 라운드
>         updated = False
>         for u, v, w in edges:
>             if dist[u] != INF and dist[u] + w < dist[v]:
>                 dist[v] = dist[u] + w
>                 updated = True
>         if not updated:               # 조기 종료
>             break
>     for u, v, w in edges:             # +1 라운드: 또 줄면 음수 사이클
>         if dist[u] != INF and dist[u] + w < dist[v]:
>             return None               # NEGATIVE CYCLE
>     return dist
>
> # (2) 플로이드-워셜: 모든 쌍 최단 거리 (k가 최외곽!)
> def floyd_warshall(n, edges):
>     dist = [[INF] * n for _ in range(n)]
>     for i in range(n):
>         dist[i][i] = 0
>     for u, v, w in edges:
>         dist[u][v] = min(dist[u][v], w)   # 중복 간선은 최솟값
>     for k in range(n):
>         for i in range(n):
>             if dist[i][k] == INF:         # 가지치기
>                 continue
>             for j in range(n):
>                 if dist[i][k] + dist[k][j] < dist[i][j]:
>                     dist[i][j] = dist[i][k] + dist[k][j]
>     return dist
>
> # (3) 도달성(전이 폐포): min/+ 대신 or/and
> def transitive_closure(n, edges):
>     reach = [[False] * n for _ in range(n)]
>     for u, v in edges:
>         reach[u][v] = True
>     for k in range(n):
>         for i in range(n):
>             for j in range(n):
>                 if reach[i][k] and reach[k][j]:
>                     reach[i][j] = True
>     return reach
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> 벨만-포드(단일 출발·음수/제약) → 플로이드-워셜(모든 쌍·도달성·곱 변형) 순으로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Network Delay Time | [LeetCode #743](https://leetcode.com/problems/network-delay-time/) | 🟡중급 | 벨만-포드(다익스트라 대비) |
> | 2 | Cheapest Flights Within K Stops | [LeetCode #787](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | 🔴심화 | K-제약 벨만-포드(스냅샷) |
> | 3 | Find the City ... Threshold Distance | [LeetCode #1334](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/) | 🟡중급 | 표준 플로이드-워셜 |
> | 4 | 순위 | [프로그래머스 #49191](https://school.programmers.co.kr/learn/courses/30/lessons/49191) | ⚫기출 | 플로이드-워셜 도달성 |
> | 5 | Course Schedule IV | [LeetCode #1462](https://leetcode.com/problems/course-schedule-iv/) | 🟡중급 | 전이 폐포(reachability) |
> | 6 | Evaluate Division | [LeetCode #399](https://leetcode.com/problems/evaluate-division/) | 🔴심화 | 플로이드-워셜 곱 변형 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 그래프 모델링, 벨만-포드 라운드·스냅샷·음수 사이클 판별, 플로이드-워셜 3중 for(k 최외곽)와 도달성/곱 변형, 프로그래머스/LeetCode 시그니처별 구현과 다중 접근 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-34-dijkstra/concept|Day 34 — 최단 경로: 다익스트라 (Dijkstra)]] — 음수 없는 단일 출발 최단 경로. 이번엔 다익스트라가 못 푸는 음수 간선(벨만-포드)과 모든 쌍(플로이드-워셜)으로 확장해 최단 경로 삼총사를 완성한다
- ➡️ **다음(next):** [[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find)]] — 그래프의 "연결성"을 거의 O(1)로 관리하는 자료구조. 최소 신장 트리(Kruskal)와 사이클 판별의 토대로 이어진다
- 🧭 **관련(related):**
  - [[day-34-dijkstra/concept|Day 34 — 다익스트라]] — 완화(relaxation)라는 공통 심장. 세 알고리즘은 완화의 순서·범위만 다르다
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 간선 리스트(벨만-포드)·인접 행렬(플로이드-워셜) 모델링이 입력 토대
  - [[day-31-dp/concept|Day 31 — 동적 계획법 입문]] — 플로이드-워셜은 "경유지 집합을 한 칸씩 넓히는" DP이고, 벨만-포드도 "간선 수 제한 하의 최단"이라는 DP다
  - [[day-21-greedy/concept|Day 21 — 그리디]] — 다익스트라가 통하던 그리디 확정이 음수 간선에서 깨지는 이유가 벨만-포드의 존재 이유
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — O(V·E)와 O(V³)를 V·E 규모로 판별해 세 알고리즘 중 하나를 고르는 사고
  - [[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]] — 도달성·전이 폐포는 그래프 위의 "누가 누구에 닿는가"로, 순회 사고와 이어진다
  - [[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find)]] — 다음 주제. 그래프 연결성·MST로 확장
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]
