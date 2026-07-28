# Day 38 — 연습문제: 위상 정렬 (Topological Sort)

> 출처는 **프로그래머스**와 **LeetCode**만 사용한다.
> 순서: 사이클 판별 → 순서 출력 → 기출 부분 순서 → 역방향 소거 → DAG DP → 잎 소거.
> 해설 코드는 [solutions.py](solutions.py), 개념은 [concept.md](concept.md).

| # | 문제 | 출처 | 난이도 | 유형 |
|---|---|---|---|---|
| 1 | Course Schedule | [LeetCode #207](https://leetcode.com/problems/course-schedule/) | 🟡중급 | 위상 정렬 가능성 = DAG 사이클 판별 |
| 2 | Course Schedule II | [LeetCode #210](https://leetcode.com/problems/course-schedule-ii/) | 🟡중급 | 위상 순서 출력(칸 vs DFS) |
| 3 | 순위 | [프로그래머스 #49191](https://school.programmers.co.kr/learn/courses/30/lessons/49191) | ⚫기출 | 부분 순서·도달 가능성으로 순위 확정 |
| 4 | Find Eventual Safe States | [LeetCode #802](https://leetcode.com/problems/find-eventual-safe-states/) | 🔴심화 | 역방향 그래프 위상 소거 |
| 5 | Parallel Courses III | [LeetCode #2050](https://leetcode.com/problems/parallel-courses-iii/) | 🔴심화 | 위상 순서 위 DP = DAG 최장 경로 |
| 6 | Minimum Height Trees | [LeetCode #310](https://leetcode.com/problems/minimum-height-trees/) | 🔴심화 | 잎 소거(degree 1 peeling) |

---

## 1. Course Schedule 🟡중급

**출처:** [LeetCode #207 — Course Schedule](https://leetcode.com/problems/course-schedule/)

`numCourses`개의 과목(0번부터 번호)이 있고, `prerequisites[i] = [aᵢ, bᵢ]`는 **"aᵢ를 들으려면 bᵢ를 먼저 들어야 한다"** 는 뜻이다. 모든 과목을 수강할 수 있으면 `true`, 아니면 `false`를 반환하라.

```
입력: numCourses = 2, prerequisites = [[1,0]]
출력: true         (0 -> 1 순서로 들으면 된다)

입력: numCourses = 2, prerequisites = [[1,0],[0,1]]
출력: false        (서로를 요구 -> 사이클)
```

**시그니처:** `def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool`

> [!tip]- 힌트
> - **이 문제의 본질은 "위상 정렬이 존재하는가"** = "이 그래프가 DAG인가" = **사이클이 없는가**이다. 순서를 실제로 만들 필요는 없고 **만들 수 있는지만** 답하면 된다.
> - **간선 방향을 소리 내어 확정하라.** `[a, b]` = "b를 먼저, 그 다음 a" → 간선은 **b → a**. 따라서 `adj[b].append(a)`, `indeg[a] += 1`. 여기서 뒤집는 게 이 유형 최다 오답이고, 뒤집어도 예제 1은 우연히 통과한다.
> - **칸 알고리즘:** 진입 차수 0을 큐에 넣고 흘려보낸 뒤 `len(order) == numCourses`인지 본다. 이 한 줄이 정답이다.
> - **DFS로 풀려면 반드시 3색(WHITE/GRAY/BLACK).** `visited` bool 하나만 쓰면 "이미 끝난 다른 분기"를 사이클로 오판해 정상 DAG를 `false`로 답한다.
> - 과목 수가 최대 2000, 재귀 깊이 문제는 크지 않지만 습관적으로 **칸을 기본**으로 쓰자.
> - 목표 복잡도: **O(V+E)**.

---

## 2. Course Schedule II 🟡중급

**출처:** [LeetCode #210 — Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)

#207과 입력은 같다. 이번엔 **실제 수강 순서를 배열로 반환**하라. 유효한 순서가 여러 개면 **아무거나** 반환해도 되고, 불가능하면 **빈 배열**을 반환한다.

```
입력: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
출력: [0,1,2,3]  또는  [0,2,1,3]   (둘 다 정답)

입력: numCourses = 1, prerequisites = []
출력: [0]
```

**시그니처:** `def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]`

> [!tip]- 힌트
> - #207의 칸 알고리즘에서 **`order` 리스트를 그대로 반환**하면 끝이다. 길이가 `numCourses`가 아니면 `[]`.
> - **고립 정점을 빠뜨리지 마라.** 선행 관계가 전혀 없는 과목도 진입 차수 0이므로 **초기 큐에 반드시 들어가야 한다**. `for v in range(numCourses)`로 돌려야지, 간선 목록에 등장한 정점만 모으면 안 된다.
> - **DFS 버전은 post-order를 뒤집는다.** 되돌아 나오는 순간 스택에 쌓고 마지막에 `[::-1]`. **뒤집는 걸 잊으면 정확히 역순**이 나온다.
> - 채점기가 "임의의 유효한 순서"를 받아주므로 칸과 DFS 결과가 달라도 둘 다 통과한다. 만약 문제가 **사전 순 최소**를 요구했다면 `deque` → `heapq`로 바꾸면 된다.
> - 목표 복잡도: **O(V+E)**.

---

## 3. 순위 ⚫기출

**출처:** [프로그래머스 #49191 — 순위](https://school.programmers.co.kr/learn/courses/30/lessons/49191) (Level 3, 그래프)

`n`명의 선수가 1대1 권투 경기를 한다. **실력이 높은 선수가 반드시 이긴다.** `results[i] = [A, B]`는 "A가 B를 이겼다"는 뜻이다. 일부 경기 기록이 유실되어 전체 순위를 정확히 매길 수 없을 때, **정확하게 순위를 매길 수 있는 선수의 수**를 반환하라.

```
입력: n = 5, results = [[4,3],[4,2],[3,2],[1,2],[2,5]]
출력: 2
```

**시그니처:** `def solution(n, results):`

> [!tip]- 힌트
> - **핵심 통찰:** 어떤 선수 `x`의 순위가 확정되려면, **나머지 n−1명 전부와 승패 관계가 (직접이든 간접이든) 결정**되어야 한다. 즉 **`x`가 이기는 사람 수 + `x`에게 이기는 사람 수 == n−1`**.
> - "간접 승리"는 **도달 가능성(reachability)** 이다. A→B, B→C면 A→C도 확정이다. 이걸 전부 구하는 게 **전이 폐쇄(transitive closure)**.
> - **접근 1 — 플로이드-워셜 O(n³).** `n ≤ 100`이므로 100³ = 100만으로 넉넉하다. `reach[a][b] = True`를 채운 뒤, `k`를 경유지로 `reach[i][k] and reach[k][j] → reach[i][j]`. [[day-35-bellman-floyd/concept|Day 35]]에서 배운 그 3중 루프다. 코드가 가장 짧다.
> - **접근 2 — 정점마다 양방향 DFS/BFS O(n·(n+E)).** 정방향 그래프에서 `x`가 이기는 사람 수를 세고, 역방향 그래프에서 `x`를 이기는 사람 수를 센다. 합이 `n−1`이면 확정. 이쪽이 개념적으로 더 명확하다.
> - **1-based 주의.** 선수 번호가 1..n이므로 배열을 `n+1` 크기로 잡거나 인덱스를 −1 하라. 프로그래머스에서 자주 밟는 지뢰다.
> - **위상 정렬과의 연결:** "순위가 확정된다"는 건 그 정점이 **전체 순서에서 위치가 하나로 고정**된다는 뜻이다. 모든 선수의 순위가 확정될 조건이 곧 "위상 순서가 유일하다 = 해밀턴 경로가 존재한다"이다.

---

## 4. Find Eventual Safe States 🔴심화

**출처:** [LeetCode #802 — Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/)

방향 그래프가 `graph[i] = [i에서 나가는 간선의 도착점들]`로 주어진다. **종착 노드(terminal node)** 는 나가는 간선이 없는 노드다. **안전한 노드(safe node)** 는 그 노드에서 시작하는 **모든 경로가 반드시 종착 노드에서 끝나는** 노드다(사이클에 절대 빠지지 않는다). 안전한 노드를 **오름차순으로** 반환하라.

```
입력: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
출력: [2,4,5,6]
      (0->1->3->0 사이클에 갇힌 0,1,3 은 안전하지 않다)
```

**시그니처:** `def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]`

> [!tip]- 힌트
> - **역방향 그래프 트릭.** "끝에서부터" 성질을 묻는 문제는 **간선을 전부 뒤집어** 칸을 돌린다. 원래 그래프의 **out-degree 0**(=종착 노드)이 역방향 그래프의 시작점이 된다.
> - 절차: `rev[v].append(u)`로 뒤집고 `outdeg[u]`를 센다 → `outdeg == 0`인 노드를 큐에 넣는다 → 큐에서 `u`를 꺼내 안전으로 표시하고, `rev[u]`의 각 `p`에 대해 `outdeg[p] -= 1` → 0이 되면(= **모든 출구가 안전해졌다**) `p`도 안전.
> - **왜 맞는가:** `p`의 모든 나가는 간선이 안전한 노드로 향하면 `p`에서 출발하는 어떤 경로도 결국 종착점에 도달한다. 반대로 사이클에 속한 노드는 out-degree가 절대 0으로 떨어지지 않는다 — **#207의 "진입 차수가 0이 안 된다"의 거울상**이다.
> - **접근 2 — DFS 3색.** `WHITE/GRAY/BLACK` 대신 여기서는 `미방문 / 방문중 / 안전 / 위험`으로 메모이제이션한다. 방문중(GRAY)인 노드를 다시 만나면 그 경로는 사이클이므로 unsafe로 확정.
> - 목표 복잡도: **O(V+E)**.

---

## 5. Parallel Courses III 🔴심화

**출처:** [LeetCode #2050 — Parallel Courses III](https://leetcode.com/problems/parallel-courses-iii/)

`n`개의 과목(1번부터)과 선행 관계 `relations[j] = [prevCourseⱼ, nextCourseⱼ]`, 그리고 각 과목의 소요 개월 수 `time[i]`(0-indexed, 과목 `i+1`의 시간)가 주어진다. **선행 과목이 전부 끝나야** 그 과목을 시작할 수 있고, **동시에 여러 과목을 들을 수 있다.** 모든 과목을 끝내는 데 필요한 **최소 개월 수**를 반환하라. 입력 그래프는 **DAG임이 보장**된다.

```
입력: n = 3, relations = [[1,3],[2,3]], time = [3,2,5]
출력: 8
      1(3개월)과 2(2개월)를 동시에 시작 -> 3개월 뒤 3 시작 -> 3+5 = 8

입력: n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]
출력: 12
```

**시그니처:** `def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int`

> [!tip]- 힌트
> - **이게 위상 정렬의 가장 중요한 응용이다.** 답은 **DAG 최장 경로(critical path)** 다. "동시에 들을 수 있다"는 조건 때문에 합이 아니라 **max**가 된다.
> - 점화식: `finish[v] = max(모든 선행 u에 대해 finish[u]) + time[v]`. 칸 알고리즘으로 정점을 꺼내며 `finish[v] = max(finish[v], finish[u] + time[v])`로 갱신하면 된다.
> - **왜 한 번 훑기로 충분한가:** 칸이 `u`를 큐에서 **꺼내는 시점**에 `u`의 모든 선행이 이미 처리되어 `finish[u]`가 **최종 확정값**이다. 이 불변식이 DAG DP를 성립시킨다.
> - **초기화 주의.** 진입 차수 0인 과목은 `finish[v] = time[v]`(0 시점에 즉시 시작)로 시작해야 한다. 전부 0으로 두면 시작 과목의 소요 시간이 누락된다.
> - 답은 `max(finish)`. 마지막 정점 하나만 보면 안 된다(끝나는 지점이 여러 개일 수 있다).
> - **일반 그래프의 최장 경로는 NP-난해**지만 DAG로 한정하면 **O(V+E)** 다. 면접 단골 대비.
> - `n ≤ 5·10⁴`, 관계도 5·10⁴ 규모 → 재귀 대신 **칸(반복문)** 으로 풀어야 안전하다.

---

## 6. Minimum Height Trees 🔴심화

**출처:** [LeetCode #310 — Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)

`n`개의 노드(0번부터)와 `n−1`개의 **무방향** 간선으로 이루어진 트리가 주어진다. 임의의 노드를 루트로 잡으면 트리의 높이가 정해지는데, **높이가 최소가 되는 루트(들)** 를 모두 반환하라. 답은 항상 **1개 또는 2개**다.

```
입력: n = 4, edges = [[1,0],[1,2],[1,3]]
출력: [1]

입력: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
출력: [3,4]
```

**시그니처:** `def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]`

> [!tip]- 힌트
> - **모든 노드를 루트로 BFS 돌리면 O(V²)로 시간 초과** (n ≤ 2·10⁴). 다른 관점이 필요하다.
> - **잎 소거(leaf peeling).** 차수 1인 잎을 **한 층씩 동시에** 벗겨낸다. 남은 노드가 **2개 이하가 되면 멈추고**, 그때 남은 것이 답이다. 칸 알고리즘과 골격이 완전히 같다 — 차이는 방향 그래프의 `indegree == 0` 대신 무방향의 **`degree == 1`**.
> - **왜 맞는가:** 트리의 최소 높이 루트는 **트리의 중심(center)** 이고, 중심은 가장 긴 경로(지름, diameter)의 **중간점**이다. 양쪽 끝에서 동시에 한 칸씩 좁혀 들어가면 중간에 도달한다. 지름의 간선 수가 짝수면 중심 1개, 홀수면 2개 — 그래서 답이 항상 1~2개다.
> - **종료 조건이 핵심.** `while remaining > 2`이고, 루프 안에서 **현재 큐 크기만큼만**(`for _ in range(len(leaves))`) 처리해 한 층씩 벗겨야 한다. 이 층 단위 처리가 없으면 한쪽만 깊이 파고들어 틀린다.
> - **엣지 케이스:** `n == 1`이면 간선이 없고 답은 `[0]`. `n == 2`면 두 노드 모두 차수 1이라 루프에 들어가지 않고 `[0,1]`이 답이다. 이 둘을 놓치면 무한 루프나 빈 배열이 나온다.
> - 목표 복잡도: **O(V+E) = O(n)**.

---

## 🔗 관련 문서

- 개념 정리: [concept.md](concept.md)
- 실행 예제: [examples.py](examples.py)
- 문제 해설: [solutions.py](solutions.py)
