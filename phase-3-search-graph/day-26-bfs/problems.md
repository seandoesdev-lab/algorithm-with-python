# Day 26 — BFS 연습문제 (Problems)

> 출처는 **프로그래머스 · LeetCode** 만 사용합니다. 난이도: 🟢기초 / 🟡중급 / 🔴심화 / ⚫기출
> 각 문제의 코드 해설은 [solutions.py](solutions.py) 에 있습니다.

## 문제 목록

| 번호 | 문제 | 출처 | 난이도 | 형태 |
|---|---|---|---|---|
| 1 | Binary Tree Level Order Traversal | [LeetCode #102](https://leetcode.com/problems/binary-tree-level-order-traversal/) | 🟢기초 | 트리 레벨 순회 BFS |
| 2 | 게임 맵 최단거리 | [프로그래머스 #1844](https://school.programmers.co.kr/learn/courses/30/lessons/1844) | 🟡중급 | 격자 최단 거리 BFS |
| 3 | Shortest Path in Binary Matrix | [LeetCode #1091](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | 🟡중급 | 8방향 격자 최단 거리 |
| 4 | Rotting Oranges | [LeetCode #994](https://leetcode.com/problems/rotting-oranges/) | 🟡중급 | 다중 소스 BFS(시간) |
| 5 | 01 Matrix | [LeetCode #542](https://leetcode.com/problems/01-matrix/) | 🟡중급 | 다중 소스 BFS(거리) |
| 6 | 단어 변환 | [프로그래머스 #43163](https://school.programmers.co.kr/learn/courses/30/lessons/43163) | 🟡중급 | 상태 공간 BFS(변환) |
| 7 | Open the Lock | [LeetCode #752](https://leetcode.com/problems/open-the-lock/) | 🟡중급 | 상태 공간 BFS(자물쇠) |
| 8 | Word Ladder | [LeetCode #127](https://leetcode.com/problems/word-ladder/) | 🔴심화 | 상태 공간 BFS(최소 변환) |

---

## 1. Binary Tree Level Order Traversal 🟢 — [LeetCode #102](https://leetcode.com/problems/binary-tree-level-order-traversal/)

이진 트리의 노드 값을 **위에서 아래로, 각 레벨(층)별로 왼쪽→오른쪽** 순서의 2차원 리스트로 반환하라.

- **핵심:** BFS의 "레벨 끊기" 정석. 큐에 든 현재 레벨의 크기 `size = len(q)`를 미리 재고, 그만큼만 꺼내 한 층을 만든다. 트리는 사이클이 없어 visited가 필요 없다([[day-11-tree-basics/concept|Day 11]] 연결).
- **팁:** DFS(전위/중위/후위)와 대비하라 — 같은 트리를 "깊이 우선"이 아니라 "너비 우선"으로 훑는 것이 곧 레벨 순회다.
- **복잡도:** O(N)(노드 수).

## 2. 게임 맵 최단거리 🟡 — [프로그래머스 #1844](https://school.programmers.co.kr/learn/courses/30/lessons/1844)

`1`(길)과 `0`(벽)으로 된 `n x m` 격자에서 좌상단 `(0,0)`에서 우하단 `(n-1,m-1)`까지 **지나야 하는 최소 칸 수**를 구하라. 도달 불가면 `-1`.

- **핵심:** 격자 최단 거리 BFS의 대표 문제. 시작 칸을 거리 1로 두고(칸 수를 세므로) 상하좌우로 퍼지며 목표 칸에 처음 닿는 순간의 거리가 답.
- **함정:** 벽에 막혀 도달 못 하면 반드시 `-1`을 반환해야 한다("도달 불가" 별도 처리).
- **복잡도:** O(n x m).

## 3. Shortest Path in Binary Matrix 🟡 — [LeetCode #1091](https://leetcode.com/problems/shortest-path-in-binary-matrix/)

`0`(통과 가능)/`1`(벽)로 된 `n x n` 격자에서 `(0,0)`→`(n-1,n-1)`까지 **8방향(대각선 포함)** 이동으로 지나는 칸 수의 최소를 구하라. 불가하면 `-1`.

- **핵심:** 방향 벡터를 8개로 확장한 격자 BFS. 시작·도착 칸이 `0`인지 먼저 확인해야 한다.
- **팁:** `dr, dc`를 8쌍으로 두면 상하좌우 4방향 코드가 그대로 재사용된다.
- **복잡도:** O(n^2).

## 4. Rotting Oranges 🟡 — [LeetCode #994](https://leetcode.com/problems/rotting-oranges/)

격자에 `0`(빈 칸)/`1`(신선한 오렌지)/`2`(썩은 오렌지)가 있다. 매 분 썩은 오렌지가 상하좌우의 신선한 오렌지를 썩게 한다. **모두 썩는 데 걸리는 최소 분**을 구하라(불가하면 `-1`).

- **핵심:** **다중 소스 BFS**의 정석. 처음부터 썩은 오렌지 **전부**를 거리 0으로 큐에 넣고 동시에 퍼뜨린다. 마지막에 도달한 거리가 총 걸린 분.
- **함정:** BFS 후 신선한 오렌지가 남아 있으면 `-1`. 처음부터 신선한 오렌지가 없으면 `0`.
- **복잡도:** O(R x C).

## 5. 01 Matrix 🟡 — [LeetCode #542](https://leetcode.com/problems/01-matrix/)

`0`과 `1`로 된 격자에서 각 칸에 대해 **가장 가까운 `0`까지의 거리**를 담은 격자를 반환하라.

- **핵심:** 다중 소스 BFS. "1에서 가장 가까운 0"을 각각 BFS로 구하면 O((RC)^2)로 느리다. 대신 **모든 `0`을 동시에 소스로** 넣고 한 번에 퍼뜨리면 O(RC)에 전부 구해진다(문제를 뒤집어 보는 발상 전환).
- **팁:** 이 "소스 뒤집기"가 다중 소스 BFS의 진짜 위력이다. Rotting Oranges와 골격이 같다.
- **복잡도:** O(R x C).

## 6. 단어 변환 🟡 — [프로그래머스 #43163](https://school.programmers.co.kr/learn/courses/30/lessons/43163)

`begin`에서 `target`으로, 한 번에 **한 글자만** 바꾸며 `words`에 있는 단어로만 변환할 때 **최소 변환 횟수**를 구하라. 불가하면 `0`.

- **핵심:** 각 단어를 정점, "한 글자 차이"를 간선으로 본 **상태 공간 BFS**. 최소 변환 횟수 = begin에서 target까지의 최단 거리.
- **팁:** 두 단어가 정확히 한 글자만 다른지 판별하는 헬퍼(`sum(a != b) == 1`)를 만들어 이웃을 찾는다.
- **함정:** `target`이 `words`에 없으면 변환 불가(`0`). 최단이므로 DFS가 아니라 BFS.
- **복잡도:** O(N^2 x L)(N=단어 수, L=단어 길이).

## 7. Open the Lock 🟡 — [LeetCode #752](https://leetcode.com/problems/open-the-lock/)

`"0000"`에서 시작하는 4자리 자물쇠. 한 번에 한 자리를 `+1`/`-1`(0↔9 순환)할 수 있다. `deadends`(걸리면 멈춤)를 피해 `target`에 도달하는 **최소 회전 횟수**를 구하라(불가하면 `-1`).

- **핵심:** 자물쇠 상태(문자열 4자리)가 정점, 한 번의 회전이 간선인 **상태 공간 BFS**. 각 상태에서 이웃은 8개(4자리 x ±1).
- **함정:** `deadends`와 이미 방문한 상태를 visited로 함께 막아야 한다. `"0000"`이 deadend면 즉시 `-1`.
- **복잡도:** 상태 수 O(10^4), 각 8이웃 → 사실상 상수 규모.

## 8. Word Ladder 🔴 — [LeetCode #127](https://leetcode.com/problems/word-ladder/)

`beginWord`에서 `endWord`로 한 글자씩 바꾸며 `wordList`의 단어로만 이동할 때, **가장 짧은 변환 순서의 단어 개수**(변환 횟수+1)를 구하라. 불가하면 `0`.

- **핵심:** 단어 변환(#43163)의 심화판. 최단이므로 BFS. 단어 수가 크면 "한 글자 차이" 비교가 병목이라, `h*t` 같은 **와일드카드 패턴 버킷**으로 이웃을 O(1)에 찾는 최적화가 핵심.
- **팁:** 각 단어의 각 자리를 `*`로 치환한 패턴을 키로 묶어두면, 같은 패턴을 공유하는 단어끼리가 곧 이웃이다.
- **복잡도:** 패턴 버킷 사용 시 O(N x L^2)(N=단어 수, L=길이).

---

## 학습 순서 제안

1. **레벨 끊기 감 잡기:** Binary Tree Level Order(#102) — BFS의 층 개념을 트리로 익힌다
2. **격자 최단 거리:** 게임 맵 최단거리(#1844) -> Shortest Path in Binary Matrix(#1091, 8방향 확장)
3. **다중 소스 BFS:** Rotting Oranges(#994) -> 01 Matrix(#542, 소스 뒤집기)
4. **상태 공간 BFS:** 단어 변환(#43163) -> Open the Lock(#752) -> Word Ladder(#127, 패턴 버킷 최적화)
