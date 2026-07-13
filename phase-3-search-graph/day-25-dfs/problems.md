# Day 25 — DFS 연습문제 (Problems)

> 출처는 **프로그래머스 · LeetCode** 만 사용합니다. 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 각 문제의 코드 해설은 [solutions.py](solutions.py) 에 있습니다.

## 문제 목록

| 번호 | 문제 | 출처 | 난이도 | 형태 |
|---|---|---|---|---|
| 1 | Flood Fill | [LeetCode #733](https://leetcode.com/problems/flood-fill/) | 🟢기초 | 격자 DFS(영역 칠하기) |
| 2 | Number of Islands | [LeetCode #200](https://leetcode.com/problems/number-of-islands/) | 🟡중급 | 격자 DFS(연결 영역 세기) |
| 3 | Max Area of Island | [LeetCode #695](https://leetcode.com/problems/max-area-of-island/) | 🟡중급 | 격자 DFS(영역 넓이) |
| 4 | 타겟 넘버 | [프로그래머스 #43165](https://school.programmers.co.kr/learn/courses/30/lessons/43165) | 🟡중급 | 상태 공간 DFS(+/-) |
| 5 | 네트워크 | [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162) | 🟡중급 | 인접 행렬 연결 요소 |
| 6 | Number of Provinces | [LeetCode #547](https://leetcode.com/problems/number-of-provinces/) | 🟡중급 | 인접 행렬 연결 요소 |
| 7 | Path Sum | [LeetCode #112](https://leetcode.com/problems/path-sum/) | 🟢기초 | 트리 DFS(경로 합) |
| 8 | Keys and Rooms | [LeetCode #841](https://leetcode.com/problems/keys-and-rooms/) | 🟡중급 | 그래프 도달 가능성 |
| 9 | 여행경로 | [프로그래머스 #43164](https://school.programmers.co.kr/learn/courses/30/lessons/43164) | 🔴심화 | DFS + 백트래킹(경로 구성) |

---

## 1. Flood Fill 🟢 — [LeetCode #733](https://leetcode.com/problems/flood-fill/)

2차원 이미지 `image`와 시작 좌표 `(sr, sc)`, 새 색 `color`가 주어진다. 시작 칸과 **같은 색으로 상하좌우 연결된** 모든 칸을 `color`로 바꾼 이미지를 반환하라.

- **핵심:** 격자 DFS의 가장 순수한 형태. "시작 칸의 원래 색"을 기억하고, 그 색인 이웃으로만 퍼진다.
- **함정:** 시작 칸이 이미 `color`와 같으면 아무것도 안 바뀌어야 하는데, 방문 체크 없이 진행하면 **무한 재귀**에 빠진다. `원래색 == color`이면 즉시 반환하거나, 방문 표시로 막아야 한다.
- **복잡도:** O(R x C).

## 2. Number of Islands 🟡 — [LeetCode #200](https://leetcode.com/problems/number-of-islands/)

`'1'`(땅)과 `'0'`(물)로 된 격자에서 상하좌우로 연결된 땅 덩어리(섬)의 개수를 구하라.

- **핵심:** "미방문 땅에서 DFS를 시작한 횟수 = 섬의 개수". DFS 한 번이 섬 하나를 통째로 물로 만든다(방문 처리).
- **팁:** 별도 visited 대신 방문한 `'1'`을 `'0'`으로 덮어써 메모리를 아낄 수 있다(입력 변형 주의).
- **복잡도:** O(R x C).

## 3. Max Area of Island 🟡 — [LeetCode #695](https://leetcode.com/problems/max-area-of-island/)

`1`로 연결된 섬들 중 **가장 넓은 섬의 칸 수**를 반환하라. 섬이 없으면 0.

- **핵심:** Number of Islands의 변형 — DFS가 "방문한 칸 수"를 세어 반환하도록 만들고, 섬마다 최댓값을 갱신한다.
- **팁:** 재귀 DFS가 `1 + 네 방향 재귀 합`을 반환하게 하면 깔끔하다.
- **복잡도:** O(R x C).

## 4. 타겟 넘버 🟡 — [프로그래머스 #43165](https://school.programmers.co.kr/learn/courses/30/lessons/43165)

음이 아닌 정수 배열 `numbers`의 각 수 앞에 `+` 또는 `-`를 붙여 순서대로 더해 `target`을 만드는 방법의 수를 구하라.

- **핵심:** 격자가 아닌 **상태 공간 DFS**. 인덱스 `i`에서 "더하기 가지"와 "빼기 가지"로 갈라지는 이진 트리를 끝까지 내려간다(2^n 완전 탐색, [[day-24-brute-force/concept|Day 24]] 연결).
- **함정:** 마지막 인덱스에 도달했을 때만 합이 target인지 검사한다(중간에 target이 되어도 끝까지 가야 함).
- **복잡도:** O(2^n). `numbers` 길이 <= 20이라 완전 탐색이 가능(2^20 ~= 100만).

## 5. 네트워크 🟡 — [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162)

컴퓨터 수 `n`과 연결 정보 인접 행렬 `computers`가 주어질 때, 네트워크(연결 요소)의 개수를 구하라.

- **핵심:** 인접 행렬 위의 연결 요소 세기. 미방문 컴퓨터에서 DFS를 시작한 횟수가 답.
- **팁:** 인접 행렬이므로 이웃 탐색이 O(n)이라 전체 O(n^2). n <= 200이라 충분.
- **복잡도:** O(n^2).

## 6. Number of Provinces 🟡 — [LeetCode #547](https://leetcode.com/problems/number-of-provinces/)

`isConnected[i][j] == 1`이면 도시 i, j가 직접 연결. 직간접으로 연결된 도시 그룹(province)의 수를 구하라.

- **핵심:** 프로그래머스 "네트워크"와 **완전히 동일한 문제**(인접 행렬 연결 요소). 두 문제를 나란히 풀며 "같은 골격, 다른 옷"임을 확인하라.
- **복잡도:** O(n^2).

## 7. Path Sum 🟢 — [LeetCode #112](https://leetcode.com/problems/path-sum/)

이진 트리와 `targetSum`이 주어질 때, 루트에서 **리프(leaf)까지의 경로** 합이 `targetSum`인 경로가 있으면 `True`.

- **핵심:** 트리 DFS. 내려가면서 남은 합을 줄이고, 리프에 도달했을 때 남은 합이 0인지 검사한다(트리는 사이클이 없어 visited 불필요, [[day-11-tree-basics/concept|Day 11]] 연결).
- **함정:** "리프"의 정의 — 양쪽 자식이 모두 없는 노드. 중간 노드에서 합이 맞아도 리프가 아니면 안 된다.
- **복잡도:** O(N).

## 8. Keys and Rooms 🟡 — [LeetCode #841](https://leetcode.com/problems/keys-and-rooms/)

방 0만 열려 있고 각 방에는 다른 방의 열쇠들이 있다. `rooms[i]`는 방 i에서 얻는 열쇠 목록. 모든 방을 방문할 수 있으면 `True`.

- **핵심:** 방을 정점, 열쇠를 간선으로 본 **도달 가능성(reachability)** DFS. 0에서 DFS로 방문한 방의 수가 전체 방 수와 같은지 확인.
- **복잡도:** O(V + E)(방 수 + 열쇠 총 개수).

## 9. 여행경로 🔴 — [프로그래머스 #43164](https://school.programmers.co.kr/learn/courses/30/lessons/43164)

항공권 목록 `tickets`(`[출발, 도착]`)가 주어진다. `"ICN"`에서 출발해 **모든 항공권을 한 번씩** 사용하는 경로를 구하라. 경로가 여러 개면 **알파벳 순으로 가장 앞선** 경로.

- **핵심:** DFS + **백트래킹**([[day-27-backtracking/concept|Day 27]] 선행 맛보기). 각 항공권 사용 여부를 표시하며 내려가고, 막히면 되돌린다(undo). 모든 항공권을 다 쓰면 성공.
- **팁:** 도착지를 알파벳 순으로 정렬해 먼저 시도하면, 처음 완성된 경로가 곧 사전순 최소 경로다.
- **함정:** 같은 구간(출발-도착) 항공권이 중복될 수 있어, 정점이 아닌 **간선(티켓) 단위**로 방문 표시해야 한다.
- **복잡도:** 최악 O(E!)이지만 정렬 + 조기 성공으로 실전에서는 훨씬 빠르다.

---

## 학습 순서 제안

1. **격자 감 잡기:** 733 -> 200 -> 695 (같은 골격이 점점 확장)
2. **연결 요소 쌍둥이:** 네트워크(#43162) -> Number of Provinces(#547)
3. **비격자 DFS:** 타겟 넘버(상태 공간) -> Path Sum(트리) -> Keys and Rooms(도달성)
4. **백트래킹 다리:** 여행경로(#43164) — 다음 주제 [[day-27-backtracking/concept|백트래킹]]으로 이어짐
