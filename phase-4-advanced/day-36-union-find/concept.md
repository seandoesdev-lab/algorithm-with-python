---
day: 36
phase: 4-advanced
title: 서로소 집합 (Union-Find / Disjoint Set)
category: [자료구조, 서로소 집합, Union-Find, 그래프, 연결 요소, 사이클 판별]
difficulty: 중급
status: done
prev: "[[day-35-bellman-floyd/concept|Day 35 — 최단 경로: 벨만-포드·플로이드-워셜]]"
next: "[[day-37-mst/concept|Day 37 — 최소 신장 트리 (MST: Kruskal·Prim)]]"
related:
  - "[[day-35-bellman-floyd/concept|Day 35 — 최단 경로: 벨만-포드·플로이드-워셜]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-09-hashing/concept|Day 09 — 해시 dict/set]]"
  - "[[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]]"
  - "[[day-37-mst/concept|Day 37 — 최소 신장 트리 (MST: Kruskal·Prim)]]"
sources:
  - https://leetcode.com/problems/number-of-provinces/
  - https://leetcode.com/problems/redundant-connection/
  - https://leetcode.com/problems/satisfiability-of-equality-equations/
  - https://leetcode.com/problems/number-of-operations-to-make-network-connected/
  - https://leetcode.com/problems/accounts-merge/
  - https://school.programmers.co.kr/learn/courses/30/lessons/43162
  - https://en.wikipedia.org/wiki/Disjoint-set_data_structure
tags: [phase/4, topic/union-find, topic/disjoint-set, topic/graph, topic/connectivity]
---

# Day 36 — 서로소 집합 (Union-Find / Disjoint Set)

> [!abstract] 한눈 요약 (TL;DR)
> **서로소 집합(disjoint set)** 은 "겹치지 않는 여러 그룹"을 관리하는 자료구조로, 흔히 **유니온-파인드(Union-Find)** 또는 **DSU(Disjoint Set Union)** 라 부른다. 딱 두 가지 질문에 **거의 O(1)** 로 답한다 — **`find(x)`**: "x는 어느 그룹의 대표(root)에 속하나?", **`union(a, b)`**: "a와 b가 든 두 그룹을 하나로 합쳐라". 각 원소가 **부모(parent) 포인터** 하나만 들고 위로 타고 올라가 대표를 찾는 **트리들의 숲(forest)** 이 전부다. 여기에 두 최적화 — **경로 압축(path compression)** 과 **랭크/사이즈 합치기(union by rank/size)** — 를 얹으면 한 연산이 **역아커만 함수 O(α(N))**, 사실상 상수 시간이 된다. 코테에서는 **① 연결 요소(connected component) 개수 세기**, **② 무방향 그래프의 사이클 판별**, **③ [[day-37-mst/concept|MST 크루스칼(Kruskal)]]의 핵심 부품**, **④ "같다/연결됐다"류 제약의 그룹핑**에 반복 등장한다. [[day-25-dfs/concept|DFS(Day 25)]]로도 연결 요소를 세지만, **간선이 하나씩 동적으로 추가되는(online)** 상황에선 Union-Find가 압도적으로 간결하다. 핵심 한 줄: **"두 원소가 같은 대표를 가리키면 같은 그룹"**.

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **무엇인가.** 원소들을 **서로 겹치지 않는(disjoint)** 그룹으로 나눠 관리하는 자료구조다. "그룹"은 곧 그래프의 **연결 요소(connected component)** 라고 보면 된다. 각 그룹은 대표 원소 하나(**root**, 대표자·리더)로 식별된다. 두 원소가 **같은 그룹인지**는 "둘의 대표가 같은가?"로 판정한다.
>
> **일상 비유 — 동아리 합병.** 학교에 여러 동아리가 있고, 각 동아리에는 **회장(root)** 이 한 명 있다. 학생 x가 어느 동아리 소속인지 알려면 "너의 선배는 누구야?"를 계속 물어 올라가 **회장에 닿는다(`find`)**. 두 동아리가 통합되면 한쪽 회장이 다른 쪽 회장 **밑으로 들어간다(`union`)** — 회장끼리만 연결하면 두 동아리 전체가 한 번에 합쳐진다. "A와 B가 같은 동아리냐"는 두 사람의 회장이 같은지만 보면 된다.
>
> **왜 배열 하나로 되나.** 원소를 0..N−1 정수로 번호 매기면, **`parent[x]` = x의 부모**라는 배열 하나로 숲 전체를 표현한다. `parent[x] == x`이면 x가 그 그룹의 root다. `find`는 root에 닿을 때까지 부모를 타고 올라가고, `union`은 한 root의 부모를 다른 root로 바꾼다(`parent[rootA] = rootB`). 원소가 문자열·좌표라면 [[day-09-hashing/concept|dict(Day 09)]]로 "이름 → 정수 인덱스"만 매핑하면 똑같이 쓴다.
>
> **DFS/BFS와의 차이.** [[day-25-dfs/concept|DFS(Day 25)]]·[[day-26-bfs/concept|BFS]]도 연결 요소를 센다. 하지만 그건 **그래프가 다 주어진 뒤(offline)** 한 번 훑는 방식이다. Union-Find는 **간선이 하나씩 들어올 때마다(online)** 즉시 그룹을 갱신하고 "지금 두 원소가 연결됐나?"를 바로 답한다. "간선 추가 → 사이클 생기나?", "지금까지 그룹 몇 개?" 같은 **동적 연결성(dynamic connectivity)** 질문은 Union-Find의 독무대다.

> [!gear]- 2. 동작 원리 (How It Works)
> **(A) 기본 골격 — parent 배열.**
> ```
> parent = [0, 1, 2, 3, 4]     # 처음엔 각자 자기 자신이 root (그룹 5개)
>
> find(x):                     # x의 root를 찾는다
>     while parent[x] != x:
>         x = parent[x]        # 부모를 타고 올라감
>     return x
>
> union(a, b):                 # a, b가 든 두 그룹을 합침
>     ra, rb = find(a), find(b)
>     if ra == rb: return      # 이미 같은 그룹 (합칠 것 없음)
>     parent[ra] = rb          # 한 root를 다른 root 밑에 붙임
> ```
> ```
>   union(0,1), union(2,3), union(1,3) 후:
>
>        3(root)              parent = [1, 3, 3, 3, 4]
>       /  \                  find(0): 0 ->1 ->3   (root=3)
>      1    2                 find(4): 4           (root=4)
>      |                      => 0,1,2,3 한 그룹 / 4 혼자
>      0
> ```
> **(B) 최적화 1 — 경로 압축(path compression).** `find`가 root를 찾은 김에, 지나온 노드들의 부모를 **root로 직접 갱신**한다. 다음 `find`는 한 번에 root에 닿는다. 트리를 납작하게(flatten) 눌러 긴 사슬을 방지한다.
> ```
> find(x):
>     if parent[x] != x:
>         parent[x] = find(parent[x])   # 재귀하며 root로 직결
>     return parent[x]
> # 반복(iterative) 버전 — 재귀 깊이 걱정 없음:
> find(x):
>     root = x
>     while parent[root] != root:
>         root = parent[root]
>     while parent[x] != root:          # 2-pass 압축
>         parent[x], x = root, parent[x]
>     return root
> ```
> **(C) 최적화 2 — 랭크/사이즈로 합치기(union by rank/size).** 항상 **작은 트리를 큰 트리 밑에** 붙인다. 그래야 전체 높이가 낮게 유지된다. `size[]`(원소 수) 또는 `rank[]`(대략적 높이)를 함께 관리한다.
> ```
> union(a, b):
>     ra, rb = find(a), find(b)
>     if ra == rb: return False         # 이미 같은 그룹 → (사이클!)
>     if size[ra] < size[rb]:
>         ra, rb = rb, ra               # ra가 항상 더 큰 쪽
>     parent[rb] = ra                   # 작은 rb를 큰 ra 밑에
>     size[ra] += size[rb]
>     return True                       # 새로 합쳐짐
> ```
> **(D) 사이클 판별.** 무방향 그래프에서 간선 (a,b)를 `union`할 때, **a와 b의 root가 이미 같으면** 이 간선은 두 원소를 잇는 게 아니라 **이미 연결된 것을 또 잇는 것** — 즉 **사이클을 만든다.** `union`이 `False`를 반환하는 순간이 사이클 발견이다(Redundant Connection, MST 크루스칼의 핵심).
> ```
>   1 - 2       간선 (1,2),(2,3),(1,3) 순서로 union:
>   |   |         (1,2): 합쳐짐  (2,3): 합쳐짐
>   +-3-+         (1,3): 1,3 root 이미 같음 -> 사이클! 이 간선이 여분
> ```
> **(E) 연결 요소 개수.** 모든 `union`을 마친 뒤 **`find(i) == i`인 i의 수**(= 서로 다른 root 수)가 그룹 개수다. 또는 union이 성공(True)할 때마다 `components -= 1`로 세도 된다(시작값 N).
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. N=원소 수, M=연산(간선) 수. α는 **역아커만 함수(inverse Ackermann)** — N이 우주의 원자 수여도 α(N) ≤ 5, 사실상 상수.
>
> | 최적화 수준 | find / union 1회 | M회 총합 | 비고 |
> |---|---|---|---|
> | 최적화 없음 (순수 트리) | 최악 O(N) | O(N·M) | 한 줄로 늘어진 사슬이면 느림 |
> | 경로 압축만 | 평균 O(log N) | — | 반쯤 개선 |
> | 랭크/사이즈만 | O(log N) | O(M log N) | 높이 보장 |
> | **경로 압축 + 랭크/사이즈** | **O(α(N)) ≈ O(1)** | **O(M·α(N))** | 실전 표준 |
> | 초기화 | O(N) | — | parent/size 배열 생성 |
> | 공간 | O(N) | — | parent(+size/rank) 배열 |
>
> > **왜 거의 O(1)인가.** 두 최적화를 **함께** 쓰면 M번의 연산 총비용이 **O(M·α(N))** 임이 증명돼 있다(Tarjan). α(N)은 5를 넘지 않으므로 "한 연산 ≈ 상수"로 취급한다. 그래서 Union-Find는 **간선 M개를 순회하며 매번 union** 해도 사실상 O(M) 선형이다.
> >
> > **DFS/BFS 대비.** 정적 그래프의 연결 요소 세기는 [[day-25-dfs/concept|DFS(Day 25)]]도 O(V+E)로 똑같이 빠르다. 차이는 **동적 상황**이다. "간선을 하나씩 추가하며 매 순간 연결 여부·그룹 수를 물으면" DFS는 매번 다시 훑어야 하지만(O(V+E)씩), Union-Find는 추가마다 O(α)라 압도적이다.
> >
> > **경로 압축은 재귀 깊이 주의.** 파이썬 재귀 `find`는 초기 트리가 깊으면 `RecursionError`가 날 수 있다(기본 한계 1000). N이 크면 **반복(iterative) 버전**을 쓰거나 `sys.setrecursionlimit`을 올린다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **"대표가 같으면 한 그룹"** 한 문장만 기억하면 90%가 풀린다. `find`는 대표 찾기, `union`은 대표끼리 연결, "같은 그룹?"은 `find(a) == find(b)`.
> - **경로 압축 + 사이즈 합치기는 세트로 외운다.** 하나만 쓰면 O(log N), 둘 다 쓰면 O(α). 코테 템플릿은 항상 둘 다 넣는다. ([Disjoint-set 위키](https://en.wikipedia.org/wiki/Disjoint-set_data_structure))
> - **문자열·좌표 원소는 dict로 인덱싱.** 이메일·이름·(r,c) 좌표가 원소면 `{key: 정수}` 매핑을 먼저 만들고 정수로 Union-Find. 좌표는 `r*W + c`로 1차원화해도 된다([[day-09-hashing/concept|Day 09]]).
> - **`union`의 반환값을 활용하라.** "이미 같은 그룹이라 합칠 게 없음(False)"이 곧 **사이클/여분 간선** 신호다. Redundant Connection, MST에서 이 boolean이 답을 만든다.
> - **연결 요소 수 = 초기 N에서 성공한 union 횟수를 뺀 값.** `comp = N; union 성공 시 comp -= 1`. 마지막에 `comp`가 그룹 수. `find(i)==i` 세기와 결과가 같다.
> - **격자(grid) 문제도 Union-Find로.** Number of Islands류는 상하좌우 인접 셀을 union. 다만 정적 격자는 DFS/BFS가 더 직관적이니, **간선이 동적으로 붙는** 문제에서 Union-Find의 이점이 크다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **`union` 전에 반드시 `find`로 root를 구해 비교한다.** `parent[a] = b`처럼 **원소를 직접 붙이면 안 된다** — a, b의 **root끼리** 붙여야(`parent[find(a)] = find(b)`) 두 그룹 전체가 합쳐진다. 초보 최다 버그.
> 2. **두 최적화를 빼면 최악 O(N) 사슬이 된다.** 경로 압축·사이즈 합치기 없이 순진하게 붙이면 한 줄로 늘어져 `find`가 O(N). 큰 입력에서 TLE(시간 초과)의 원인.
> 3. **재귀 `find`의 깊이 한계.** 파이썬은 기본 재귀 한계가 1000이라 초기 트리가 깊으면 터진다. **반복 버전**을 쓰거나 `sys.setrecursionlimit(10**6)`. (경로 압축이 되면 이후엔 얕아지지만 첫 호출이 위험.)
> 4. **Union-Find는 "합치기"만 잘한다. "쪼개기(분리)"는 못 한다.** 한 번 합친 그룹을 되돌리는 연산은 기본형에 없다(그래서 "간선 삭제" 문제는 **역순으로 union** 하는 오프라인 트릭을 쓴다).
> 5. **방향 그래프의 사이클 판별에는 부적합.** Union-Find의 사이클 판별은 **무방향 그래프** 전용이다. 방향 그래프의 사이클은 [[day-29-tree-traversal/concept|DFS]] 방문 색칠이나 [[day-28-graph/concept|위상 정렬]]로 판별한다.
> 6. **연결 요소 수 세기: `find(i)==i` vs `parent[i]==i`.** 반드시 **`find(i)`** 로 세라. 경로 압축이 끝까지 안 됐다면 `parent[i]==i`만으로는 root가 아닌 노드를 놓칠 수 있다. 세기 직전에 모든 i를 `find` 한 번 돌려 확정하는 게 안전하다.
> 7. **"같다(==)/다르다(!=)" 제약 문제의 정석.** 990처럼 등식(`a==b`)을 먼저 전부 `union` 하고, 그 다음 부등식(`a!=b`)에서 `find(a)==find(b)`면 모순 → 불가능. **처리 순서(등식 먼저)** 가 핵심.
> 8. **크루스칼 MST의 심장.** [[day-37-mst/concept|Day 37]] 크루스칼은 "간선을 가중치 오름차순 정렬 → 사이클 안 만드는 간선만 union으로 채택". Union-Find 없이는 성립하지 않는다. 오늘 배운 사이클 판별이 그대로 쓰인다.
> 9. **인덱스 0-based / 1-based 혼동 주의.** 문제가 1..n으로 노드를 주면 `parent`를 크기 n+1로 잡고 0번을 버린다. 오프바이원(off-by-one)이 조용한 오답을 만든다.

> [!example]- 예제 코드 (Examples)
> ```python
> # 표준 Union-Find (경로 압축 + 사이즈 합치기) - 코테 템플릿
> class DSU:
>     def __init__(self, n):
>         self.parent = list(range(n))   # 각자 자기 자신이 root
>         self.size = [1] * n            # 그룹 크기
>         self.count = n                 # 연결 요소 수
>
>     def find(self, x):                 # 경로 압축(반복 버전)
>         root = x
>         while self.parent[root] != root:
>             root = self.parent[root]
>         while self.parent[x] != root:  # 지나온 노드를 root로 직결
>             self.parent[x], x = root, self.parent[x]
>         return root
>
>     def union(self, a, b):             # 사이즈로 합치기
>         ra, rb = self.find(a), self.find(b)
>         if ra == rb:
>             return False               # 이미 같은 그룹 -> 사이클/여분
>         if self.size[ra] < self.size[rb]:
>             ra, rb = rb, ra            # 큰 쪽(ra) 밑에 작은 쪽(rb)
>         self.parent[rb] = ra
>         self.size[ra] += self.size[rb]
>         self.count -= 1                # 그룹 하나 줄어듦
>         return True
>
>     def connected(self, a, b):
>         return self.find(a) == self.find(b)
>
>
> # 활용 1) 연결 요소 개수
> def count_components(n, edges):
>     dsu = DSU(n)
>     for a, b in edges:
>         dsu.union(a, b)
>     return dsu.count
>
> # 활용 2) 무방향 그래프 사이클 판별
> def has_cycle(n, edges):
>     dsu = DSU(n)
>     for a, b in edges:
>         if not dsu.union(a, b):        # 합칠 수 없으면 사이클
>             return True
>     return False
> ```
>
> 전체 실행 가능한 예제: [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> **연결 요소 세기 → 사이클 판별 → 제약 그룹핑 → 응용** 순으로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Number of Provinces | [LeetCode #547](https://leetcode.com/problems/number-of-provinces/) | 🟡중급 | 연결 요소 개수(기본) |
> | 2 | 네트워크 | [프로그래머스 #43162](https://school.programmers.co.kr/learn/courses/30/lessons/43162) | ⚫기출 | 연결 요소(Union-Find 적용) |
> | 3 | Redundant Connection | [LeetCode #684](https://leetcode.com/problems/redundant-connection/) | 🟡중급 | 무방향 사이클 판별 |
> | 4 | Satisfiability of Equality Equations | [LeetCode #990](https://leetcode.com/problems/satisfiability-of-equality-equations/) | 🟡중급 | 등식/부등식 제약(2-pass) |
> | 5 | Number of Operations to Make Network Connected | [LeetCode #1319](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) | 🔴심화 | 컴포넌트 수−1 + 여분 간선 |
> | 6 | Accounts Merge | [LeetCode #721](https://leetcode.com/problems/accounts-merge/) | 🔴심화 | dict 인덱싱 + 그룹핑 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 DSU 모델링(인접 행렬·간선 리스트·문자열 dict 인덱싱), 연결 요소 세기·무방향 사이클 판별·등식 우선 2-pass·컴포넌트−1 공식, 프로그래머스/LeetCode 시그니처별 구현과 DFS 대비 다중 접근: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-35-bellman-floyd/concept|Day 35 — 최단 경로: 벨만-포드·플로이드-워셜]] — 간선을 완화하며 "거리"를 다뤘다면, 이번엔 간선으로 "연결성(그룹)"을 관리한다. 둘 다 그래프 위 간선 순회지만 답하는 질문이 다르다
- ➡️ **다음(next):** [[day-37-mst/concept|Day 37 — 최소 신장 트리 (MST: Kruskal·Prim)]] — 오늘의 사이클 판별이 크루스칼의 심장이다. "가중치 오름차순 간선을 사이클 안 나게 union"으로 최소 신장 트리를 만든다
- 🧭 **관련(related):**
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 간선 리스트·인접 행렬 입력을 Union-Find로 그룹핑하는 토대
  - [[day-25-dfs/concept|Day 25 — DFS]] — 연결 요소를 세는 또 다른 길. 정적이면 DFS, 동적(간선 추가·사이클 질의)이면 Union-Find로 갈린다
  - [[day-09-hashing/concept|Day 09 — 해시 dict/set]] — 문자열·좌표 원소를 정수 인덱스로 매핑해 배열 Union-Find에 태우는 필수 도구
  - [[day-16-big-o/concept|Day 16 — 시간복잡도와 Big-O]] — 역아커만 O(α(N))이 왜 사실상 상수인지, 두 최적화의 유무가 O(N)↔O(α)를 가르는 근거
  - [[day-37-mst/concept|Day 37 — 최소 신장 트리]] — 다음 주제. Union-Find를 부품으로 쓰는 대표 알고리즘
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]
