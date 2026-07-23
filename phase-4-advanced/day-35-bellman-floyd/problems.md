# Day 35 — 연습문제: 최단 경로 (벨만-포드·플로이드-워셜)

> 출처는 **프로그래머스 / LeetCode만** 사용합니다.
> 난이도: 🟢기초 · 🟡중급 · 🔴심화 · ⚫기출
> 코드 해설 → [solutions.py](solutions.py) · 개념 → [concept.md](concept.md)

풀이 순서는 **벨만-포드(단일 출발·음수/제약) → 플로이드-워셜(모든 쌍·도달성·곱 변형)** 으로,
"음수/제약이면 벨만-포드", "모든 쌍이고 V가 작으면 플로이드-워셜"을 몸에 익히도록 배치했다.

---

## 1. Network Delay Time 🟡
- **출처:** [LeetCode #743](https://leetcode.com/problems/network-delay-time/)
- **유형:** 단일 출발 최단 경로 — **벨만-포드**로 풀어 [[day-34-dijkstra/concept|Day 34]]의 다익스트라 풀이와 대비
- **문제:** 방향 그래프의 간선 `times[i] = [u, v, w]`(u→v 전파 시간 w). 노드 `k`에서 신호를 보낼 때 **모든 노드가 받는 최소 시간**을 구하라. 일부라도 못 받으면 `-1`.
- **입력/출력:** `times: List[List[int]], n: int, k: int` → `int`
- **제약:** `1 <= k <= n <= 100`, `1 <= times.length <= 6000`, `1 <= w <= 100`
- **핵심 힌트:**
  - `k`에서 벨만-포드 → `dist[]`. 답은 **`max(dist[1..n])`**(가장 늦게 받는 노드).
  - 가중치가 모두 양수라 다익스트라가 더 빠르지만, 벨만-포드도 정답이며 "V−1 라운드 완화" 감을 잡기 좋다.
  - `max`가 INF면 도달 못 한 노드 → `-1`.

---

## 2. Cheapest Flights Within K Stops 🔴
- **출처:** [LeetCode #787](https://leetcode.com/problems/cheapest-flights-within-k-stops/)
- **유형:** **K-제약 벨만-포드**(스냅샷) — 라운드당 간선 1개씩 늘리는 정석
- **문제:** 도시 `n`개, 항공편 `flights[i] = [u, v, w]`(u→v 요금 w). `src`에서 `dst`까지 **최대 K번 경유(=간선 K+1개 이하)** 하는 **최소 요금**을 구하라. 불가능하면 `-1`.
- **입력/출력:** `n, flights, src, dst, k: int` → `int`
- **제약:** `1 <= n <= 100`, `0 <= flights.length <= n*(n-1)`, `1 <= w <= 10^4`, `0 <= k < n`
- **핵심 힌트:**
  - `K+1`번 라운드를 돌리되, 매 라운드 **직전 `dist`의 스냅샷(`snap = dist[:]`)으로만** 완화한다. 제자리 갱신하면 한 라운드에 간선이 여러 개 연쇄로 늘어 제약을 어긴다.
  - [[day-34-dijkstra/concept|Day 34]]에서 상태 다익스트라 `(비용, 도시, 남은 경유)`로도 풀었다 — 이번엔 벨만-포드 관점으로 다시 본다.

---

## 3. Find the City With the Smallest Number of Neighbors at a Threshold Distance 🟡
- **출처:** [LeetCode #1334](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/)
- **유형:** **표준 플로이드-워셜**(모든 쌍 최단 거리)
- **문제:** 도시 `n`개, 무방향 가중 간선 `edges[i] = [u, v, w]`, 임계 거리 `distanceThreshold`. 각 도시에서 임계 거리 **이하로 닿는 도시 수**가 **가장 적은** 도시를 구하라(동률이면 **번호가 큰** 도시).
- **입력/출력:** `n, edges, distanceThreshold: int` → `int`
- **제약:** `2 <= n <= 100`, `1 <= edges.length <= n*(n-1)/2`, `1 <= w, distanceThreshold <= 10^4`
- **핵심 힌트:**
  - 모든 쌍 최단 거리 → **플로이드-워셜 O(n³)**. `n <= 100`이라 `10^6`, 충분.
  - **무방향**이므로 `dist[u][v]`와 `dist[v][u]` **둘 다** 초기화.
  - 각 도시 i에 대해 `dist[i][j] <= threshold`인 j를 센다. 동률이면 큰 번호 → i를 오름차순으로 순회하며 `<=`로 갱신하면 자연히 큰 번호가 남는다.

---

## 4. 순위 ⚫ (기출)
- **출처:** [프로그래머스 #49191](https://school.programmers.co.kr/learn/courses/30/lessons/49191)
- **유형:** **플로이드-워셜 도달성(reachability)** — 승패의 전이 관계
- **문제:** 선수 `n`명. `results[i] = [A, B]`는 "A가 B를 이겼다". A가 B보다 강하면 항상 이긴다. 주어진 결과로 **정확히 순위를 매길 수 있는 선수 수**를 구하라.
- **입력/출력:** `n: int, results: List[List[int]]` → `int`
- **제약:** `1 <= n <= 100`, `1 <= results.length <= 4500`
- **핵심 힌트:**
  - 어떤 선수의 순위가 확정되려면 **자신을 이긴 선수 수 + 자신에게 진 선수 수 == n−1**이어야 한다(모든 다른 선수와의 상대 우열이 전이적으로 결정됨).
  - `beats[i][j]` = "i가 j를 (직접·간접) 이긴다"를 **플로이드-워셜 전이 폐포**로 채운다: `beats[i][j] |= beats[i][k] and beats[k][j]`.
  - i마다 `이긴 수 = sum(beats[i])`, `진 수 = sum(beats[j][i])`. 합이 n−1이면 확정.

---

## 5. Course Schedule IV 🟡
- **출처:** [LeetCode #1462](https://leetcode.com/problems/course-schedule-iv/)
- **유형:** **전이 폐포(transitive closure)** — 선수과목 도달성 질의
- **문제:** 과목 `numCourses`개, 선수 관계 `prerequisites[i] = [a, b]`(a는 b의 선수과목). 질의 `queries[j] = [u, v]`마다 "u가 v의 (직접·간접) 선수과목인가?"를 `bool`로 답하라.
- **입력/출력:** `numCourses: int, prerequisites, queries: List[List[int]]` → `List[bool]`
- **제약:** `2 <= numCourses <= 100`, `prerequisites`는 DAG, 질의 다수
- **핵심 힌트:**
  - `reach[u][v]` = "u가 v의 선수과목"을 플로이드-워셜 도달성으로 한 번에 전개하면, 질의는 **O(1) 조회**로 끝난다.
  - 완화 식: `reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])`. **k 최외곽** 규칙 동일.
  - 대안: 각 노드에서 BFS/DFS로 도달 집합을 구해도 되지만, 질의가 많으면 플로이드-워셜 전개가 깔끔하다.

---

## 6. Evaluate Division 🔴
- **출처:** [LeetCode #399](https://leetcode.com/problems/evaluate-division/)
- **유형:** **플로이드-워셜 곱(product) 변형** — 비율 전파
- **문제:** 방정식 `equations[i] = [A, B]`와 값 `values[i]`가 `A / B = values[i]`를 뜻한다. 질의 `queries[j] = [C, D]`마다 `C / D`의 값을 구하라(불가능하면 `-1.0`).
- **입력/출력:** `equations: List[List[str]], values: List[float], queries: List[List[str]]` → `List[float]`
- **제약:** `1 <= equations.length <= 20`, 변수는 소문자 문자열, `values[i] > 0`
- **핵심 힌트:**
  - 각 방정식은 간선 두 개: `ratio[A][B] = v`, `ratio[B][A] = 1/v`. 변수를 정점으로 인덱싱.
  - 최단 "거리(합)" 대신 **비율(곱)** 을 전파: `ratio[i][j] = ratio[i][k] * ratio[k][j]`(연결돼 있을 때). 플로이드-워셜 뼈대에서 `+`를 `*`로 바꾼 셈.
  - 질의 `C/D`는 `ratio[C][D]` 조회. 둘 중 하나라도 그래프에 없거나 연결 안 되면 `-1.0`.
  - 대안: 질의마다 DFS로 경로 곱을 구해도 된다(변수 수가 작아 둘 다 통과).

---

### 학습 체크리스트
- [ ] "음수 간선/제약 → 벨만-포드", "모든 쌍·V 작음 → 플로이드-워셜"을 먼저 가른다
- [ ] 벨만-포드는 V−1 라운드 완화 + INF 가드(`dist[u] != INF`)를 손에 익힌다 (1번)
- [ ] K-제약은 직전 라운드 스냅샷(`snap = dist[:]`)으로만 완화한다 (2번)
- [ ] 플로이드-워셜은 `for k → for i → for j`(k 최외곽)를 반사적으로 쓴다 (3번)
- [ ] 무방향 그래프는 `dist[u][v]`·`dist[v][u]` 둘 다 초기화한다 (3번)
- [ ] 도달성은 or/and, 비율은 곱(*)으로 완화 식만 바꾼다 (4·5·6번)
