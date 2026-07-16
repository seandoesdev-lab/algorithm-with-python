# Day 28 — 그래프 표현과 순회 연습문제 (Problems)

> 출처는 **프로그래머스 · LeetCode** 만 사용합니다. 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 각 문제의 코드 해설은 [solutions.py](solutions.py) 에 있습니다.

## 문제 목록

| 번호 | 문제 | 출처 | 난이도 | 형태 |
|---|---|---|---|---|
| 1 | Find Center of Star Graph | [LeetCode #1791](https://leetcode.com/problems/find-center-of-star-graph/) | 🟢기초 | 표현·차수 이해 |
| 2 | Find if Path Exists in Graph | [LeetCode #1971](https://leetcode.com/problems/find-if-path-exists-in-graph/) | 🟢기초 | 인접리스트 + 연결성 |
| 3 | Find the Town Judge | [LeetCode #997](https://leetcode.com/problems/find-the-town-judge/) | 🟢기초 | 진입/진출 차수 |
| 4 | Number of Provinces | [LeetCode #547](https://leetcode.com/problems/number-of-provinces/) | 🟡중급 | 인접행렬 + 연결요소 |
| 5 | Number of Islands | [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | 🟡중급 | 격자 암시적 그래프 |
| 6 | Keys and Rooms | [LeetCode #841](https://leetcode.com/problems/keys-and-rooms/) | 🟡중급 | 도달 가능성 DFS |
| 7 | Clone Graph | [LeetCode #133](https://leetcode.com/problems/clone-graph/) | 🟡중급 | 인접리스트 복제 |
| 8 | All Paths From Source to Target | [LeetCode #797](https://leetcode.com/problems/all-paths-from-source-to-target/) | 🟡중급 | DAG 모든 경로 |
| 9 | 네트워크 | [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162) | 🟡중급 | 연결 요소 개수 |
| 10 | 여행경로 | [프로그래머스 #43164](https://school.programmers.co.kr/learn/courses/30/lessons/43164) | 🔴심화 | 인접리스트 DFS 사전순 |

---

## 1. Find Center of Star Graph 🟢 — [LeetCode #1791](https://leetcode.com/problems/find-center-of-star-graph/)

`n`개 정점의 **스타 그래프(star graph)** 가 간선 목록 `edges`로 주어진다. 스타 그래프는 하나의 중심 정점이 나머지 모든 정점과 연결된 형태다. **중심 정점**을 반환하라.

- **핵심:** 순회할 필요조차 없다. 중심 정점은 **모든 간선에 등장**하므로, 임의의 두 간선 `edges[0]`과 `edges[1]`에서 **공통으로 나타나는 정점**이 곧 중심이다.
- **팁:** "그래프 = 무조건 DFS/BFS"가 아니라, 표현(간선 목록)의 성질만으로 O(1)에 풀리는 경우가 있음을 보여주는 문제. 차수로 보면 중심의 차수는 `n-1`, 나머지는 1.
- **복잡도:** O(1)(간선 두 개만 확인).

## 2. Find if Path Exists in Graph 🟢 — [LeetCode #1971](https://leetcode.com/problems/find-if-path-exists-in-graph/)

`n`개 정점의 **무방향 그래프**가 `edges`로 주어진다. `source`에서 `destination`으로 가는 경로가 존재하는지 판별하라.

- **핵심:** 인접 리스트를 만들고(**무방향이니 양방향**) `source`에서 DFS 또는 BFS로 도달 가능한 정점을 모은 뒤 `destination`이 포함되는지 확인한다.
- **함정:** 무방향 간선을 한 방향만 넣으면 연결이 끊겨 오답. `source == destination`이면 즉시 `True`.
- **복잡도:** O(V + E).

## 3. Find the Town Judge 🟢 — [LeetCode #997](https://leetcode.com/problems/find-the-town-judge/)

마을에 `n`명이 있고 신뢰 관계 `trust[i] = [a, b]`(a가 b를 신뢰)가 주어진다. **재판관(town judge)** 은 ① 아무도 신뢰하지 않고, ② 나머지 `n-1`명 모두에게 신뢰받는 사람이다. 재판관의 번호를 반환하라(없으면 -1).

- **핵심:** 순회가 아니라 **차수(degree) 카운트**로 푼다. 각 사람의 `score = 진입차수 - 진출차수`를 세고, `score == n-1`인 사람이 재판관.
- **팁:** 방향 그래프의 in-degree/out-degree를 한 배열로 관리하는 전형. `a`는 -1, `b`는 +1.
- **복잡도:** O(V + E).

## 4. Number of Provinces 🟡 — [LeetCode #547](https://leetcode.com/problems/number-of-provinces/)

`n`개 도시의 연결 관계가 **인접 행렬** `isConnected[i][j]`(1이면 직접 연결)로 주어진다. 직접·간접으로 연결된 도시 무리(province)의 개수를 구하라.

- **핵심:** **인접 행렬로 주어진 연결 요소 세기.** 방문 안 한 도시를 만나면 카운트 +1 하고 그 도시에서 도달 가능한 전부를 순회로 표시한다.
- **팁:** 행렬이므로 이웃 순회가 `for j in range(n): if isConnected[i][j]`. Union-Find로도 풀 수 있으나 순회가 직관적.
- **복잡도:** O(V^2)(행렬 전체 스캔).

## 5. Number of Islands 🟡 — [LeetCode #200](https://leetcode.com/problems/number-of-islands/)

`'1'`(땅)과 `'0'`(물)로 채워진 격자에서 **섬의 개수**를 구하라. 섬은 상하좌우로 인접한 땅의 덩어리다.

- **핵심:** **격자 = 암시적 그래프.** 칸이 정점, 상하좌우가 간선이다. 방문 안 한 `'1'`을 만날 때마다 카운트 +1 하고 그 섬 전체를 DFS/BFS로 침몰(방문 표시)시킨다. 연결 요소 세기의 격자판.
- **함정:** 경계 검사 필수. 방문 표시를 격자 자체를 `'0'`으로 덮어 하거나 별도 `seen` 배열로 관리.
- **복잡도:** O(R x C).

## 6. Keys and Rooms 🟡 — [LeetCode #841](https://leetcode.com/problems/keys-and-rooms/)

`n`개의 방이 있고 방 `i`에는 다른 방의 열쇠 목록 `rooms[i]`가 있다. 0번 방에서 시작해 **모든 방에 들어갈 수 있는지** 판별하라.

- **핵심:** `rooms`가 곧 인접 리스트(방 i -> 열 수 있는 방들)인 **방향 그래프**. 0에서 DFS/BFS로 도달 가능한 방을 세어 `n`개면 `True`.
- **팁:** "모두 방문 가능한가" = 0에서의 도달 정점 수 == 전체 정점 수. 도달성(reachability) 문제의 전형.
- **복잡도:** O(V + E)(E = 전체 열쇠 수).

## 7. Clone Graph 🟡 — [LeetCode #133](https://leetcode.com/problems/clone-graph/)

무방향 연결 그래프의 한 정점 `node`가 주어진다(각 노드는 `val`과 이웃 리스트 `neighbors`를 가짐). 그래프 전체의 **깊은 복사(deep copy)** 를 반환하라.

- **핵심:** 순회하며 복제한다. `원본 노드 -> 복제 노드`를 `dict`(visited 겸 매핑)로 관리해, 이미 만든 노드는 재사용하고 사이클에서 무한 복제를 막는다.
- **함정:** visited를 안 쓰면 사이클에서 무한 루프. 매핑을 "방문 표시"로 겸하는 것이 핵심 테크닉.
- **복잡도:** O(V + E).

## 8. All Paths From Source to Target 🟡 — [LeetCode #797](https://leetcode.com/problems/all-paths-from-source-to-target/)

`n`개 노드의 **DAG(방향 비순환 그래프)** 가 인접 리스트 `graph`로 주어진다(`graph[i]`는 i에서 갈 수 있는 노드들). 노드 `0`에서 `n-1`까지의 **모든 경로**를 반환하라.

- **핵심:** 그래프 위의 DFS로 경로를 쌓아 나가는 백트래킹([[day-27-backtracking/concept|Day 27]])과의 접점. `n-1`에 닿으면 현재 경로의 복사본을 기록.
- **팁:** DAG라 사이클이 없어 visited가 필요 없다(같은 노드를 다른 경로로 다시 지나도 됨). 이 점이 일반 그래프와의 차이.
- **복잡도:** 최악 O(2^V x V)(경로 수가 지수).

## 9. 네트워크 🟡 — [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162)

컴퓨터 `n`대의 연결 정보가 **인접 행렬** `computers[i][j]`(1이면 i-j 연결)로 주어진다. 서로 연결된 컴퓨터 무리인 **네트워크의 개수**를 구하라.

- **핵심:** 이 Day의 대표 문제. **연결 요소 개수 = 네트워크 수.** 방문 안 한 컴퓨터에서 DFS/BFS로 한 네트워크 전체를 방문하고 카운트를 센다.
- **함정:** `computers[i][i] = 1`(자기 자신)이 섞여 있어도 로직에 영향 없도록. 무방향이므로 대칭 행렬.
- **복잡도:** O(n^2)(인접 행렬 스캔).

## 10. 여행경로 🔴 — [프로그래머스 #43164](https://school.programmers.co.kr/learn/courses/30/lessons/43164)

항공권 목록 `tickets`(`[출발, 도착]`)이 주어진다. 항상 `"ICN"`에서 출발해 **모든 항공권을 한 번씩 다 사용**하는 여행 경로를 구하라. 가능한 경로가 여럿이면 **알파벳 순서가 앞서는** 경로를 반환한다.

- **핵심:** 공항 코드(문자열) 라벨 그래프. `defaultdict(list)`로 인접 리스트를 만들고 **각 목적지 리스트를 정렬**한 뒤 DFS로 경로를 만든다(백트래킹: 티켓을 쓰면 제거, 실패하면 복원). 사전순 정렬 덕에 먼저 완성되는 경로가 답.
- **함정:** 정점이 아니라 **간선(티켓)** 을 다 써야 완성. 한 공항을 여러 번 방문할 수 있으므로 visited(정점)가 아니라 **티켓 사용 여부**로 관리한다.
- **팁:** 오일러 경로(Eulerian path)의 특수형. 티켓 수 `+1`이 경로 길이. 정렬 후 DFS면 첫 완성 경로가 사전순 최소.
- **복잡도:** 최악 지수지만 티켓 수가 작아(<=10,000, 실전 입력은 훨씬 작음) 통과.

---

## 학습 순서 제안

1. **표현·차수만으로:** Find Center of Star Graph(#1791) -> Find the Town Judge(#997) — 순회 없이 표현/차수로 푸는 감각
2. **기본 순회 + 연결성:** Find if Path Exists(#1971) -> Keys and Rooms(#841) — 인접 리스트 구축 + DFS/BFS 도달성
3. **연결 요소 세기:** Number of Provinces(#547) -> 네트워크(#43162) -> Number of Islands(#200) — 행렬/격자에서 무리 세기
4. **복제·경로 나열 심화:** Clone Graph(#133, 매핑=visited) -> All Paths(#797, DAG 경로) -> 여행경로(#43164, 간선 소모 DFS)
