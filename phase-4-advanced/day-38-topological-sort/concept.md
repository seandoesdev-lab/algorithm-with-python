---
day: 38
phase: 4-advanced
title: 위상 정렬 (Topological Sort)
category: [그래프, 위상 정렬, DAG, 칸 알고리즘, Kahn, DFS, 사이클 판별, 의존성]
difficulty: 중급
status: done
prev: "[[day-37-mst/concept|Day 37 — 최소 신장 트리 (MST: Kruskal·Prim)]]"
next: "[[day-39-trie/concept|Day 39 — 트라이 (Trie)]]"
related:
  - "[[day-37-mst/concept|Day 37 — 최소 신장 트리 (MST: Kruskal·Prim)]]"
  - "[[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]]"
  - "[[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
  - "[[day-31-dp/concept|Day 31 — 동적 계획법 입문 (Dynamic Programming)]]"
  - "[[day-35-bellman-floyd/concept|Day 35 — 최단 경로: 벨만-포드·플로이드-워셜]]"
  - "[[day-08-queue-deque/concept|Day 08 — 큐와 덱]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
sources:
  - https://leetcode.com/problems/course-schedule/
  - https://leetcode.com/problems/course-schedule-ii/
  - https://school.programmers.co.kr/learn/courses/30/lessons/49191
  - https://leetcode.com/problems/find-eventual-safe-states/
  - https://leetcode.com/problems/parallel-courses-iii/
  - https://leetcode.com/problems/minimum-height-trees/
  - https://en.wikipedia.org/wiki/Topological_sorting
  - https://en.wikipedia.org/wiki/Directed_acyclic_graph
tags: [phase/4, topic/topological-sort, topic/dag, topic/kahn, topic/graph, topic/bfs, topic/dfs, topic/cycle-detection]
---

# Day 38 — 위상 정렬 (Topological Sort)

> [!abstract] 한눈 요약 (TL;DR)
> **위상 정렬(topological sort)** 은 **방향 그래프(directed graph)** 의 정점을 **모든 간선 u→v에 대해 u가 v보다 앞에 오도록** 한 줄로 늘어놓는 것이다. 한 문장으로: **"선행 조건을 먼저 하는 순서 만들기"**. 선수 과목 수강 순서, 빌드 의존성(`make`), 패키지 설치 순서, 작업 스케줄링이 모두 이 문제다. 핵심 전제: **위상 정렬은 사이클이 없는 방향 그래프(DAG, Directed Acyclic Graph)에서만 존재한다.** A가 B를 요구하고 B가 A를 요구하면 시작할 수 있는 게 없기 때문이다. 그래서 **위상 정렬 시도 = 사이클 판별기**로 그대로 쓰인다 — 정렬 결과의 길이가 V보다 짧으면 사이클이 있다. 구하는 방법은 두 가지다. **칸 알고리즘(Kahn's algorithm)**: 각 정점의 **진입 차수(in-degree)** 를 세고, **진입 차수 0인 정점을 큐에 넣고 하나씩 꺼내면서** 그 정점이 가리키는 이웃의 진입 차수를 1 줄인다([[day-26-bfs/concept|BFS(Day 26)]]와 똑같은 골격). **DFS 기반**: [[day-25-dfs/concept|DFS(Day 25)]]로 깊이 들어갔다가 **되돌아 나오는 순간(post-order)** 정점을 스택에 쌓고, 마지막에 **뒤집는다**. 둘 다 **O(V+E)** — 그래프를 한 번 훑는 값에 정렬을 얻는다. 그리고 DAG에서는 위상 순서대로 훑으면 **의존 관계가 이미 다 계산되어 있으므로** [[day-31-dp/concept|DP(Day 31)]]가 공짜로 성립한다(DAG 최장 경로 = 작업 완료 최소 시간). 핵심 한 줄: **"진입 차수 0부터 꺼내고, 못 꺼낸 게 남으면 사이클."**

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **정의.** 방향 그래프 G=(V,E)의 위상 정렬은 정점 전체를 나열한 순열 v₁, v₂, …, v_V 로서, **모든 간선 (u→v)에 대해 u가 v보다 먼저 등장**하는 것이다. 이 순열을 **위상 순서(topological order)** 라 한다.
>
> **존재 조건이 곧 정의의 절반이다.** 위상 정렬이 존재하는 것과 그래프가 **DAG(사이클 없는 방향 그래프)** 인 것은 **완전히 동치(if and only if)** 다. 사이클 v₁→v₂→v₁ 이 있으면 v₁이 v₂보다 앞이어야 하고 동시에 뒤여야 하므로 모순이다. 반대로 DAG라면 **진입 차수 0인 정점이 항상 최소 하나 존재**하고(그렇지 않으면 거꾸로 따라가다 반드시 정점이 재방문되어 사이클), 그것을 떼어내도 남은 그래프는 여전히 DAG이므로 귀납적으로 끝까지 나열할 수 있다. **이 증명이 곧 칸 알고리즘이다.**
>
> **일상 비유 — 옷 입는 순서.** 속옷 → 셔츠 → 스웨터, 양말 → 신발, 바지 → 신발. 이 규칙만 지키면 "속옷, 셔츠, 양말, 바지, 스웨터, 신발"도 되고 "양말, 속옷, 바지, 셔츠, 스웨터, 신발"도 된다. **답이 여러 개인 게 정상**이다. 그런데 "신발을 신어야 양말을 신을 수 있다"는 규칙이 추가되면? 양말↔신발 사이클이라 **아침에 아예 옷을 입을 수 없다**. 이게 위상 정렬 불가 상태다.
>
> **부분 순서(partial order)를 전체 순서(total order)로 펴는 작업.** 간선은 "A는 B보다 먼저"라는 **부분적인** 제약만 준다. 제약이 없는 두 정점(양말과 셔츠)은 서로 순서가 정해지지 않는다. 위상 정렬은 이 느슨한 부분 순서를 **모순 없이 한 줄로 확장(linear extension)** 하는 것이다. 그래서 **위상 순서가 유일한 경우는 인접한 모든 쌍이 간선으로 강제될 때**, 즉 **해밀턴 경로(Hamiltonian path)가 존재할 때**뿐이다. 프로그래머스 #49191 "순위"가 정확히 이 감각을 묻는다.
>
> **두 구현의 성격 차이.** 칸(Kahn)은 **"지금 당장 할 수 있는 일"을 큐에 모아두고 하나씩 처리**한다 — 시뮬레이션에 가깝고, 사이클 판별과 "동시에 처리 가능한 작업 묶음(레벨)"을 자연스럽게 얻는다. DFS는 **"나보다 뒤에 와야 하는 모든 것을 먼저 끝내고 나를 기록"** 한다 — 재귀적이고, 되돌아 나오는 순서를 뒤집는 트릭이 핵심이다. 코테에서는 **칸이 압도적으로 유리**하다(재귀 깊이 문제 없음, 사이클 판별이 카운터 한 줄).

> [!gear]- 2. 동작 원리 (How It Works)
> **예제 DAG** (정점 0~5, "수강 선후 관계"):
> ```
>    0 ----> 2 ----> 3 ----> 5
>            ^       ^
>            |       |
>    1 ------+-------+----> 4
>
>   간선: 0->2, 1->2, 2->3, 1->3, 3->5, 1->4
>   진입 차수: 0:0  1:0  2:2(0,1)  3:2(2,1)  4:1(1)  5:1(3)
> ```
>
> **(A) 칸 알고리즘 (Kahn) — 진입 차수 0을 큐로 흘려보낸다.**
> ```
> 1) 모든 정점의 진입 차수(indegree) 계산
> 2) indegree == 0 인 정점 전부를 큐에 넣는다
> 3) 큐가 빌 때까지:
>      u = 큐에서 pop  ->  결과 리스트에 append
>      u 의 모든 이웃 v 에 대해 indegree[v] -= 1
>          indegree[v] == 0 이 되면 큐에 push
> 4) len(결과) == V 면 위상 순서, 아니면 사이클 존재
> ```
> ```
> 초기 큐 = [0, 1]                       결과 = []
>
> pop 0 -> 결과 [0]         indeg[2] 2->1
> pop 1 -> 결과 [0,1]       indeg[2] 1->0 (push 2)
>                           indeg[3] 2->1
>                           indeg[4] 1->0 (push 4)
> 큐 = [2, 4]
> pop 2 -> 결과 [0,1,2]     indeg[3] 1->0 (push 3)
> pop 4 -> 결과 [0,1,2,4]
> pop 3 -> 결과 [0,1,2,4,3] indeg[5] 1->0 (push 5)
> pop 5 -> 결과 [0,1,2,4,3,5]
>
> len == 6 == V  ->  위상 순서 성립
> ```
> **왜 맞는가.** 결과에 넣는 순간 그 정점의 **모든 선행 정점은 이미 결과에 들어가 있다**(그래서 진입 차수가 0으로 떨어졌다). 이 불변식(invariant)이 위상 순서 조건 그 자체다.
>
> **(B) 사이클이 있으면 어떻게 되는가.**
> ```
>    0 ----> 1 ----> 2
>            ^       |
>            +-------+          간선: 0->1, 1->2, 2->1
>
>   indegree: 0:0  1:2(0,2)  2:1(1)
>   큐 = [0]  ->  pop 0, indeg[1] 2->1  ->  큐 빔!
>   결과 = [0],  len 1 != 3   ->  사이클 존재 (1,2 가 서로를 붙잡고 있다)
> ```
> 사이클에 속한 정점은 **진입 차수가 절대 0으로 떨어지지 않는다**. 그래서 "못 꺼낸 정점 = 사이클에 갇힌 정점"이다. LeetCode #207이 이 한 줄 판정을 그대로 묻는다.
>
> **(C) DFS 기반 — post-order를 뒤집는다.**
> ```
> visit(u):
>     state[u] = 방문중(GRAY)
>     for v in adj[u]:
>         if state[v] == GRAY:  ->  뒤로 가는 간선(back edge) = 사이클!
>         if state[v] == WHITE: visit(v)
>     state[u] = 완료(BLACK)
>     stack.append(u)          # 되돌아 나오는 순간 기록 (post-order)
>
> 모든 정점에 대해 visit  ->  stack 을 reverse 하면 위상 순서
> ```
> ```
> visit(0) -> visit(2) -> visit(3) -> visit(5) [끝] push 5
>                                     push 3
>                             push 2
>                     push 0
> visit(1) -> 2,3 은 BLACK(끝남) -> visit(4) push 4
>                                   push 1
> stack = [5, 3, 2, 0, 4, 1]
> reverse = [1, 4, 0, 2, 3, 5]   ->  유효한 위상 순서 (칸과 다르지만 둘 다 정답)
> ```
> **3색 표시(white/gray/black)가 사이클 판별의 핵심이다.** 방문 여부만 이진(bool)으로 두면 "이미 끝난 정점(BLACK)"과 "지금 재귀 스택 위에 있는 정점(GRAY)"을 구분할 수 없어 **사이클을 놓친다**. 방향 그래프 사이클 판별은 반드시 3색이다.
>
> **(D) 사전 순 최소 위상 순서 — 큐를 최소 힙으로.**
> ```
> 칸 알고리즘에서 deque 대신 heapq 를 쓰면
> 매 순간 "지금 가능한 정점 중 가장 작은 번호"를 고른다
>   -> 사전 순으로 가장 앞선(lexicographically smallest) 위상 순서
>   -> O((V+E) log V)
> ```
> "여러 답 중 사전 순 최소"를 요구하는 문제가 흔하다([[day-12-heap/concept|힙(Day 12)]] 응용).
>
> **(E) 위상 순서 = DAG DP의 계산 순서 (가장 중요한 응용).**
> ```
> 과목 i 를 끝내는 데 time[i] 가 걸리고, 선행 과목은 모두 끝나야 시작 가능.
> 전부 끝내는 최소 시간 = DAG 최장 경로(critical path)
>
> 칸으로 정점을 꺼내는 순서대로:
>     for v in adj[u]:
>         finish[v] = max(finish[v], finish[u] + time[v])
>
> 꺼낸 시점에 u 의 선행이 전부 확정되어 있으므로
> finish[u] 는 이미 최종값이다  ->  한 번 훑기로 DP 완성 O(V+E)
> ```
> [[day-31-dp/concept|DP(Day 31)]]에서 "부분 문제를 올바른 순서로 풀어야 한다"고 배운 그 **순서를 그래프에서 뽑아내는 도구**가 위상 정렬이다. LeetCode #2050이 정확히 이 패턴이다.
>
> **(F) 잎 소거(leaf peeling) — 무방향 트리의 위상 정렬 사촌.**
> ```
> 무방향 트리에서 차수(degree) 1 인 정점(잎)을 한 층씩 벗겨낸다.
> 마지막에 남는 1~2개 정점이 트리의 중심(centroid).
>   -> LeetCode #310 Minimum Height Trees
> 골격이 칸 알고리즘과 동일하다: 차수 1 을 큐에 넣고 벗기며 갱신.
> 차이: 방향 그래프의 "indegree 0" 대신 무방향의 "degree 1".
> ```
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. V=정점 수, E=간선 수.
>
> | 방법 | 시간복잡도 | 공간 | 특징 |
> |---|---|---|---|
> | **칸 알고리즘 (BFS, deque)** | **O(V+E)** | O(V+E) | 코테 기본. 사이클 판별이 카운터 한 줄. 재귀 없음 |
> | **DFS 기반 (post-order 역순)** | **O(V+E)** | O(V+E) + 재귀 O(V) | 3색 필요. 파이썬은 재귀 깊이 주의 |
> | 사전 순 최소 (heapq) | O((V+E) log V) | O(V+E) | log는 힙 삽입/삭제에서 |
> | 위상 순서 유일성 판정 | O(V+E) | O(V+E) | 칸에서 **큐 크기가 항상 1**인지 확인 |
> | DAG 최장/최단 경로 DP | O(V+E) | O(V) | 위상 순서대로 한 번 훑기 |
> | 모든 위상 순서 열거 | O(V!) 최악 | O(V) | 백트래킹. V ≤ 10 정도만 |
> | 도달 가능성 전체(전이 폐쇄) | O(V³) 또는 O(V·(V+E)) | O(V²) | 플로이드-워셜 또는 정점마다 BFS |
>
> > **왜 O(V+E)인가.** 각 정점은 큐에 **정확히 한 번** 들어가고 한 번 나온다(O(V)). 각 간선은 "이웃의 진입 차수 감소"에서 **정확히 한 번** 사용된다(O(E)). 더 볼 게 없다. [[day-26-bfs/concept|BFS(Day 26)]]와 같은 급의 비용으로 정렬을 얻는 것이 위상 정렬의 매력이다.
> >
> > **진입 차수 계산도 O(E)다.** 간선 목록을 한 번 훑으며 `indeg[v] += 1`. 인접 리스트를 만드는 비용과 합쳐 여전히 O(V+E).
> >
> > **비교 정렬의 O(n log n) 하한과 무관하다.** 위상 정렬은 값을 비교하지 않는다. 간선이 주는 제약만 따르므로 **정렬인데 log가 없다**. 단, "사전 순 최소"를 요구하면 비교(힙)가 개입해 log가 붙는다.
> >
> > **DAG DP는 왜 공짜인가.** 일반 그래프의 최장 경로는 **NP-난해(NP-hard)** 다. 사이클이 있으면 계속 돌아 무한히 길어질 수 있기 때문이다. 그런데 DAG로 한정하면 위상 순서가 존재해 **O(V+E)에 최장 경로가 풀린다**. "사이클이 없다"는 조건 하나가 NP-난해를 선형으로 만든다 — 면접에서 좋은 답변 소재다.
> >
> > **[[day-35-bellman-floyd/concept|Day 35]]와의 연결.** DAG라면 음수 간선이 있어도 벨만-포드(O(VE)) 없이 **위상 순서 한 번 훑기 O(V+E)** 로 최단 경로가 끝난다. DAG 최단 경로는 모든 최단 경로 알고리즘 중 가장 빠르다.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **암기 문장 하나면 끝.** **"진입 차수 0을 큐에 넣고, 꺼낼 때마다 이웃의 빚을 갚아준다."** 결과 길이가 V가 아니면 사이클. ([위상 정렬 위키](https://en.wikipedia.org/wiki/Topological_sorting))
> - **칸은 BFS 템플릿 재활용이다.** [[day-26-bfs/concept|BFS(Day 26)]] 코드에서 `visited` 자리에 `indegree`를 놓고, "처음 만나면 push" 대신 "빚이 0이 되면 push"로 바꾼 것뿐이다. 새로 외울 자료구조가 없다.
> - **간선 방향을 문제 문장에서 뽑는 연습.** LeetCode #207의 `prerequisites[i] = [a, b]`는 "**b를 먼저** 들어야 a를 들을 수 있다" → 간선은 **b→a**, `indeg[a] += 1`. **여기서 방향을 뒤집는 게 이 유형 최다 오답**이다. "먼저 하는 쪽 → 나중 하는 쪽"으로 소리 내어 확인하라.
> - **DAG인지 아닌지가 문제 유형을 결정한다.** "사이클 없음"이 문제에 명시되면 위상 정렬 + DP를 의심하고, 명시되지 않으면 **먼저 사이클 판별**부터 한다. ([DAG 위키](https://en.wikipedia.org/wiki/Directed_acyclic_graph))
> - **"동시에 처리 가능한 작업 묶음"은 칸의 레벨이다.** 큐를 비울 때 `for _ in range(len(queue))`로 한 층씩 처리하면(BFS 레벨 순회와 동일) "최소 몇 학기가 필요한가" 같은 질문에 바로 답한다.
> - **역방향 그래프 트릭.** "끝에서부터" 성질을 묻는 문제(LeetCode #802: 반드시 종착점에 도달하는 안전한 정점)는 **간선을 모두 뒤집어** 칸을 돌린다. 나가는 차수(out-degree) 0부터 벗겨내는 것과 같다.
> - **위상 순서가 유일한지 확인하는 법.** 칸을 돌리면서 **큐의 크기가 매 단계 정확히 1**이면 유일하다. 2 이상인 순간이 있으면 "지금 어느 것을 먼저 해도 된다"는 뜻이라 답이 여러 개다. 프로그래머스 #49191의 사고 구조가 이것이다.
> - **트리 중심 찾기도 같은 골격.** LeetCode #310처럼 무방향 트리에서 **차수 1(잎)을 벗겨나가면** 남는 1~2개가 중심이다. 방향 그래프의 "indegree 0"과 대응된다.

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **위상 정렬은 방향 그래프(directed) 전용이다.** 무방향 그래프에는 정의되지 않는다(간선 u—v가 양방향 제약이므로 둘 다 먼저일 수 없다). "무방향인데 위상 정렬"이라고 나오면 **잎 소거** 같은 다른 문제다.
> 2. **DAG가 아니면 위상 정렬은 존재하지 않는다.** 그리고 그 **부존재를 감지하는 것 자체가 알고리즘의 산출물**이다. `len(order) != V` 검사를 빼먹으면 사이클 그래프에서 **짧은 리스트를 정답인 척 반환**한다. 조용한 오답 1위.
> 3. **간선 방향을 반대로 넣는 실수가 압도적으로 많다.** `[a, b]`가 "a가 b를 선행 요구"인지 "a 다음에 b"인지 문제마다 다르다. **한 문장으로 읽어보고 진입 차수를 어느 쪽에 더할지 확정**한 다음 코딩하라. 방향이 뒤집혀도 대부분 예제 1개는 우연히 통과한다.
> 4. **답은 보통 여러 개다.** "정답 순서를 출력하라"인데 정해진 하나를 기대하는 채점기라면 **사전 순 최소** 같은 추가 조건이 반드시 명시되어 있다. 없으면 아무 유효 순서나 OK(LeetCode #210은 임의 유효 순서를 받는다).
> 5. **방향 그래프 사이클 판별에 bool `visited` 하나는 부족하다.** 반드시 **3색(WHITE/GRAY/BLACK)** 또는 **재귀 스택 집합**을 쓴다. `visited`만 쓰면 "이미 끝난 다른 분기"를 사이클로 오판해 **정상 DAG를 사이클이라 답한다**. 무방향 그래프 사이클 판별(부모 제외)과 혼동 금지.
> 6. **파이썬 재귀 DFS는 깊이 제한에 걸린다.** 기본 재귀 한도는 1000. 정점 10⁵의 사슬 그래프에서 즉사한다. `sys.setrecursionlimit(300000)`도 스택 오버플로 위험이 있으니 **코테에서는 칸(반복문)을 기본**으로 하라.
> 7. **진입 차수 배열 크기와 1-based/0-based.** 문제가 정점을 1..n으로 주면 `indeg = [0]*(n+1)`로 잡고 0번 인덱스는 버린다. LeetCode는 0-based(#207, #210), 프로그래머스는 1-based(#49191)가 많다. 이 혼동으로 IndexError 또는 조용한 오답이 난다.
> 8. **중복 간선(duplicate edge)은 진입 차수를 중복 계산한다.** `[[1,0],[1,0]]`처럼 같은 간선이 두 번 오면 `indeg[1]`이 2가 되고, 감소도 두 번 일어나므로 **결과는 여전히 맞다**. 다만 "간선 수"를 세거나 유일성을 판정할 때는 문제가 되니 필요하면 `set`으로 중복 제거한다.
> 9. **고립 정점(isolated vertex)을 빠뜨리지 마라.** 간선이 하나도 없는 정점은 진입 차수 0이므로 **초기 큐에 반드시 들어가야 한다**. 간선 목록만 보고 정점을 수집하면 고립 정점이 사라져 `len(order) != V`가 되어 "사이클 있음"으로 오판한다.
> 10. **DAG 최장 경로는 O(V+E), 일반 그래프 최장 경로는 NP-난해.** 이 대비는 면접 단골이다. "왜 DAG면 쉬워지나?" → 위상 순서가 존재해 부분 문제 의존성이 한 방향으로만 흐르므로 DP가 성립한다.
> 11. **위상 정렬이 유일 ⟺ 해밀턴 경로 존재.** 인접한 모든 쌍이 간선으로 강제되어야 순서가 하나로 확정된다. "몇 명의 순위를 확정할 수 있나"(프로그래머스 #49191)는 이 성질의 국소판 — **어떤 정점이 나머지 V−1개 전부와 도달 관계(위 또는 아래)를 가지면** 그 정점의 순위는 확정된다.
> 12. **강한 연결 요소(SCC)로 사이클을 압축하면 항상 DAG가 된다.** 사이클이 있는 그래프도 SCC 단위로 묶으면(condensation) DAG가 되어 위상 정렬이 가능하다. 코테 상급(타잔·코사라주) 주제지만 "사이클 있어도 위상 정렬 쓰는 법"의 정답이다.
> 13. **정렬(sorting)과 이름만 같다.** 비교 함수도, 안정성(stability)도, O(n log n) 하한도 이 문제와 무관하다. "제약 만족 나열"로 이해하라.

> [!example]- 예제 코드 (Examples)
> ```python
> from collections import deque
> import heapq
>
>
> # ---- (1) 칸 알고리즘: 위상 순서 + 사이클 판별 ----
> def topo_kahn(n, edges):
>     """edges = [(u, v), ...] 는 u -> v (u 를 먼저 한다).
>        반환: 위상 순서 리스트, 사이클이면 None"""
>     adj = [[] for _ in range(n)]
>     indeg = [0] * n
>     for u, v in edges:
>         adj[u].append(v)
>         indeg[v] += 1                      # 진입 차수는 '나중' 쪽에!
>
>     q = deque(v for v in range(n) if indeg[v] == 0)   # 고립 정점도 포함
>     order = []
>     while q:
>         u = q.popleft()
>         order.append(u)
>         for v in adj[u]:
>             indeg[v] -= 1                  # 빚 하나 갚기
>             if indeg[v] == 0:
>                 q.append(v)
>     return order if len(order) == n else None          # 길이 검사 필수
>
>
> # ---- (2) 사전 순 최소 위상 순서: 큐 대신 최소 힙 ----
> def topo_smallest(n, edges):
>     adj = [[] for _ in range(n)]
>     indeg = [0] * n
>     for u, v in edges:
>         adj[u].append(v)
>         indeg[v] += 1
>
>     heap = [v for v in range(n) if indeg[v] == 0]
>     heapq.heapify(heap)
>     order = []
>     while heap:
>         u = heapq.heappop(heap)            # 가능한 것 중 최소 번호
>         order.append(u)
>         for v in adj[u]:
>             indeg[v] -= 1
>             if indeg[v] == 0:
>                 heapq.heappush(heap, v)
>     return order if len(order) == n else None
>
>
> # ---- (3) DFS 기반: post-order 역순 + 3색 사이클 판별 ----
> WHITE, GRAY, BLACK = 0, 1, 2
>
> def topo_dfs(n, edges):
>     adj = [[] for _ in range(n)]
>     for u, v in edges:
>         adj[u].append(v)
>
>     state = [WHITE] * n
>     out = []
>     has_cycle = False
>
>     def visit(u):
>         nonlocal has_cycle
>         state[u] = GRAY                    # 재귀 스택 위에 있음
>         for v in adj[u]:
>             if state[v] == GRAY:           # back edge -> 사이클
>                 has_cycle = True
>                 return
>             if state[v] == WHITE:
>                 visit(v)
>                 if has_cycle:
>                     return
>         state[u] = BLACK
>         out.append(u)                      # 되돌아 나오는 순간 기록
>
>     for s in range(n):
>         if state[s] == WHITE:
>             visit(s)
>             if has_cycle:
>                 return None
>     return out[::-1]                       # 뒤집어야 위상 순서
>
>
> # ---- (4) 위상 순서가 유일한가: 큐 크기가 항상 1 ----
> def topo_is_unique(n, edges):
>     adj = [[] for _ in range(n)]
>     indeg = [0] * n
>     for u, v in edges:
>         adj[u].append(v)
>         indeg[v] += 1
>     q = deque(v for v in range(n) if indeg[v] == 0)
>     seen = 0
>     while q:
>         if len(q) > 1:                     # 선택지가 2개 이상 -> 답이 여럿
>             return False
>         u = q.popleft()
>         seen += 1
>         for v in adj[u]:
>             indeg[v] -= 1
>             if indeg[v] == 0:
>                 q.append(v)
>     return seen == n                       # 사이클이면 False
>
>
> # ---- (5) DAG 최장 경로 DP = 작업 완료 최소 시간 (critical path) ----
> def dag_min_finish_time(n, edges, time):
>     """time[i] = 작업 i 소요 시간. 선행 작업이 끝나야 시작 가능."""
>     adj = [[] for _ in range(n)]
>     indeg = [0] * n
>     for u, v in edges:
>         adj[u].append(v)
>         indeg[v] += 1
>
>     finish = [0] * n
>     q = deque()
>     for v in range(n):
>         if indeg[v] == 0:
>             finish[v] = time[v]            # 선행 없음 -> 즉시 시작
>             q.append(v)
>
>     done = 0
>     while q:
>         u = q.popleft()
>         done += 1
>         for v in adj[u]:
>             # u 를 꺼낸 시점에 finish[u] 는 이미 확정값이다
>             finish[v] = max(finish[v], finish[u] + time[v])
>             indeg[v] -= 1
>             if indeg[v] == 0:
>                 q.append(v)
>     return max(finish) if done == n else -1   # -1 = 사이클
> ```
>
> 전체 실행 가능한 예제(칸 레벨 순회·역방향 그래프·모든 위상 순서 열거·잎 소거로 트리 중심 찾기 포함): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> **사이클 판별 → 순서 출력 → 기출 부분 순서 → 역방향 소거 → DAG DP → 잎 소거** 순으로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Course Schedule | [LeetCode #207](https://leetcode.com/problems/course-schedule/) | 🟡중급 | 위상 정렬 가능성 = DAG 사이클 판별 |
> | 2 | Course Schedule II | [LeetCode #210](https://leetcode.com/problems/course-schedule-ii/) | 🟡중급 | 위상 순서 출력(칸 vs DFS) |
> | 3 | 순위 | [프로그래머스 #49191](https://school.programmers.co.kr/learn/courses/30/lessons/49191) | ⚫기출 | 부분 순서·도달 가능성으로 순위 확정(Level 3) |
> | 4 | Find Eventual Safe States | [LeetCode #802](https://leetcode.com/problems/find-eventual-safe-states/) | 🔴심화 | 역방향 그래프 위상 소거(out-degree 0부터) |
> | 5 | Parallel Courses III | [LeetCode #2050](https://leetcode.com/problems/parallel-courses-iii/) | 🔴심화 | 위상 순서 위 DP = DAG 최장 경로 |
> | 6 | Minimum Height Trees | [LeetCode #310](https://leetcode.com/problems/minimum-height-trees/) | 🔴심화 | 잎 소거(degree 1 peeling)로 트리 중심 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 간선 방향 결정 요령, 칸과 DFS 3색의 구현 비교, 순위 문제를 플로이드-워셜 전이 폐쇄와 양방향 DFS 두 가지로 푸는 법, 역방향 그래프로 뒤집는 사고, 위상 순서 위 DP 점화식, 잎 소거의 종료 조건(남은 정점 ≤ 2), 프로그래머스/LeetCode 시그니처별 구현과 복잡도 비교: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-37-mst/concept|Day 37 — 최소 신장 트리 (MST: Kruskal·Prim)]] — MST가 **무방향** 그래프에서 "전부 잇는 최소 골격"을 다뤘다면, 위상 정렬은 **방향** 그래프에서 "모순 없는 순서"를 다룬다. 둘 다 "사이클 회피"가 핵심이지만 목적이 정반대다
- ➡️ **다음(next):** [[day-39-trie/concept|Day 39 — 트라이 (Trie)]] — 그래프 계열을 마치고 문자열 전용 자료구조로 넘어간다. 접두사 검색·자동완성의 기본기
- 🧭 **관련(related):**
  - [[day-26-bfs/concept|Day 26 — BFS (너비 우선 탐색)]] — 칸 알고리즘은 BFS 골격 그대로다. `visited` 대신 `indegree`, "처음 만나면 push" 대신 "빚이 0이면 push"
  - [[day-25-dfs/concept|Day 25 — DFS (깊이 우선 탐색)]] — DFS 기반 위상 정렬의 post-order 역순 트릭과 3색 사이클 판별의 근거
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 인접 리스트와 진입 차수 배열을 간선 목록에서 만드는 전처리가 모든 위상 정렬의 시작점
  - [[day-31-dp/concept|Day 31 — 동적 계획법 입문]] — 위상 순서는 "DP를 어떤 순서로 계산할지"를 그래프에서 뽑아내는 도구. DAG DP가 O(V+E)로 성립하는 이유
  - [[day-35-bellman-floyd/concept|Day 35 — 벨만-포드·플로이드-워셜]] — DAG면 음수 간선이 있어도 위상 순서 한 번 훑기로 최단 경로가 끝난다. 프로그래머스 #49191의 전이 폐쇄도 플로이드로 푼다
  - [[day-08-queue-deque/concept|Day 08 — 큐와 덱]] — 칸 알고리즘의 `deque`. "지금 할 수 있는 작업 대기열"이라는 의미가 그대로 드러난다
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — 큐를 최소 힙으로 바꾸면 사전 순 최소 위상 순서가 나온다
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]
