---
day: 43
phase: 4-advanced
title: 최소 공통 조상 (LCA: Lowest Common Ancestor)
category: [최소 공통 조상, Lowest Common Ancestor, LCA, 이진 상승, Binary Lifting, 희소 배열, Sparse Table, 오일러 투어, Euler Tour, RMQ, Range Minimum Query, 타잔 오프라인, Tarjan Offline LCA, 트리 거리, Tree Distance, 조상 질의, Ancestor Query, 트리 DP, Tree DP]
difficulty: 심화
status: done
prev: "[[day-42-string-matching/concept|Day 42 — 문자열 매칭 (KMP·라빈-카프)]]"
next: "[[day-44-tree-dp/concept|Day 44 — 트리 DP (Tree DP)]]"
related:
  - "[[day-42-string-matching/concept|Day 42 — 문자열 매칭 (KMP·라빈-카프)]]"
  - "[[day-11-tree-basics/concept|Day 11 — 트리 기본 (Tree Basics)]]"
  - "[[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]]"
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
  - "[[day-22-recursion/concept|Day 22 — 재귀와 분할정복]]"
  - "[[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find)]]"
  - "[[day-40-segment-tree/concept|Day 40 — 세그먼트 트리·펜윅 트리]]"
  - "[[day-41-bitmask/concept|Day 41 — 비트마스킹 (Bitmasking)]]"
  - "[[day-31-dp/concept|Day 31 — 동적 계획법 입문]]"
  - "[[day-35-bellman-floyd/concept|Day 35 — 벨만-포드·플로이드-워셜]]"
  - "[[day-18-binary-search/concept|Day 18 — 이분 탐색]]"
  - "[[day-14-prefix-sum/concept|Day 14 — 누적 합 (Prefix Sum)]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
sources:
  - https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
  - https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
  - https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/
  - https://school.programmers.co.kr/learn/courses/30/lessons/72413
  - https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/
  - https://leetcode.com/problems/kth-ancestor-of-a-tree-node/
  - https://leetcode.com/discuss/post/4299594/binary-lifting-technique-a-beginners-gui-k7p0/
  - https://leetcode.com/discuss/study-guide/4139774/Binary-Lifting-to-compute-Kth-ancestors-in-fastest-time/
tags: [phase/4, topic/lca, topic/binary-lifting, topic/tree, topic/sparse-table, topic/euler-tour, topic/rmq, topic/union-find, topic/graph]
---

# Day 43 — 최소 공통 조상 (LCA: Lowest Common Ancestor)

> [!abstract] 한눈 요약 (TL;DR)
> **최소 공통 조상(LCA, Lowest Common Ancestor)** 은 트리에서 두 노드 `u`, `v`를 **동시에 자손으로 갖는 조상 중 가장 깊은 것**이다. 정의는 한 줄인데, 이 한 줄이 **"트리에서 두 점 사이의 경로"에 관한 거의 모든 질문의 관문**이다. 왜냐하면 트리에는 **두 노드를 잇는 경로가 정확히 하나**뿐이고, 그 경로는 반드시 **`u` → LCA → `v`** 형태로 **꺾이기** 때문이다. 그래서 LCA를 알면 **두 노드 사이 거리 = `depth[u] + depth[v] - 2·depth[LCA]`** 가 즉시 나오고, 경로 위의 가중치 합·최댓값·XOR 같은 것도 [[day-14-prefix-sum/concept|누적 합(Day 14)]]을 루트 기준으로 미리 쌓아 두면 `O(1)`에 답한다. 오늘의 핵심은 **"질의가 한 번인가, 수십만 번인가"에 따라 도구가 완전히 달라진다**는 것이다. **① 질의 1회 + 이진 트리 객체(LeetCode 스타일)** 라면 **후위 순회 재귀 한 방**이 정답이다 — `왼쪽에서도 찾고 오른쪽에서도 찾았으면 여기가 LCA`라는 6줄 코드([#236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/))이고, **BST라면 값 비교로 한 방향만 내려가 `O(h)`** 다([#235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)). **② 질의가 많다면 재귀는 매번 `O(N)`이라 `O(Q·N)`으로 터진다.** 이때의 표준 무기가 **이진 상승(binary lifting)** — `up[k][v]` = `v`의 **`2^k`번째 조상**을 DP로 채워 두고(`up[k][v] = up[k-1][up[k-1][v]]`), 질의 때 **깊이 차를 이진수로 분해해 점프**한다. 전처리 `O(N log N)`, 질의 `O(log N)`. **"어떤 숫자든 2의 거듭제곱의 합으로 쓸 수 있다"** 는 [[day-41-bitmask/concept|비트 사고(Day 41)]]가 트리에 그대로 옮겨진 것이고, `k`번째 조상 질의([#1483](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/))는 이 표 하나로 끝난다. **③ 질의를 `O(1)`에 답해야 한다면** **오일러 투어(Euler tour)로 트리를 배열로 펼쳐** LCA를 **구간 최솟값 질의(RMQ)** 로 바꾸고 **희소 배열(sparse table)** 을 얹는다 — **"트리 문제를 배열 문제로 환원"** 하는 사고가 [[day-40-segment-tree/concept|세그먼트 트리(Day 40)]]와 만나는 지점이다. **④ 질의를 미리 다 알고 있다면(오프라인)** **타잔(Tarjan) 알고리즘**이 [[day-36-union-find/concept|Union-Find(Day 36)]] 하나로 거의 선형에 전부 답한다. 파이썬 실전에서 반드시 기억할 것: **재귀 깊이.** 노드가 `10^5`인 **체인 모양 트리**에서 재귀 DFS는 `RecursionError`로 죽는다 — **`sys.setrecursionlimit`은 임시방편이고, 정답은 반복문 DFS 또는 BFS로 `parent`·`depth`를 만드는 것**이다. 핵심 한 줄: **"트리의 모든 경로는 LCA에서 꺾인다. 그래서 LCA는 트리 경로 문제의 좌표계다."**

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **정의.** 루트가 정해진 트리(rooted tree)에서 노드 `u`, `v`의 **최소 공통 조상 LCA(u, v)** 는
> - `u`의 조상이면서 동시에 `v`의 조상인 노드들 중
> - **깊이가 가장 깊은(=가장 낮은, lowest)** 노드다.
>
> 여기서 **"조상"은 자기 자신을 포함**한다는 관례가 표준이다. 즉 `v`가 `u`의 조상이면 **`LCA(u, v) = v`** 다. LeetCode #235/#236도 이 관례를 따른다("a node can be a descendant of itself").
>
> **이름의 함정.** "**최소(lowest)**"는 **값이 작다는 뜻이 아니라 트리에서 아래쪽(깊다)** 이라는 뜻이다. 한국어 "최소 공통 조상"의 "최소"도 **깊이 기준**이다. 루트는 항상 모든 쌍의 공통 조상이지만 **가장 얕아서** 답이 아니다.
>
> ```
>                 1              depth 0
>               /   \
>              2     3           depth 1
>             / \     \
>            4   5     6         depth 2
>               / \
>              7   8             depth 3
>
>   LCA(7, 8) = 5     (둘의 바로 위 부모)
>   LCA(4, 8) = 2     (4의 조상 {4,2,1}, 8의 조상 {8,5,2,1} -> 공통 {2,1} -> 깊은 것 = 2)
>   LCA(4, 6) = 1     (다른 가지로 완전히 갈라진다 -> 루트에서만 만난다)
>   LCA(5, 8) = 5     (5 가 8 의 조상. 자기 자신도 조상으로 센다!)
>   LCA(3, 3) = 3     (같은 노드)
> ```
>
> ---
>
> ### 비유 1 — 가족의 촌수와 족보
>
> **LCA는 "두 사람의 가장 가까운 공통 조상"** 이다. 사촌 두 명의 LCA는 **할아버지**이고, 형제 두 명의 LCA는 **아버지**다. 부모와 자식의 LCA는 **부모 자신**이다. 그리고 **촌수를 세는 방식**이 곧 트리 거리 공식이다.
> ```
>   나 -> 공통 조상까지 올라간 세대 수  +  공통 조상 -> 상대까지 내려간 세대 수
>   = (depth[u] - depth[LCA]) + (depth[v] - depth[LCA])
>   = depth[u] + depth[v] - 2·depth[LCA]
> ```
> **이 공식이 오늘 배우는 것의 실용적 절반**이다. 트리에서 "두 노드 사이 거리"를 물으면 BFS를 돌릴 필요가 없다 — LCA 하나만 알면 산수다.
>
> ---
>
> ### 비유 2 — 지하철 환승과 "꺾이는 점"
>
> 노선도가 **나무 모양**(순환 없음)일 때, 두 역 사이 경로는 **하나뿐**이고 반드시 **어딘가에서 방향을 바꾼다**. 그 꺾이는 역이 LCA다.
> ```
>   u 에서 v 로 가는 유일한 경로:
>
>        LCA
>       /   \
>      /     \        위로 올라갔다가(u -> LCA)
>     u       v       아래로 내려간다(LCA -> v)
>
>   "트리에서 두 점 사이 경로는 항상 U 자 모양(위로, 그다음 아래로)이다."
> ```
> **이 관찰이 LCA를 "트리 경로 문제의 좌표계"로 만든다.** 경로 위의 가중치 합을 묻는다면, 루트에서 각 노드까지의 누적 합 `S[v]`를 미리 구해 두고
> $$ \text{path}(u, v) = S[u] + S[v] - 2 \cdot S[\text{LCA}(u,v)] $$
> 로 `O(1)`에 답한다 — **[[day-14-prefix-sum/concept|누적 합(Day 14)]]을 직선이 아니라 트리에 적용한 것**이다. 거리 공식은 여기서 모든 간선 가중치를 1로 둔 특수 경우일 뿐이다.
>
> ---
>
> ### 왜 방법이 다섯 가지나 되는가 — 질의 횟수가 도구를 결정한다
>
> LCA는 **"똑같은 질문에 대한 답이 여러 개인 대표적인 주제"** 다. 이유는 단순하다: **전처리 비용과 질의 비용의 트레이드오프**가 문제마다 다르기 때문이다.
>
> ```
>   질의 1번:            재귀 후위 순회        전처리 0,          질의 O(N)
>   질의 몇 번:          부모 타고 올라가기    전처리 O(N),       질의 O(h)
>   질의 10^5 번:        이진 상승             전처리 O(N log N), 질의 O(log N)   <- 표준
>   질의 10^6 번:        오일러 투어 + RMQ     전처리 O(N log N), 질의 O(1)
>   질의를 미리 다 안다: 타잔(오프라인)        전체 O((N+Q)·a(N))
> ```
>
> **코딩테스트 현실:** LeetCode의 트리 문제는 **대개 질의가 1회**라서 **재귀 한 방이 정답**이고, 이진 상승은 **`k`번째 조상을 여러 번 묻는 문제([#1483](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/))** 나 **가중치 트리 경로 질의**에서 등장한다. 그래서 오늘의 학습 순서는 **"재귀를 완벽히 이해한 뒤 이진 상승을 손에 익히는 것"** 이다.
>
> ---
>
> ### 재귀 해법의 직관 — "아래에서 위로 신호를 올려보낸다"
>
> #236의 6줄 코드는 처음 보면 마법 같지만, **"각 노드가 부모에게 보내는 보고서"** 로 읽으면 자명해진다.
> ```
>   각 노드는 부모에게 이렇게 보고한다:
>     - "내 서브트리에서 p 나 q 를 찾았다" -> 찾은 노드(또는 LCA)를 올려보낸다
>     - "아무것도 못 찾았다"              -> None 을 올려보낸다
>
>   그러면 어떤 노드에서:
>     왼쪽 보고 O, 오른쪽 보고 O  ->  p 와 q 가 서로 다른 가지에 있다
>                                     -> "여기가 갈라지는 지점" = 내가 LCA다!
>     왼쪽만 O                    ->  아직 둘 다 왼쪽 아래에 있다 -> 왼쪽 보고를 그대로 전달
>     오른쪽만 O                  ->  대칭
>     둘 다 X                     ->  None 전달
>
>   그리고 자기 자신이 p 나 q 면 즉시 자신을 올려보낸다
>   (자기 자신도 조상으로 세는 관례가 여기서 정확히 반영된다)
> ```
> ```python
> def lowestCommonAncestor(self, root, p, q):
>     if root is None or root is p or root is q:
>         return root                      # 찾았으면 나를 올려보낸다
>     L = self.lowestCommonAncestor(root.left, p, q)
>     R = self.lowestCommonAncestor(root.right, p, q)
>     if L and R:
>         return root                      # 양쪽에서 왔다 -> 내가 갈라지는 지점
>     return L or R                        # 한쪽만 -> 그것을 그대로 전달
> ```
> **"양쪽에서 신호가 오면 내가 답"** — 이 한 줄이 전부다. **후위 순회(post-order)** 인 것이 본질이다: **자식의 답을 먼저 알아야 내 답을 정할 수 있다.** [[day-29-tree-traversal/concept|Day 29]]의 "후위 순회는 아래에서 위로 정보를 모은다"가 그대로 쓰인다.
>
> **⚠️ 이 코드의 숨은 가정:** **`p`와 `q`가 둘 다 트리에 존재한다.** 하나가 없으면 이 코드는 **"있는 쪽 하나"를 반환**해 버린다(#236 제약이 존재를 보장하므로 통과한다). 존재가 보장되지 않는 변형(LCA II)에서는 **"찾은 개수를 함께 세서 마지막에 2인지 확인"** 하는 처리가 추가로 필요하다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 방법 1 — 루트에서의 경로를 저장하고 공통 접두사를 찾기 (가장 원시적, 가장 이해하기 쉬움)**
> ```
>   1) 루트에서 u 까지의 경로, 루트에서 v 까지의 경로를 각각 리스트로 만든다
>   2) 두 리스트의 "공통 접두사(common prefix)" 의 마지막 원소가 LCA다
>
>   u = 8:  [1, 2, 5, 8]
>   v = 4:  [1, 2, 4]
>           ^^^^^^        공통 접두사 = [1, 2]  ->  LCA = 2
>
>   시간: 경로 찾기 O(N) + 비교 O(h)   ->  질의당 O(N)
>   공간: O(h)
> ```
> **이 방법의 가치는 "정답 기준선(baseline)"** 이다. 나중에 만드는 이진 상승·RMQ가 맞는지 **무작위 트리로 교차 검증**할 때 반드시 쓴다. 그리고 **#2096(경로 방향 문자열)** 처럼 **"경로 자체가 답인 문제"** 에서는 이 방법이 오히려 정답이다.
>
> ---
>
> **(B) 방법 2 — BST의 특권: 값 비교로 한 방향만 내려간다 `O(h)`**
>
> [[day-11-tree-basics/concept|이진 탐색 트리(BST)]]에서는 **모든 값이 정렬 순서를 지킨다**는 성질 하나로 탐색이 극적으로 단순해진다.
> ```
>   현재 노드 c 에서:
>     p.val < c.val  이고  q.val < c.val   ->  둘 다 왼쪽에 있다   ->  c = c.left
>     p.val > c.val  이고  q.val > c.val   ->  둘 다 오른쪽에 있다  ->  c = c.right
>     그 외 (값이 c 를 사이에 두고 갈라진다, 또는 c 가 p/q 중 하나)
>                                          ->  c 가 LCA다. 끝!
>
>          6
>        /   \
>       2     8
>      / \   / \
>     0   4 7   9
>        / \
>       3   5
>
>   LCA(2, 8):  6 에서 2 < 6 < 8  ->  갈라진다  ->  답 6
>   LCA(2, 4):  6 에서 둘 다 작다 -> 2 로 이동.  2 는 p 자신 -> 답 2
>   LCA(3, 5):  6 -> 2 -> 4.  4 에서 3 < 4 < 5 -> 답 4
> ```
> ```
>   "처음으로 두 값이 갈라지는 노드가 LCA다."
>
>   시간 O(h) (균형 BST면 O(log N), 한쪽으로 치우치면 O(N))
>   공간 O(1) (while 반복문으로 쓰면 재귀 스택조차 필요 없다)
> ```
> **왜 되는가:** LCA 아래로 내려가면 `p`와 `q`가 서로 다른 서브트리로 갈라지므로, **값이 현재 노드를 "사이에 두는" 첫 지점이 정확히 갈라지는 지점**이다. **BST 문제에서 정렬 성질을 쓰지 않으면 문제를 절반만 푼 것**이라는 감각을 여기서 익혀 두라.
>
> ---
>
> **(C) 방법 3 — 부모·깊이를 만들고 함께 올라가기 `O(h)` (이진 상승의 전 단계)**
>
> 먼저 **BFS나 반복문 DFS로 `parent[]`와 `depth[]`를 만든다**(파이썬에서는 재귀 대신 이것이 정석이다).
> ```
>   1단계: 깊이를 맞춘다 (깊은 쪽을 끌어올린다)
>       while depth[u] > depth[v]: u = parent[u]
>       while depth[v] > depth[u]: v = parent[v]
>
>   2단계: 같은 높이에서 함께 한 칸씩 올라간다
>       while u != v:  u, v = parent[u], parent[v]
>       return u
>
>   왜 2단계가 되는가:
>     같은 깊이의 두 노드가 만나는 첫 지점은 반드시 LCA다.
>     (더 아래에서 만날 수 없고, 루트에서는 반드시 만난다)
> ```
> ```
>              1
>            /   \
>           2     3
>          / \     \
>         4   5     6
>            / \
>           7   8
>
>   LCA(7, 6):  depth[7]=3, depth[6]=2
>     1단계: 7 을 한 칸 올려 5 (depth 2).  이제 (5, 6) 같은 깊이
>     2단계: (5,6) 다르다 -> (2,3) 다르다 -> (1,1) 같다!  ->  답 1
> ```
> **이것이 왜 부족한가:** **체인 모양 트리**(`1-2-3-...-100000`)에서는 `h = N`이라 **질의 하나가 `O(N)`** 이다. 질의가 `10^5`개면 `10^10` — 불가능하다. **한 칸씩 올라가는 것이 병목**이고, 이 병목을 **"한 번에 `2^k`칸 뛰어오르기"** 로 바꾸는 것이 다음 단계다.
>
> ---
>
> **(D) 방법 4 — 이진 상승(Binary Lifting): 오늘의 핵심 ⭐**
>
> **아이디어의 출발점은 [[day-41-bitmask/concept|비트(Day 41)]]다.** 어떤 자연수 `d`든 **2의 거듭제곱의 합**으로 유일하게 쓸 수 있다.
> ```
>   13 = 8 + 4 + 1 = 2^3 + 2^2 + 2^0  ->  이진수 1101
>
>   "13칸 올라가라" = "8칸 뛰고, 4칸 뛰고, 1칸 뛰어라"  ->  점프 3번!
>   한 칸씩 13번 대신 3번.  일반적으로 d 칸을 popcount(d) <= log d 번에 해결한다.
> ```
> **그러려면 "`2^k`칸 위 조상"을 미리 알아야 한다.** 그것이 표 `up[k][v]`다.
> ```
>   up[k][v] = v 의 2^k 번째 조상  (없으면 -1)
>
>   점화식 (DP!):
>       up[0][v] = parent[v]                        <- 기저: 1칸 = 직접 부모
>       up[k][v] = up[k-1][ up[k-1][v] ]            <- 2^k = 2^(k-1) 두 번
>
>   "2^k 칸 = 2^(k-1) 칸 뛰고 또 2^(k-1) 칸 뛰기"  <- 이 한 줄이 전부다
>
>   +----------------------------------------------------------+
>   |  이것은 트리 위의 DP다 (Day 31).                          |
>   |  상태: (k, v),  전이: up[k][v] = up[k-1][up[k-1][v]]     |
>   |  거듭제곱 빠른 계산(pow(a, b))의 "반복 제곱"과 같은 구조다 |
>   +----------------------------------------------------------+
> ```
> ```
>   예:  체인  0 - 1 - 2 - 3 - 4 - 5 - 6 - 7   (0 이 루트, parent[i] = i-1)
>
>   up[0]:  [-1, 0, 1, 2, 3, 4, 5, 6]        1칸 위
>   up[1]:  [-1,-1, 0, 1, 2, 3, 4, 5]        2칸 위  (up[0][up[0][v]])
>   up[2]:  [-1,-1,-1,-1, 0, 1, 2, 3]        4칸 위
>
>   노드 7 에서 5칸 위 = 4 + 1 = up[0][ up[2][7] ] = up[0][3] = 2.  점프 2번!
> ```
>
> **질의 알고리즘 — 두 단계로 나뉜다.**
> ```
>   lca(u, v):
>     [1단계] 깊이 맞추기 - 깊이 차 d 를 이진수로 분해해 점프
>         if depth[u] < depth[v]: u, v = v, u        # u 를 항상 깊은 쪽으로
>         d = depth[u] - depth[v]
>         k = 0
>         while d:
>             if d & 1: u = up[k][u]                 # 이 비트가 켜졌으면 2^k 점프
>             d >>= 1
>             k += 1
>         if u == v: return u                        # v 가 u 의 조상이었다!
>
>     [2단계] 함께 "LCA 직전까지" 최대한 올라가기
>         for k in range(LOG-1, -1, -1):             # 큰 점프부터!
>             if up[k][u] != up[k][v]:               # 아직 갈라져 있으면
>                 u, v = up[k][u], up[k][v]          # 둘 다 2^k 점프
>         return up[0][u]                            # 지금 u,v 는 LCA 의 자식 -> 부모가 답
> ```
> ```
>   2단계가 왜 "다를 때만 올라가는가" — 오늘 가장 헷갈리는 부분이다
>
>     up[k][u] == up[k][v] 이면  ->  2^k 칸 위에서 이미 만났다
>                                    = LCA 를 지나쳤거나 딱 도달했다
>                                    -> 올라가면 안 된다 (지나치면 답을 잃는다)
>     up[k][u] != up[k][v] 이면  ->  아직 LCA 아래다  ->  안전하게 올라간다
>
>   큰 k 부터 내려가며 "안전한 만큼만" 올라가면, 루프가 끝났을 때
>   u 와 v 는 "LCA 의 바로 아래 자식"에 정확히 멈춘다.  그래서 답은 up[0][u].
>
>   +-- 이분 탐색과 같은 사고다 (Day 18) --------------------------+
>   |  "조건을 깨지 않는 최대 거리"를 큰 보폭부터 시도해 확정한다  |
>   |  = 상한을 넘지 않으면서 최대한 전진하는 그리디 + 이진 분해    |
>   +--------------------------------------------------------------+
> ```
> ```
>   왜 마지막에 return up[0][u] 이고 u 가 아닌가:
>     루프에서 우리는 "아직 다른(=LCA 미달)" 상태만 유지했으므로
>     끝났을 때 u != v 이고, 한 칸만 더 올리면 만난다. 즉 up[0][u] == up[0][v] == LCA.
>     실수로 return u 를 쓰면 "LCA 의 자식"을 반환한다 - 최다 버그 중 하나.
>
>   1단계 후 u == v 검사를 빼먹으면:
>     v 가 u 의 조상인 경우(예: LCA(8,5)=5) 2단계에서 up[k][u] != up[k][v] 가
>     계속 참이 되어 엉뚱한 값이 나온다. 이 검사는 필수다.
> ```
> ```
>   LOG 의 크기:  2^LOG > N 이어야 한다.  LOG = N.bit_length() 로 잡으면 안전하다.
>                 N = 10^5 -> LOG = 17.   N = 10^6 -> LOG = 20.
>
>   전처리 시간 O(N log N),  공간 O(N log N),  질의 O(log N)
>   N = 10^5, LOG = 17 이면 표 크기 1.7·10^6 - 파이썬에서도 충분히 감당된다
> ```
>
> **부수 효과가 크다: `k`번째 조상 질의가 공짜다.** 같은 표로 **`k`번째 조상**을 `O(log k)`에 답한다 — 그것이 [#1483](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/)의 정답이고, **"LCA를 배우면 조상 관련 질의 전부가 따라온다"** 는 뜻이다.
>
> ---
>
> **(E) 방법 5 — 오일러 투어 + 희소 배열: LCA를 배열의 RMQ로 환원 `O(1)` 질의**
>
> **트리 문제를 배열 문제로 바꾸는 것**이 이 방법의 사상이다.
> ```
>   오일러 투어(Euler tour):  DFS 로 트리를 돌면서 "방문할 때마다" 노드를 기록한다.
>                            자식에서 돌아올 때 부모를 다시 기록하는 것이 핵심!
>                            길이는 정확히 2N - 1.
>
>              1
>            /   \
>           2     3
>          / \
>         4   5
>
>   euler:  1  2  4  2  5  2  1  3  1
>   depth:  0  1  2  1  2  1  0  1  0
>   first:  1->0,  2->1,  3->7,  4->2,  5->4     (각 노드의 첫 등장 위치)
> ```
> ```
>   핵심 정리:  LCA(u, v) = euler 배열의 구간 [first[u], first[v]] 에서
>                          depth 가 최소인 노드
>
>   왜?  u 를 처음 방문한 시점과 v 를 처음 방문한 시점 사이에
>        DFS 는 반드시 "u 와 v 를 모두 감싸는 가장 깊은 조상"을 통과한다.
>        그리고 그 구간에서 LCA 보다 얕은 노드는 절대 등장하지 않는다
>        (LCA 의 서브트리를 벗어나지 않으므로).
>        따라서 구간의 최소 깊이 = LCA 의 깊이, 그 노드가 LCA다.
>
>   LCA(4, 5):  first[4]=2, first[5]=4  ->  euler[2..4] = [4, 2, 5]
>               depth        = [2, 1, 2]  ->  최소는 노드 2  ->  LCA = 2  O
>   LCA(4, 3):  first[4]=2, first[3]=7  ->  euler[2..7] = [4,2,5,2,1,3]
>               depth        = [2,1,2,1,0,1] ->  최소 깊이 0 -> 노드 1  ->  LCA = 1  O
> ```
> ```
>   이제 "구간 최솟값 질의(RMQ, Range Minimum Query)" 문제가 되었다.
>
>     세그먼트 트리 (Day 40):     전처리 O(M), 질의 O(log M)   - 갱신도 되지만 여기선 불필요
>     희소 배열 (sparse table):   전처리 O(M log M), 질의 O(1)  <- 정적이므로 이게 최적
>
>   희소 배열:  table[k][i] = 구간 [i, i + 2^k) 의 최솟값(의 위치)
>       table[k][i] = min( table[k-1][i],  table[k-1][i + 2^(k-1)] )
>
>       질의 [l, r]:  k = (r - l + 1).bit_length() - 1
>                     겹치는 두 블록 [l, l+2^k) 와 (r-2^k, r] 의 min
>                     -> min 은 겹쳐도 되므로(idempotent) O(1)!
>
>       +-- 왜 겹쳐도 되는가 -----------------------------------------+
>       |  min(a, a) = a 이다(멱등, idempotent).                     |
>       |  그래서 두 블록이 겹쳐도 답이 안 변한다.                    |
>       |  합(sum)은 멱등이 아니라 이 트릭을 못 쓴다 - 세그먼트 트리행 |
>       +------------------------------------------------------------+
> ```
> **참고: `O(N)` 전처리 + `O(1)` 질의도 가능하다**(Farach-Colton–Bender: 인접 깊이 차가 ±1인 성질을 이용한 블록 분해). 이론적으로 아름답지만 **코딩테스트에서 쓸 일은 거의 없다** — 이진 상승으로 충분하다.
>
> ---
>
> **(F) 방법 6 — 타잔 오프라인 LCA: Union-Find 하나로 거의 선형**
>
> **질의를 미리 전부 알고 있을 때(오프라인, offline)** 쓸 수 있다.
> ```
>   DFS 로 트리를 한 번 훑으면서:
>     1) 노드 v 에 진입하면 visited[v] = True,  ancestor[find(v)] = v
>     2) v 의 모든 자식을 처리하고, 자식이 끝날 때마다 union(child, v)
>        그리고 ancestor[find(v)] = v 로 갱신
>     3) v 의 처리가 끝나면, v 가 연관된 질의 (v, w) 를 확인한다:
>          w 가 이미 visited 이면  ->  LCA(v, w) = ancestor[find(w)]
>
>   직관:  "v 를 다 끝낸 시점에, 이미 방문한 노드 w 는
>           자기가 속한 '아직 안 끝난 조상' 아래로 묶여 있다.
>           그 조상이 곧 갈라지는 지점 = LCA다."
>
>   시간 O((N + Q)·a(N))  (a = 아커만 역함수, 사실상 상수)   -> Day 36 그대로
>   공간 O(N + Q)
> ```
> **왜 알아 두는가:** [[day-36-union-find/concept|Union-Find(Day 36)]]가 **"묶기"라는 도구로 트리 구조 질의까지 해결한다**는 것을 보여주는 대표 예다. 다만 **온라인 질의(질의가 하나씩 들어오는 상황)에는 쓸 수 없다**는 명확한 한계가 있고, 파이썬에서는 재귀 깊이 문제까지 얹혀 실전 채택률이 낮다.
>
> ---
>
> **(G) LCA의 응용 — 이것이 오늘 배우는 진짜 이유**
> ```
>   [1] 두 노드 사이 거리 (간선 수)
>       dist(u, v) = depth[u] + depth[v] - 2·depth[LCA(u,v)]
>
>   [2] 가중치 트리의 경로 합
>       S[v] = 루트에서 v 까지 가중치 합 (DFS 로 미리 계산)
>       path_sum(u, v) = S[u] + S[v] - 2·S[LCA(u,v)]
>       -> 트리 위의 누적 합 (Day 14 의 트리 버전)
>
>   [3] u 에서 v 로 가는 경로의 k 번째 노드
>       L = LCA(u,v),  d1 = depth[u]-depth[L]
>       k <= d1 이면  u 의 k 번째 조상
>       그렇지 않으면 v 의 (dist - k) 번째 조상        <- 이진 상승이 그대로 필요
>
>   [4] 노드 w 가 u-v 경로 위에 있는가?
>       dist(u,w) + dist(w,v) == dist(u,v)             <- 삼각 등식
>
>   [5] 경로의 최댓값/최솟값/XOR
>       up[k][v] 와 함께 maxw[k][v] (2^k 구간의 최대 가중치)를 같이 올려 둔다
>       -> 점프할 때 값도 합성한다.  MST 검증·대체 간선 문제의 핵심 기법
>
>   [6] u-v 경로에 +x 더하기 (오프라인 일괄 갱신)
>       diff[u] += x, diff[v] += x, diff[L] -= x, diff[parent[L]] -= x
>       -> 마지막에 서브트리 합을 한 번 굴린다 (트리 차분 배열)
> ```
>
> ---
>
> **(H) ⚠️ 파이썬 실전 최대 함정 — 재귀 깊이**
> ```
>   기본 재귀 한도:  sys.getrecursionlimit() == 1000
>
>   노드 10^5 개의 "체인" 트리 (1-2-3-...-100000) 에서 재귀 DFS:
>       -> RecursionError: maximum recursion depth exceeded
>
>   흔한 처방과 그 한계:
>     sys.setrecursionlimit(10**6)     <- 파이썬은 늘어나지만 C 스택이 터져 죽을 수 있다
>     threading.stack_size(...) + Thread 로 우회  <- 동작하지만 번거롭고 환경 의존
>
>   정석: 반복문으로 짜라.
>     parent/depth 는 BFS(deque) 로 만드는 것이 가장 짧고 안전하다.
>     후위 순회가 필요하면 BFS 순서를 뒤집어서 쓴다 (자식이 먼저 처리된다!)
> ```
> ```python
> from collections import deque
>
> def root_tree(adj, root=0):
>     """BFS 로 parent, depth, 방문 순서를 만든다. 재귀 없음 = 깊이 무제한."""
>     n = len(adj)
>     parent = [-1] * n
>     depth = [0] * n
>     order = [root]                       # BFS 순서 (부모가 자식보다 항상 앞)
>     visited = [False] * n
>     visited[root] = True
>     dq = deque([root])
>     while dq:
>         v = dq.popleft()
>         for w in adj[v]:
>             if not visited[w]:
>                 visited[w] = True
>                 parent[w] = v
>                 depth[w] = depth[v] + 1
>                 order.append(w)
>                 dq.append(w)
>     return parent, depth, order
>
> # 트리 DP(서브트리 집계)가 필요하면 reversed(order) 로 순회한다
> # -> 자식이 부모보다 먼저 처리되므로 후위 순회와 같은 효과. 재귀 0.
> ```
> **`reversed(order)` 트릭은 오늘 이후 계속 쓴다.** 트리 DP·서브트리 크기·부분합을 **재귀 없이** 계산하는 표준 관용구다.
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. **N** = 노드 수, **Q** = 질의 수, **h** = 트리 높이, **LOG** = `⌈log₂N⌉`.
>
> | 방법 | 전처리 시간 | 전처리 공간 | 질의당 시간 | 온라인? | 비고 |
> |---|---|---|---|---|---|
> | 루트 경로 비교 | 0 | O(h) | **O(N)** | O | 가장 단순. **검증 기준선** |
> | BST 값 비교 | 0 | O(1) | **O(h)** | O | BST 전용. 반복문이면 공간 `O(1)` |
> | 재귀 후위 순회 (#236) | 0 | O(h) 스택 | **O(N)** | O | **질의 1회면 이게 정답** ✅ |
> | 부모 타고 한 칸씩 | O(N) | O(N) | **O(h)** | O | 체인이면 `O(N)` ⚠️ |
> | **이진 상승** | **O(N log N)** | **O(N log N)** | **O(log N)** ✅ | O | **실전 표준** ⭐ |
> | 오일러 투어 + 희소 배열 | O(N log N) | O(N log N) | **O(1)** ✅ | O | 질의가 극단적으로 많을 때 |
> | 오일러 투어 + 세그먼트 트리 | O(N) | O(N) | O(log N) | O | 갱신이 필요하면 |
> | 타잔 (오프라인) | — | O(N+Q) | 전체 **O((N+Q)·α(N))** | **X** ❌ | Union-Find. 질의를 미리 알아야 |
> | Farach-Colton–Bender | O(N) | O(N) | O(1) | O | 이론 최적. 실전 과잉 |
>
> > **"이진 상승 vs 한 칸씩"의 실전 감각 — 트리 모양이 승부를 가른다.**
> >
> > | 트리 모양 (N = 10⁵) | h | 한 칸씩 (Q = 10⁵) | 이진 상승 (Q = 10⁵) |
> > |---|---|---|---|
> > | 완전 이진 트리 | ~17 | 1.7×10⁶ (**충분히 빠름**) | 1.7×10⁶ (비슷) |
> > | 랜덤 트리 | ~수십 | ~10⁶ (괜찮음) | ~10⁶ (비슷) |
> > | **체인(일자)** | **10⁵** | **10¹⁰** ❌ | **1.7×10⁶** ✅ |
> >
> > **균형 트리에서는 두 방법의 차이가 거의 없다.** 이진 상승이 이기는 것은 **최악(체인)** 이고, 코딩테스트는 **최악을 반드시 넣는다.** "랜덤 트리에서 잘 되니까 괜찮다"는 판단이 오답의 흔한 출발점이다. **제약에 `N, Q ≤ 10⁵`이 함께 있으면 즉시 이진 상승**을 꺼내라. (표의 수치는 자릿수 감각이며, 실측은 `examples.py`의 벤치마크 섹션에서 직접 확인하라.)
>
> > **전처리 공간이 실제로 얼마인가 — 파이썬은 리스트 오버헤드가 크다.**
> >
> > | N | LOG | `up` 표 원소 수 | 파이썬 `list[int]` 개략 메모리 |
> > |---|---|---|---|
> > | 10⁴ | 14 | 1.4×10⁵ | ~1 MB |
> > | 10⁵ | 17 | 1.7×10⁶ | ~14 MB |
> > | 10⁶ | 20 | 2×10⁷ | ~160 MB ⚠️ |
> >
> > `N = 10⁶`이면 **메모리 제한(보통 256 MB)에 위험하게 근접**한다. 처방: **① `LOG`를 `N.bit_length()`로 딱 맞게 계산**(넉넉하게 `20`으로 고정하지 말 것), **② `array` 모듈이나 1차원 평탄화(`up[k*n + v]`) 사용**, **③ 질의가 적으면 아예 이진 상승을 포기하고 `O(h)` 방법**. 다행히 LeetCode·프로그래머스에서 `N = 10⁶` 트리는 드물다.
>
> > **`O(Q·N)`이 실제로 얼마나 위험한가.**
> >
> > | N = Q | Q·N | 파이썬 판정 |
> > |---|---|---|
> > | 10³ | 10⁶ | 여유 |
> > | 10⁴ | 10⁸ | **위험** (수십 초) |
> > | 10⁵ | 10¹⁰ | ❌ 불가능 |
> >
> > **재귀 해법(`O(N)`/질의)을 루프 안에서 부르는 것**이 이 주제의 최다 TLE 패턴이다. #236은 질의가 1회라 괜찮지만, **"여러 쌍의 LCA를 구하라"로 바뀌는 순간 전처리형으로 갈아타야** 한다.
>
> **재귀 깊이는 복잡도가 아니라 "동작 여부"의 문제다.** 이진 상승은 전처리·질의 모두 **반복문으로 짤 수 있다** — 그래서 파이썬에서 특히 안전하다. 반면 재귀 후위 순회는 `h`가 `10^5`면 **복잡도와 무관하게 `RecursionError`로 죽는다.** [[day-22-recursion/concept|Day 22]]의 "파이썬에서 깊은 재귀는 알고리즘이 아니라 환경 문제"라는 교훈이 오늘 가장 크게 작동한다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **암기 문장 셋.** **"트리의 모든 경로는 LCA에서 꺾인다."** / **"`dist = depth[u] + depth[v] - 2·depth[LCA]`"** / **"`up[k][v] = up[k-1][up[k-1][v]]`"**. 이 세 줄이면 오늘의 90%가 복원된다.
> - **#236의 6줄을 "보고서 비유"로 외워라.** **"양쪽에서 신호가 오면 내가 답, 한쪽만 오면 그걸 전달"**. 코드를 외우는 게 아니라 **각 노드가 부모에게 무엇을 보고하는지**를 외우면 변형 문제(#1123, #2096)에서도 즉시 응용된다.
> - **BST면 반드시 값 비교를 써라.** #235에 #236 해법을 쓰면 통과는 하지만 **`O(N)` vs `O(h)`** 로 손해다. **"BST 문제에서 정렬 성질을 안 쓰면 절반만 푼 것"** — 면접에서 특히 감점 포인트다.
> - **이진 상승의 2단계는 "큰 점프부터"** 다. `range(LOG-1, -1, -1)`. 작은 것부터 하면 **지나쳐 버린다**. 그리고 **`up[k][u] != up[k][v]`(다를 때만) 올라간다** — 같으면 이미 LCA를 지났다는 신호다. 이 두 가지가 이진 상승 버그의 90%다.
> - **마지막 줄은 `return up[0][u]`** 다. `return u`가 아니다. 루프가 끝난 시점에 `u`, `v`는 **LCA의 자식**에 멈춰 있다. **"자식까지만 올라가고, 마지막 한 칸은 손으로"** 라고 외우라.
> - **`-1`(루트의 부모)을 어떻게 다룰지 정하고 일관되게 지켜라.** 두 방식이 있다: **① `-1`로 두고 매번 검사**, **② 가상 노드 `n`을 만들어 루트의 부모로 삼고 `up[k][n] = n`(자기 루프)**. **②가 코드가 훨씬 깔끔**하다 — 경계 검사가 사라지기 때문이다. 다만 반환값이 `n`인지 확인하는 처리는 남는다.
> - **`LOG`는 `n.bit_length()`로 계산하라.** `20`으로 고정하면 작은 트리에서 메모리·시간을 낭비하고, `N`이 크면 부족해진다. `LOG = max(1, n.bit_length())`가 안전한 관용구다.
> - **파이썬 재귀는 트리 문제의 1번 사인(死因)이다.** LeetCode의 트리 문제는 `N ≤ 10^5`이면서 **"체인 모양"** 테스트가 실재한다. **`parent`·`depth`는 BFS로 만들고, 후위 순회가 필요하면 `reversed(BFS 순서)`** 를 쓰라 — 재귀 0줄로 같은 효과다.
> - **오일러 투어의 길이는 `2N-1`** 이다. 외워 두면 배열 크기 실수를 막는다. 그리고 **"자식에서 돌아올 때 부모를 다시 기록"** 하는 것이 이 투어의 전부다. 기록을 빼먹으면 RMQ 정리가 깨진다.
> - **희소 배열의 `min` 트릭은 "겹쳐도 되기 때문"에 성립한다.** `min(a, a) = a`(멱등)이라 두 블록이 겹쳐도 답이 같다. **합(sum)에는 못 쓴다** — 그건 [[day-40-segment-tree/concept|세그먼트 트리(Day 40)]] 담당이다. 이 구분을 아는 것이 "언제 어떤 자료구조인가"의 핵심이다. ([이진 상승 입문 — LeetCode 토론](https://leetcode.com/discuss/post/4299594/binary-lifting-technique-a-beginners-gui-k7p0/))
> - **이진 상승은 LCA 전용이 아니다.** `k`번째 조상([#1483](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/)), **함수형 그래프에서 `k`번 적용 후 위치**(순열 사이클·"토끼가 `k`번 점프"), **희소 표에 최댓값·합을 같이 올려 경로 집계** 등에 그대로 쓰인다. **"`2^k` 단위로 미리 합성해 두고 이진 분해로 조합한다"** 는 패턴 자체를 익혀라 — 행렬 거듭제곱·`pow(a,b,m)`과 같은 사고다. ([이진 상승으로 k번째 조상 구하기 — 스터디 가이드](https://leetcode.com/discuss/study-guide/4139774/Binary-Lifting-to-compute-Kth-ancestors-in-fastest-time/))
> - **#2096은 "LCA를 명시적으로 구하지 않고 푸는" 좋은 예다.** 루트에서 `start`·`dest`까지의 **경로 문자열**을 각각 구해 **공통 접두사를 잘라내면** 남은 것이 답이다(`'U' × 남은 start 길이 + 남은 dest 경로`). **"공통 접두사를 자르는 것"이 곧 LCA를 지나치는 것** 이라는 통찰이 예쁘다.
> - **#1123은 "LCA를 몰라도 되는 LCA 문제"** 다. 각 노드가 **(서브트리 높이, 그 서브트리 안 최심 잎들의 LCA)** 를 함께 반환하게 하면, **왼쪽 높이 == 오른쪽 높이면 자신이 답**이고 아니면 **높은 쪽의 답을 그대로 올린다**. **"한 번의 DFS로 두 값을 동시에 올려보낸다"** 는 트리 DP의 기본 형태이며 [[day-31-dp/concept|Day 31]]과 이어진다.
> - **그래프에서의 "LCA 사고"도 있다.** [합승 택시 요금(프로그래머스 #72413)](https://school.programmers.co.kr/learn/courses/30/lessons/72413)은 **"함께 가다가 갈라지는 지점 `c`"** 를 **모든 정점에 대해 시도**하고 `d[s][c] + d[c][a] + d[c][b]`의 최솟값을 찾는다. 트리가 아니어서 LCA를 쓸 수 없으니 [[day-35-bellman-floyd/concept|플로이드-워셜(Day 35)]]로 모든 쌍 거리를 구해 **"분기점 전수 조사"** 로 대체하는 것이다. **"트리면 LCA, 일반 그래프면 분기점 완전 탐색 + 전체 최단 거리"** 라는 대응 관계를 기억하라.
> - **경계 케이스 셋을 항상 테스트하라.** **① `u == v`**(답은 자기 자신), **② 한쪽이 다른 쪽의 조상**(답은 그 조상), **③ 루트가 답인 경우**. 이 셋이 LCA 구현 검증의 최소 세트다.
> - **무작위 트리로 교차 검증하는 습관을 들여라.** `parent[i] = randint(0, i-1)`로 랜덤 트리를 만들면 **항상 유효한 트리**가 나온다(사이클 불가). 그 위에서 **경로 비교 나이브와 이진 상승의 결과를 모든 쌍에 대해 대조**하면 구현 확신이 생긴다 — [[day-42-string-matching/concept|Day 42]]에서 KMP를 `find`와 대조한 것과 같은 방식이다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **"조상"에는 자기 자신이 포함된다 — 문제마다 확인하라.** LeetCode #235/#236은 포함(`LCA(5, 8) = 5`, 5가 8의 조상일 때). 이 관례를 반대로 가정하면 **"한쪽이 다른 쪽의 조상"인 모든 케이스가 틀린다.** 이 주제 최다 오답 유형이다.
> 2. **"lowest"는 값이 아니라 깊이다.** 트리에서 아래쪽(깊은 쪽)이 `lowest`다. 루트는 항상 공통 조상이지만 가장 얕아서 답이 아니다. 용어에 속지 마라.
> 3. **#236의 6줄 해법은 "`p`, `q`가 둘 다 존재"를 가정한다.** 하나가 없으면 **있는 쪽 하나를 반환**해 조용히 틀린다. 존재가 보장되지 않는 변형에서는 **찾은 개수를 세서 2인지 확인**하는 처리를 반드시 추가하라.
> 4. **이진 상승 2단계는 반드시 큰 `k`부터.** `for k in range(LOG-1, -1, -1)`. 작은 것부터 올라가면 **LCA를 지나쳐** 엉뚱한 답이 나온다. 그리고 **`up[k][u] != up[k][v]`일 때만** 올라가라 — 같으면 이미 LCA 위쪽이다.
> 5. **1단계 후 `if u == v: return u` 검사를 절대 빼먹지 마라.** `v`가 `u`의 조상인 경우가 여기서 걸러진다. 이 검사가 없으면 2단계가 정상 동작하지 않는다.
> 6. **마지막은 `up[0][u]`.** 2단계 루프가 끝났을 때 `u`, `v`는 **LCA의 자식**이다. `return u`로 쓰면 **한 칸 아래를 반환**한다.
> 7. **깊이 차 점프에서 `-1`(범위 밖)을 밟지 않도록 하라.** `depth`를 정확히 맞춘 뒤에만 점프하면 이론상 `-1`이 나오지 않지만, `depth` 계산 버그가 있으면 조용히 `-1`을 타고 인덱스가 깨진다. **가상 루트 부모(자기 루프)를 쓰면 이 클래스의 버그가 사라진다.**
> 8. **파이썬 재귀 한도 1000은 트리 문제에서 반드시 문제가 된다.** `N ≤ 10^5`인 트리 문제에서 **체인 입력이 실제로 나온다.** `sys.setrecursionlimit(10**6)`은 **C 스택 오버플로로 프로세스가 죽을 수 있는** 임시방편이다. **정석은 BFS/반복 DFS**이며, 후위 순회는 **`reversed(BFS 순서)`** 로 대체한다.
> 9. **LCA는 "루트가 정해진 트리"에서만 정의된다.** 루트를 바꾸면 LCA도 바뀐다. 무향 트리가 주어지면 **먼저 루트를 정해 `parent`·`depth`를 만드는 것이 0단계**다. 문제가 루트를 지정하지 않으면 아무 노드나(보통 0 또는 1) 루트로 잡아도 되지만, **"경로"를 묻는 문제라면 루트 선택이 답에 영향을 주지 않는지 확인**하라(거리는 영향 없음, "조상 관계"는 영향 있음).
> 10. **1-based / 0-based 인덱스를 섞지 마라.** 프로그래머스 문제는 노드 번호가 **1부터** 시작하는 경우가 많고, LeetCode는 0부터가 흔하다. **입력을 읽는 즉시 한쪽으로 통일**하고, 배열 크기를 `n+1`로 잡을지 `n`으로 잡을지 정해 두라. 오프바이원(off-by-one)이 LCA 코드에서 특히 잡기 어렵다.
> 11. **`depth[u] + depth[v] - 2·depth[LCA]`는 "간선 수" 거리다.** 노드 수 거리를 원하면 `+1`을 하라. 가중치 트리라면 `depth` 대신 **루트까지의 가중치 합 `S[]`** 를 쓴다. **"무엇을 세는지"를 명확히 하지 않으면 1씩 틀린다.**
> 12. **오일러 투어 배열 크기는 `2N-1`** 이다. `N`으로 잡으면 인덱스 에러, `2N`으로 잡으면 안전하지만 낭비다. 그리고 **`first[v]`(첫 등장 위치)** 를 반드시 기록하라 — 질의 구간의 양 끝이 그것이다.
> 13. **희소 배열은 정적(static) 데이터 전용이다.** 값이 바뀌면 전부 다시 만들어야 한다. **갱신이 있으면 [[day-40-segment-tree/concept|세그먼트 트리(Day 40)]]** 로 가라. 또한 **`min`/`max`/`gcd`처럼 멱등한 연산에만** 겹치는 블록 트릭이 성립한다 — **합에는 못 쓴다.**
> 14. **타잔 LCA는 오프라인 전용이다.** 질의가 하나씩 들어오는 상황(온라인)에서는 쓸 수 없다. 면접에서 "질의를 미리 알 수 있나요?"를 먼저 묻는 것이 좋은 신호다.
> 15. **메모리 한계를 계산하라.** `up` 표는 `N × LOG` 정수다. `N = 10^6`, `LOG = 20`이면 **2천만 개** — 파이썬 리스트로는 위험하다. **`LOG`를 `bit_length`로 딱 맞추고, 필요하면 1차원 평탄화(`up[k*n + v]`)나 `array('i', ...)`** 를 쓰라.
> 16. **실무에서의 LCA.** **Git의 `merge-base`** 가 정확히 LCA다(커밋 DAG의 공통 조상 — 트리가 아니라 DAG여서 더 복잡하다). **파일 시스템의 공통 상위 디렉터리**, **DOM 트리에서 두 요소의 공통 조상 컨테이너**(`Range.commonAncestorContainer`), **조직도의 공통 상급자**, **분류 체계(taxonomy)에서 두 개념의 최소 상위 개념**, **패키지 의존성 트리에서 공통 상위 의존성**. **"계층 구조가 있는 곳에는 반드시 LCA 질문이 있다."**
> 17. **LCA는 상위 개념의 입구다.** **HLD(Heavy-Light Decomposition)** 와 **오일러 투어 + 세그먼트 트리**는 **경로 갱신·경로 질의**를 `O(log²N)`에 해내며, 그 골격에 LCA가 들어간다. **트리 차분 배열**, **가상 트리(virtual tree)**, **오프라인 트리 질의(DSU on tree)** 도 모두 LCA를 전제한다. **오늘의 이진 상승 표는 트리 고급 기법 전체의 입장권**이다.

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import deque
>
> # ---- (1) 무향 트리에 루트를 정해 parent/depth/BFS순서 만들기 (재귀 없음!) ----
> def root_tree(adj, root=0):
>     n = len(adj)
>     parent = [-1] * n
>     depth = [0] * n
>     visited = [False] * n
>     visited[root] = True
>     order = [root]                       # BFS 순서: 부모가 항상 자식보다 앞
>     dq = deque([root])
>     while dq:
>         v = dq.popleft()
>         for w in adj[v]:
>             if not visited[w]:
>                 visited[w] = True
>                 parent[w] = v
>                 depth[w] = depth[v] + 1
>                 order.append(w)
>                 dq.append(w)
>     return parent, depth, order
>
>
> # ---- (2) 나이브: 루트 경로의 공통 접두사 - O(N)/질의. 검증 기준선 ----
> def lca_naive(parent, u, v):
>     def path(x):
>         p = []
>         while x != -1:
>             p.append(x)
>             x = parent[x]
>         return p[::-1]                   # 루트 -> x 순서
>     pu, pv = path(u), path(v)
>     res = -1
>     for a, b in zip(pu, pv):
>         if a != b:
>             break
>         res = a                          # 공통 접두사의 마지막
>     return res
>
>
> # ---- (3) 한 칸씩 올라가기 - O(h)/질의. 체인이면 O(N) ----
> def lca_climb(parent, depth, u, v):
>     while depth[u] > depth[v]:
>         u = parent[u]
>     while depth[v] > depth[u]:
>         v = parent[v]
>     while u != v:                        # 같은 깊이에서 함께 올라간다
>         u, v = parent[u], parent[v]
>     return u
>
>
> # ---- (4) 이진 상승 - 오늘의 핵심. 전처리 O(N log N), 질의 O(log N) ----
> class BinaryLiftingLCA:
>     def __init__(self, adj, root=0):
>         n = len(adj)
>         self.n = n
>         self.parent, self.depth, _ = root_tree(adj, root)
>         self.LOG = max(1, n.bit_length())        # 2^LOG > n 보장. 고정 20 금지!
>         self.up = [[-1] * n for _ in range(self.LOG)]
>         self.up[0] = self.parent[:]              # 기저: 1칸 위 = 직접 부모
>         for k in range(1, self.LOG):
>             prev, cur = self.up[k - 1], self.up[k]
>             for v in range(n):
>                 mid = prev[v]
>                 cur[v] = prev[mid] if mid != -1 else -1   # 2^k = 2^(k-1) 두 번
>
>     def kth_ancestor(self, v, k):
>         """v 의 k 번째 조상. 없으면 -1. O(log k)"""
>         i = 0
>         while k and v != -1:
>             if k & 1:
>                 v = self.up[i][v]                # 이 비트가 켜졌으면 2^i 점프
>             k >>= 1
>             i += 1
>         return v
>
>     def lca(self, u, v):
>         depth, up = self.depth, self.up
>         # [1단계] 깊은 쪽을 끌어올려 깊이를 맞춘다
>         if depth[u] < depth[v]:
>             u, v = v, u
>         u = self.kth_ancestor(u, depth[u] - depth[v])
>         if u == v:                               # v 가 u 의 조상이었다. 필수 검사!
>             return u
>         # [2단계] 큰 점프부터, "다를 때만" 함께 올라간다
>         for k in range(self.LOG - 1, -1, -1):
>             if up[k][u] != up[k][v]:
>                 u, v = up[k][u], up[k][v]
>         return up[0][u]                          # u 가 아니라 부모! LCA 의 자식에 멈춰 있다
>
>     def dist(self, u, v):
>         """두 노드 사이 간선 수."""
>         return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]
>
>
> # ---- (5) 오일러 투어 + 희소 배열 - 질의 O(1) ----
> class EulerRMQLCA:
>     def __init__(self, adj, root=0):
>         parent, depth, order = root_tree(adj, root)
>         self.depth = depth
>         children = [[] for _ in adj]
>         for v in order[1:]:
>             children[parent[v]].append(v)
>         # 반복문 오일러 투어: 길이 정확히 2N-1
>         euler, first = [root], [-1] * len(adj)
>         first[root] = 0
>         stack = [(root, 0)]                      # (노드, 다음에 볼 자식 인덱스)
>         while stack:
>             v, i = stack.pop()
>             if i < len(children[v]):
>                 stack.append((v, i + 1))
>                 w = children[v][i]
>                 first[w] = len(euler)
>                 euler.append(w)
>                 stack.append((w, 0))
>             elif stack:
>                 euler.append(stack[-1][0])       # 부모로 돌아오며 다시 기록 - 핵심!
>         self.euler, self.first = euler, first
>         # 희소 배열: table[k][i] = [i, i+2^k) 에서 depth 최소인 euler 인덱스
>         m = len(euler)
>         LOG = max(1, m.bit_length())
>         table = [list(range(m))]
>         for k in range(1, LOG):
>             span, prev = 1 << k, table[-1]
>             half = span >> 1
>             row = [0] * (m - span + 1)
>             for i in range(m - span + 1):
>                 a, b = prev[i], prev[i + half]
>                 row[i] = a if depth[euler[a]] <= depth[euler[b]] else b
>             table.append(row)
>         self.table = table
>
>     def lca(self, u, v):
>         l, r = self.first[u], self.first[v]
>         if l > r:
>             l, r = r, l
>         k = (r - l + 1).bit_length() - 1
>         a = self.table[k][l]
>         b = self.table[k][r - (1 << k) + 1]      # 겹쳐도 된다 - min 은 멱등!
>         e, d = self.euler, self.depth
>         return e[a] if d[e[a]] <= d[e[b]] else e[b]
> ```
>
> 전체 실행 파일(타잔 오프라인·교차 검증·실측 포함) → [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> | # | 문제 | 출처 | 난이도 | 핵심 유형 |
> |---|---|---|---|---|
> | 1 | Lowest Common Ancestor of a BST | [LeetCode #235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | 🟢기초 | BST 값 비교 `O(h)` |
> | 2 | Lowest Common Ancestor of a Binary Tree | [LeetCode #236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | 🟡중급 | 후위 순회 재귀 6줄 |
> | 3 | Lowest Common Ancestor of Deepest Leaves | [LeetCode #1123](https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/) | 🟡중급 | (높이, LCA) 동시 반환 트리 DP |
> | 4 | 합승 택시 요금 | [프로그래머스 #72413](https://school.programmers.co.kr/learn/courses/30/lessons/72413) | ⚫기출 | 분기점 전수 조사 + 플로이드-워셜 |
> | 5 | Step-By-Step Directions From a Binary Tree Node to Another | [LeetCode #2096](https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/) | 🔴심화 | 경로 문자열의 공통 접두사 제거 |
> | 6 | Kth Ancestor of a Tree Node | [LeetCode #1483](https://leetcode.com/problems/kth-ancestor-of-a-tree-node/) | 🔴심화 | 이진 상승 표 |
>
> 상세 설명·힌트 → [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제를 **플랫폼 시그니처**(LeetCode `class Solution` / 프로그래머스 `def solution`)로 구현하고, 가능한 곳은 **다중 접근 + 교차 검증**을 붙였다.
> - **#235** — 반복문 값 비교 `O(h)`·`O(1)` / 재귀 / #236 범용 해법 세 가지 대조
> - **#236** — 후위 순회 재귀 / 부모 맵 + 조상 집합 `O(N)` 반복 버전(재귀 없음) 두 가지
> - **#1123** — `(높이, LCA)` 동시 반환 1-pass / 최대 깊이 선계산 후 2-pass 두 가지
> - **#72413** — 플로이드-워셜 `O(n³)` / 다익스트라 `n`회 두 가지 비교
> - **#2096** — 경로 문자열 공통 접두사 제거 / 명시적 LCA 계산 후 조립 두 가지
> - **#1483** — 이진 상승 `O(N log N)` 전처리 / 나이브 부모 추적과 소규모 교차 검증
>
> 코드 → [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-42-string-matching/concept|Day 42 — 문자열 매칭 (KMP·라빈-카프)]]
- ➡️ **다음(next):** [[day-44-tree-dp/concept|Day 44 — 트리 DP (Tree DP)]]
- 🧭 **관련(related):**
  - [[day-11-tree-basics/concept|Day 11 — 트리 기본 (Tree Basics)]] — 부모·자식·깊이·높이의 정의와 BST 성질. #235는 여기서 바로 파생된다.
  - [[day-29-tree-traversal/concept|Day 29 — 트리 순회·응용]] — **후위 순회가 아래에서 위로 정보를 모은다**는 것이 #236·#1123 해법의 본질.
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — 오일러 투어와 타잔 LCA가 모두 DFS의 진입·이탈 시점을 이용한다.
  - [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — 파이썬에서 `parent`·`depth`를 **재귀 없이** 만드는 정석 도구.
  - [[day-22-recursion/concept|Day 22 — 재귀와 분할정복]] — 재귀 한도 1000이 오늘의 최대 실전 함정. `reversed(BFS 순서)`가 그 우회로다.
  - [[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find)]] — **타잔 오프라인 LCA**가 Union-Find 하나로 거의 선형에 전부 답한다.
  - [[day-40-segment-tree/concept|Day 40 — 세그먼트 트리·펜윅 트리]] — LCA를 **RMQ로 환원**하는 순간 그대로 이어진다. 희소 배열과의 역할 분담(정적 vs 갱신)도 여기서.
  - [[day-41-bitmask/concept|Day 41 — 비트마스킹 (Bitmasking)]] — **이진 상승의 전부가 "깊이 차를 2의 거듭제곱으로 분해"** 다. 비트 사고의 트리 응용.
  - [[day-31-dp/concept|Day 31 — 동적 계획법 입문]] — `up[k][v] = up[k-1][up[k-1][v]]`는 상태 `(k, v)`의 DP다. #1123은 트리 DP의 기본형.
  - [[day-35-bellman-floyd/concept|Day 35 — 벨만-포드·플로이드-워셜]] — #72413에서 **트리가 아닐 때 "분기점"을 어떻게 찾는가**의 답.
  - [[day-18-binary-search/concept|Day 18 — 이분 탐색]] — 이진 상승 2단계의 "큰 보폭부터 안전한 만큼만 전진"이 같은 사고 구조.
  - [[day-14-prefix-sum/concept|Day 14 — 누적 합 (Prefix Sum)]] — `path_sum = S[u] + S[v] - 2·S[LCA]`는 **트리 위의 누적 합**이다.
  - [[day-42-string-matching/concept|Day 42 — 문자열 매칭 (KMP·라빈-카프)]] — #2096의 **"공통 접두사 제거"** 가 접두사 사고의 재등장. 무작위 교차 검증 습관도 그대로 이어진다.
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — **전처리 vs 질의 트레이드오프**를 한 주제 안에서 다섯 가지나 비교할 수 있는 드문 사례.
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]
