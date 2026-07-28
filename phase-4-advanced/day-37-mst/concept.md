---
day: 37
phase: 4-advanced
title: 최소 신장 트리 (MST: Kruskal·Prim)
category: [그래프, 최소 신장 트리, MST, 크루스칼, 프림, 그리디, Union-Find]
difficulty: 중급
status: done
prev: "[[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find / Disjoint Set)]]"
next: "[[day-38-topological-sort/concept|Day 38 — 위상 정렬 (Topological Sort)]]"
related:
  - "[[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find / Disjoint Set)]]"
  - "[[day-34-dijkstra/concept|Day 34 — 최단 경로: 다익스트라 (Dijkstra)]]"
  - "[[day-21-greedy/concept|Day 21 — 그리디 (Greedy)]]"
  - "[[day-12-heap/concept|Day 12 — 힙·우선순위 큐]]"
  - "[[day-17-sorting/concept|Day 17 — 정렬 (Sorting)]]"
  - "[[day-28-graph/concept|Day 28 — 그래프 표현과 순회]]"
  - "[[day-38-topological-sort/concept|Day 38 — 위상 정렬 (Topological Sort)]]"
sources:
  - https://leetcode.com/problems/min-cost-to-connect-all-points/
  - https://school.programmers.co.kr/learn/courses/30/lessons/42861
  - https://school.programmers.co.kr/learn/courses/30/lessons/86971
  - https://leetcode.com/problems/path-with-minimum-effort/
  - https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/
  - https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/
  - https://en.wikipedia.org/wiki/Minimum_spanning_tree
  - https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
  - https://en.wikipedia.org/wiki/Prim%27s_algorithm
tags: [phase/4, topic/mst, topic/kruskal, topic/prim, topic/greedy, topic/graph, topic/union-find]
---

# Day 37 — 최소 신장 트리 (MST: Kruskal·Prim)

> [!abstract] 한눈 요약 (TL;DR)
> **신장 트리(spanning tree)** 는 그래프의 **모든 정점을 포함하면서 사이클이 없는** 부분 그래프다 — 정점이 V개면 간선은 정확히 **V−1개**. 그중 **간선 가중치 합이 최소**인 것이 **최소 신장 트리(MST, Minimum Spanning Tree)** 다. 한 문장으로: **"모든 지점을 가장 싸게 하나로 잇는 방법"**. 도로·전력망·통신망 건설 비용 최소화가 원형 문제다. 구하는 방법은 두 가지 그리디 알고리즘이다 — **크루스칼(Kruskal)**: 간선을 **가중치 오름차순으로 정렬**해 훑으며 **사이클을 만들지 않는 간선만 채택**한다([[day-36-union-find/concept|Union-Find(Day 36)]]로 사이클 판별). **프림(Prim)**: 시작 정점 하나에서 출발해 **현재 트리에 붙는 가장 싼 간선**을 계속 흡수하며 트리를 키운다([[day-12-heap/concept|힙(Day 12)]]으로 최소 간선 선택). 복잡도는 크루스칼 **O(E log E)**, 프림(힙) **O(E log V)** — 희소 그래프(sparse)엔 크루스칼, 밀집 그래프(dense)엔 프림 O(V²)가 유리하다. [[day-34-dijkstra/concept|다익스트라(Day 34)]]와 코드가 소름 돋게 닮았지만 **답하는 질문이 완전히 다르다**: 다익스트라는 "**시작점에서 각 정점까지**의 최단 거리", MST는 "**전체를 잇는** 총비용 최소". 그래서 **MST는 음수 가중치도 아무 문제 없다.** 핵심 한 줄: **"싼 간선부터, 사이클만 피해서 V−1개."**

> [!note]- 1. 정의와 직관 (Definition & Intuition)
> **신장 트리부터.** 연결된 무방향 그래프 G=(V,E)의 **신장 트리**는 (1) **모든 정점을 포함**하고, (2) **사이클이 없고**, (3) **연결되어 있는** 부분 그래프다. 이 세 조건이 모이면 간선 수는 자동으로 **정확히 V−1개**가 된다. 하나라도 빼면 끊어지고(연결 실패), 하나라도 더하면 사이클이 생긴다. 그래서 신장 트리는 **"끊어지지 않는 최소한의 골격"** 이다.
>
> **MST.** 간선마다 가중치(비용)가 있을 때, 가능한 신장 트리 중 **가중치 합이 가장 작은 것**이 MST다. 신장 트리는 보통 여러 개 존재하고, MST도 (가중치가 겹치면) 여러 개일 수 있다. 다만 **최소 비용 값 자체는 항상 유일**하다.
>
> **일상 비유 — 마을에 수도관 깔기.** 마을 5곳에 물을 보내야 한다. 두 마을을 잇는 관마다 공사비가 다르다. 목표는 **모든 마을에 물이 닿게**(=연결) 하면서 **총 공사비 최소**. 여기서 순환하는 관로를 깔면? 물은 이미 닿는데 돈만 더 쓴 것이다 — 그게 **사이클 = 낭비**다. 그래서 답은 항상 트리 모양이고, 관은 정확히 (마을 수 − 1)개다.
>
> **왜 그리디가 통하는가.** MST는 "싼 것부터 집으면 최적"이 **증명되는 드문 문제**다. 근거는 **컷 성질(cut property)**: 정점을 임의의 두 그룹으로 갈랐을 때, **두 그룹을 잇는 간선 중 가장 싼 것은 반드시 어떤 MST에 포함된다.** 뒤집으면 **사이클 성질(cycle property)**: **어떤 사이클에서 가장 비싼 간선은 MST에 절대 안 들어간다.** 크루스칼은 사이클 성질을(비싼 간선을 사이클이라 버림), 프림은 컷 성질을(트리와 나머지를 가르는 컷에서 최소 간선을 채택) 각각 곧바로 실행하는 알고리즘이다. [[day-21-greedy/concept|그리디(Day 21)]]가 "국소 최적 = 전역 최적"으로 성립하는 교과서 사례다.
>
> **두 알고리즘의 성격 차이.** 크루스칼은 **간선 중심(edge-based)** 이라 처음엔 조각난 숲(forest)들이 흩어져 있다가 마지막에 하나로 합쳐진다. 프림은 **정점 중심(vertex-based)** 이라 항상 **연결된 트리 하나**를 유지하며 몸집을 불린다. 결과(최소 비용)는 같지만 중간 과정의 모양이 다르다.

> [!gear]- 2. 동작 원리 (How It Works)
> **예제 그래프** (정점 0~5, 간선 7개):
> ```
>         4
>    0 ------- 1              간선 목록 (a, b, w)
>    |       / |              (0,1,4) (0,2,3) (1,2,1)
>  3 |   1 /   | 2            (1,3,2) (2,3,4) (3,4,2)
>    |   /     |              (4,5,6)
>    2 ------- 3 ---- 4 ---- 5
>         4      2       6
> ```
>
> **(A) 크루스칼 (Kruskal) — 간선을 싼 순서로, 사이클만 피한다.**
> ```
> 1) 모든 간선을 가중치 오름차순 정렬
> 2) 앞에서부터 훑으며 union(a, b) 시도
>    - 성공(다른 그룹이었음) -> MST에 채택
>    - 실패(이미 같은 그룹)  -> 사이클! 버린다
> 3) 채택 간선이 V-1 개가 되면 조기 종료
> ```
> ```
> 정렬: (1,2,1) (1,3,2) (3,4,2) (0,2,3) (0,1,4) (2,3,4) (4,5,6)
>
> (1,2,1) union OK  -> 채택  누적 1   그룹 {1,2}
> (1,3,2) union OK  -> 채택  누적 3   그룹 {1,2,3}
> (3,4,2) union OK  -> 채택  누적 5   그룹 {1,2,3,4}
> (0,2,3) union OK  -> 채택  누적 8   그룹 {0,1,2,3,4}
> (0,1,4) union 실패 -> 버림 (0,1 이미 같은 그룹 = 사이클)
> (2,3,4) union 실패 -> 버림
> (4,5,6) union OK  -> 채택  누적 14  그룹 {0..5}  <- 간선 5개 = V-1, 종료
>
> MST 비용 = 14,  MST 간선 = (1,2) (1,3) (3,4) (0,2) (4,5)
> ```
> [[day-36-union-find/concept|Day 36]]에서 배운 `union`의 반환값(False = 이미 같은 그룹 = 사이클)이 **그대로 채택 여부 판정기**로 쓰인다. 이게 크루스칼의 심장이다.
>
> **(B) 프림 (Prim) — 트리를 한 정점씩 키운다.**
> ```
> 1) 아무 정점(예: 0)에서 시작. 트리 T = {0}
> 2) T와 T 밖을 잇는 간선 중 최소 가중치 간선을 골라
>    그 바깥 정점을 T에 흡수 (최소 힙으로 고름)
> 3) T가 모든 정점을 포함할 때까지 반복 (V-1 회)
> ```
> ```
> T={0}         후보 간선: (0,1,4) (0,2,3)          -> 최소 3 : 정점 2 흡수
> T={0,2}       후보: (0,1,4) (1,2,1) (2,3,4)       -> 최소 1 : 정점 1 흡수  누적 4
> T={0,1,2}     후보: (1,3,2) (2,3,4) (0,1,4)x      -> 최소 2 : 정점 3 흡수  누적 6
> T={0,1,2,3}   후보: (3,4,2) (2,3,4)x              -> 최소 2 : 정점 4 흡수  누적 8
> T={0..4}      후보: (4,5,6)                       -> 최소 6 : 정점 5 흡수  누적 14
>
> MST 비용 = 14  (크루스칼과 동일! 간선 구성도 이 그래프에선 같음)
> ```
> **핵심 구현 포인트:** 힙에서 꺼낸 간선의 도착 정점이 **이미 트리에 있으면 버린다**(`if visited[v]: continue`). 이 한 줄이 프림의 사이클 방지다. Union-Find가 필요 없다.
>
> **(C) 왜 사이클을 피하면 되는가 — 사이클 성질.**
> ```
>   1 --1-- 2        사이클 1-2-3-1 의 간선: 1, 2, 4
>    \      |        가장 비싼 (2,3,4) 를 빼도 1-2-3 은 여전히 연결.
>     2     4        => 사이클의 최대 간선은 MST에 절대 필요 없다.
>      \    |        크루스칼은 이 간선을 만날 때 이미 두 끝이 연결돼
>        \  |        있으므로 자연히 버려진다.
>          3
> ```
>
> **(D) 밀집 그래프용 프림 O(V²) — 힙 없이 배열로.**
> ```
> dist[v] = 트리에서 v 까지 붙는 최소 간선 비용 (초기 INF, dist[start]=0)
> V 번 반복:
>     아직 안 쓴 정점 중 dist 최소인 u 를 선형 탐색으로 고름   # O(V)
>     u 를 트리에 넣고 total += dist[u]
>     u 의 모든 이웃 v 에 대해 dist[v] = min(dist[v], w(u,v))  # O(V)
> ```
> 간선이 V² 급으로 많은 완전 그래프(예: 좌표 n개를 서로 연결)에서는 힙 버전보다 이 **O(V²)** 버전이 오히려 빠르고 메모리도 적다.
>
> 실행 가능한 전체 코드: [examples.py](examples.py)

> [!chart]- 3. 복잡도 (Time / Space Complexity)
> [[day-16-big-o/concept|Big-O(Day 16)]] 기준. V=정점 수, E=간선 수. α는 역아커만 함수(사실상 상수).
>
> | 알고리즘 | 시간복잡도 | 공간 | 유리한 상황 |
> |---|---|---|---|
> | **크루스칼 (정렬 + Union-Find)** | **O(E log E)** | O(V+E) | **희소 그래프**(E ≈ V), 간선 목록으로 입력이 주어질 때 |
> | 크루스칼 (간선이 이미 정렬됨) | O(E·α(V)) ≈ O(E) | O(V+E) | 가중치가 작은 정수라 계수 정렬 가능할 때 |
> | **프림 (이진 힙)** | **O(E log V)** | O(V+E) | 중간 밀도. 인접 리스트 입력 |
> | **프림 (인접 행렬, 힙 없음)** | **O(V²)** | O(V) 또는 O(V²) | **밀집/완전 그래프**(E ≈ V²) |
> | 프림 (피보나치 힙) | O(E + V log V) | O(V+E) | 이론용. 코테에선 안 씀 |
> | 사이클 판별 1회(Union-Find) | O(α(V)) ≈ O(1) | — | 크루스칼 내부 |
>
> > **정렬이 크루스칼의 병목이다.** `E log E`의 log는 **정렬**에서 나온다. Union-Find 부분은 O(E·α)로 사실상 선형이라 무시된다. 즉 크루스칼 = **"정렬 비용 + 공짜"**. [[day-17-sorting/concept|정렬(Day 17)]]이 그대로 성능을 결정한다.
> >
> > **E와 V의 관계로 갈린다.** 무방향 그래프에서 E ≤ V(V−1)/2. `log E ≤ log V² = 2 log V`이므로 **O(E log E)와 O(E log V)는 사실 같은 급**이다. 실전 선택 기준은 상수와 입력 형태다 — **간선 리스트로 주어지면 크루스칼**(정렬만 하면 끝), **인접 리스트/행렬이고 밀집이면 프림**. 특히 좌표 n개를 완전 연결하는 문제(LeetCode 1584)는 E = n²/2라 **프림 O(n²)** 가 크루스칼 **O(n² log n)** 보다 확실히 빠르다.
> >
> > **조기 종료로 절약.** 크루스칼은 채택 간선이 V−1개가 되면 남은 간선을 볼 필요가 없다. 정렬 자체는 여전히 O(E log E)지만 union 호출은 줄어든다.
> >
> > **MST 총비용 vs 최단 경로.** 둘을 혼동하면 복잡도 감각도 무너진다. 다익스트라도 O(E log V)지만 **답은 거리 배열**이고, MST는 **간선 집합**이다. 같은 그래프에서 "MST 위의 경로"가 최단 경로일 필요는 **전혀 없다**.

> [!tip]- 💡 이해를 돕는 팁 (Tips)
> - **암기 문장 두 개면 끝.** 크루스칼 = **"싼 간선부터, 사이클이면 패스"**. 프림 = **"내 트리에 가장 싸게 붙는 정점부터 흡수"**. ([MST 위키](https://en.wikipedia.org/wiki/Minimum_spanning_tree))
> - **크루스칼은 Day 36 코드 재활용이다.** [[day-36-union-find/concept|Union-Find]] 템플릿 + `edges.sort()` + `if dsu.union(a,b): total += w` 세 줄. 새로 외울 게 거의 없다. ([Kruskal 위키](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm))
> - **프림은 다익스트라에서 한 글자만 바꾼 것.** 힙에 넣는 값이 다익스트라는 `dist[u] + w`(누적 거리), 프림은 **`w`(간선 하나의 값)** 이다. 이 차이 하나가 "경로 최단"과 "전체 연결 최소"를 가른다. ([Prim 위키](https://en.wikipedia.org/wiki/Prim%27s_algorithm))
> - **"최대 신장 트리"는 정렬만 뒤집는다.** 가중치 **내림차순**으로 크루스칼을 돌리면 최대 신장 트리다. 또는 모든 가중치에 −1을 곱해도 된다(MST는 음수 OK라서 가능).
> - **최소 병목 경로(minimax path)는 MST가 공짜로 준다.** "경로상 **최대 간선을 최소화**"하는 문제(LeetCode 1631 등)는 크루스칼을 돌리다 **출발·도착이 처음 연결되는 순간의 간선 가중치**가 답이다. MST는 자동으로 **최소 병목 신장 트리(minimum bottleneck spanning tree)** 이기도 하다.
> - **완전 그래프는 간선을 다 만들지 말고 프림 O(V²).** 좌표 n=1000이면 간선 약 50만 개 → 리스트 생성·정렬 자체가 부담. `dist[]` 배열 프림이 메모리·속도 모두 유리하다.
> - **간선을 강제로 포함/제외하기.** "이 간선은 반드시 쓴다"면 먼저 `union`하고 비용에 더한 뒤 크루스칼 진행. "제외"면 순회에서 건너뛴다. LeetCode 1489(critical / pseudo-critical 판별)가 정확히 이 두 트릭이다.
> - **오프라인 쿼리 + 크루스칼.** "가중치 L 미만 간선만 써서 두 정점이 연결되나?" 류(LeetCode 1697)는 **쿼리를 L 오름차순으로 정렬**해 간선을 점진적으로 union하며 답한다. 간선을 한 번만 훑어 O(E log E + Q log Q).

> [!warning]- ⚠️ 개발자 필수 상식 (Must-Know)
> 1. **MST는 무방향 그래프(undirected) 전용이다.** 방향 그래프의 대응 개념은 **최소 신장 수형도(arborescence)** 이고 Chu-Liu/Edmonds 알고리즘이 필요하다 — 크루스칼·프림을 방향 그래프에 그대로 쓰면 **틀린다**. 코테 범위 밖이지만 "MST는 무방향"은 반드시 기억.
> 2. **그래프가 연결되어 있지 않으면 MST는 존재하지 않는다.** 이때 결과는 **최소 신장 숲(minimum spanning forest)** 이다. 구현에서는 **채택 간선 수가 V−1인지** 또는 `dsu.count == 1`인지 확인해 `-1`/불가능을 반환해야 한다. 이 검사를 빼먹는 게 가장 흔한 오답.
> 3. **음수 가중치는 아무 문제 없다.** [[day-34-dijkstra/concept|다익스트라(Day 34)]]는 음수 간선에서 깨지지만, MST는 "간선 V−1개를 고르는 문제"이므로 음수여도 정렬 순서만 지키면 정확하다. 음수 간선은 오히려 무조건 먼저 채택된다.
> 4. **MST 위의 경로는 최단 경로가 아니다.** 정말 자주 틀리는 지점이다. MST는 **전체 합**을 최소화하고 두 정점 간 거리는 보장하지 않는다. "A에서 B까지 최단"을 물으면 다익스트라, "전부 잇는 최소 비용"이면 MST.
> 5. **MST의 최소 비용은 유일하지만 MST 자체는 유일하지 않을 수 있다.** 같은 가중치 간선이 있으면 서로 다른 MST가 여럿 나온다. **모든 간선 가중치가 서로 다르면 MST는 유일**하다. "MST가 유일한가?"를 묻는 문제는 각 MST 간선을 하나씩 빼고 다시 돌려 비용이 커지는지 본다.
> 6. **크루스칼에서 `union` 전에 root 비교를 빼먹지 마라.** `parent[a] = b`로 원소를 직접 붙이면 그룹 전체가 안 합쳐진다. 반드시 `find(a)`, `find(b)` 결과끼리 연결한다([[day-36-union-find/concept|Day 36]] 최다 버그).
> 7. **프림에서 `visited` 검사 위치가 핵심.** 힙에서 **꺼낸 직후** `if visited[v]: continue`로 걸러야 한다. 넣을 때만 검사하면 같은 정점이 여러 번 트리에 편입되어 비용이 부풀거나 간선 수가 V−1을 넘는다. 다익스트라의 "낡은 항목 스킵"과 같은 패턴이다.
> 8. **간선 정렬 키는 가중치가 먼저다.** 튜플을 `(a, b, w)` 순으로 담아 `sort()` 하면 **정점 번호로 정렬**되어 완전히 틀린다. `(w, a, b)`로 담거나 `key=lambda e: e[2]`를 반드시 지정한다. 조용한 오답의 대표.
> 9. **1-based / 0-based 혼동.** 문제가 정점을 1..n으로 주면 `parent` 크기를 n+1로 잡고 0번은 버린다. 프로그래머스 문제(42861, 86971)에서 자주 밟는 지뢰다.
> 10. **중복 간선(multi-edge)·자기 루프(self-loop)는 그냥 둬도 된다.** 크루스칼은 비싼 중복을 사이클로 걸러내고, 자기 루프는 `find(a)==find(a)`라 항상 버려진다. 굳이 전처리하지 않아도 정답이 나온다.
> 11. **면접 단골: "왜 그리디가 최적인가?"** 답은 **컷 성질(cut property)** — 임의의 컷을 건너는 최소 간선은 어떤 MST에 반드시 포함된다. 이걸 반복 적용하면 크루스칼·프림의 정당성이 증명된다. "교환 논법(exchange argument)"으로 설명하면 만점.
> 12. **간선 삭제형 문제는 역순 union.** Union-Find는 분리를 못 하므로, "간선을 하나씩 제거하며 연결성 추적"은 **모든 삭제를 거꾸로 재생(추가)** 하는 오프라인 트릭으로 푼다.

> [!example]- 예제 코드 (Examples)
> ```python
> import heapq
>
> class DSU:                                  # Day 36 템플릿 재사용
>     def __init__(self, n):
>         self.parent = list(range(n))
>         self.size = [1] * n
>         self.count = n
>
>     def find(self, x):
>         root = x
>         while self.parent[root] != root:
>             root = self.parent[root]
>         while self.parent[x] != root:        # 경로 압축
>             self.parent[x], x = root, self.parent[x]
>         return root
>
>     def union(self, a, b):
>         ra, rb = self.find(a), self.find(b)
>         if ra == rb:
>             return False                     # 사이클 -> 채택 불가
>         if self.size[ra] < self.size[rb]:
>             ra, rb = rb, ra
>         self.parent[rb] = ra
>         self.size[ra] += self.size[rb]
>         self.count -= 1
>         return True
>
>
> # ---- 크루스칼: 간선 리스트 [(a, b, w), ...] -> (총비용, MST 간선) ----
> def kruskal(n, edges):
>     dsu = DSU(n)
>     total, picked = 0, []
>     for a, b, w in sorted(edges, key=lambda e: e[2]):   # 가중치 오름차순!
>         if dsu.union(a, b):                  # 사이클 아니면 채택
>             total += w
>             picked.append((a, b, w))
>             if len(picked) == n - 1:         # V-1 개 모이면 종료
>                 break
>     if len(picked) != n - 1:                 # 연결 불가 -> MST 없음
>         return None, []
>     return total, picked
>
>
> # ---- 프림(힙): 인접 리스트 adj[u] = [(v, w), ...] ----
> def prim(n, adj, start=0):
>     visited = [False] * n
>     heap = [(0, start)]                      # (간선 비용, 정점)
>     total, cnt = 0, 0
>     while heap and cnt < n:
>         w, u = heapq.heappop(heap)
>         if visited[u]:                       # 꺼낸 직후 검사가 핵심
>             continue
>         visited[u] = True
>         total += w
>         cnt += 1
>         for v, cost in adj[u]:
>             if not visited[v]:
>                 heapq.heappush(heap, (cost, v))
>         # 주의: 힙에 넣는 값은 cost(간선 하나)다.
>         #       다익스트라처럼 dist[u]+cost 를 넣으면 안 된다!
>     return total if cnt == n else None        # None = 연결 불가
>
>
> # ---- 최소 병목 경로: s~t 가 처음 연결되는 간선의 가중치 ----
> def bottleneck(n, edges, s, t):
>     dsu = DSU(n)
>     for a, b, w in sorted(edges, key=lambda e: e[2]):
>         dsu.union(a, b)
>         if dsu.find(s) == dsu.find(t):       # 방금 연결됨 -> 이 w 가 답
>             return w
>     return None
> ```
>
> 전체 실행 가능한 예제(최대 신장 트리·MST 유일성 판정·완전 그래프 프림 O(V²) 포함): [examples.py](examples.py)

> [!question]- 연습문제 (Problems)
> **MST 기본 → 기출 크루스칼 → 신장 트리 분할 → 병목 → 오프라인 쿼리 → critical 간선** 순으로 배치했다. 출처는 프로그래머스/LeetCode만 사용한다.
>
> | # | 문제 | 출처 | 난이도 | 유형 |
> |---|---|---|---|---|
> | 1 | Min Cost to Connect All Points | [LeetCode #1584](https://leetcode.com/problems/min-cost-to-connect-all-points/) | 🟡중급 | MST 기본(완전 그래프, Kruskal vs Prim) |
> | 2 | 섬 연결하기 | [프로그래머스 #42861](https://school.programmers.co.kr/learn/courses/30/lessons/42861) | ⚫기출 | 크루스칼 정석(Level 3) |
> | 3 | 전력망을 둘로 나누기 | [프로그래머스 #86971](https://school.programmers.co.kr/learn/courses/30/lessons/86971) | ⚫기출 | 신장 트리 간선 제거 + 컴포넌트 크기 |
> | 4 | Path With Minimum Effort | [LeetCode #1631](https://leetcode.com/problems/path-with-minimum-effort/) | 🔴심화 | 최소 병목 경로(minimax) |
> | 5 | Checking Existence of Edge Length Limited Paths | [LeetCode #1697](https://leetcode.com/problems/checking-existence-of-edge-length-limited-paths/) | 🔴심화 | 오프라인 쿼리 + 점진적 union |
> | 6 | Find Critical and Pseudo-Critical Edges in MST | [LeetCode #1489](https://leetcode.com/problems/find-critical-and-pseudo-critical-edges-in-minimum-spanning-tree/) | 🔴심화 | 간선 강제 제외/포함으로 MST 재계산 |
>
> 전체 문제 설명 및 힌트: [problems.md](problems.md)

> [!check]- 해설 (Solutions)
> 각 문제의 MST 모델링(좌표 완전 그래프·간선 리스트·격자 셀 1차원화), 크루스칼과 프림 O(V²)의 비교, 병목 경로를 이분 탐색 대신 union으로 푸는 법, 오프라인 쿼리 정렬, 간선 강제 포함/제외 트릭, 프로그래머스/LeetCode 시그니처별 구현과 다중 접근: [solutions.py](solutions.py)

---

## 🔗 관계 (Relationships)

- ⬅️ **이전(prev):** [[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find / Disjoint Set)]] — 어제 만든 `union`의 반환값(사이클 판별)이 오늘 크루스칼의 채택 판정기로 그대로 쓰인다. Day 36 없이는 크루스칼이 성립하지 않는다
- ➡️ **다음(next):** [[day-38-topological-sort/concept|Day 38 — 위상 정렬 (Topological Sort)]] — MST가 무방향 그래프의 골격을 다뤘다면, 위상 정렬은 **방향 그래프(DAG)** 의 순서를 다룬다. 선후 관계·의존성 해결의 기본기
- 🧭 **관련(related):**
  - [[day-36-union-find/concept|Day 36 — 서로소 집합 (Union-Find)]] — 크루스칼의 부품. 사이클 판별과 연결 요소 관리를 O(α)로 처리
  - [[day-34-dijkstra/concept|Day 34 — 최단 경로: 다익스트라]] — 프림과 코드가 거의 같다. 힙에 `dist[u]+w`를 넣는가 `w`를 넣는가가 두 알고리즘을 가르는 유일한 차이
  - [[day-21-greedy/concept|Day 21 — 그리디]] — "국소 최적 = 전역 최적"이 컷 성질로 증명되는 대표 사례. 그리디 정당성 증명의 교과서
  - [[day-12-heap/concept|Day 12 — 힙·우선순위 큐]] — 프림이 매 단계 최소 간선을 O(log V)로 뽑는 도구
  - [[day-17-sorting/concept|Day 17 — 정렬]] — 크루스칼의 O(E log E)는 사실상 정렬 비용. 정렬 키를 `(w, a, b)`로 잡는 감각이 오답을 막는다
  - [[day-28-graph/concept|Day 28 — 그래프 표현과 순회]] — 간선 리스트/인접 리스트/인접 행렬 중 어떤 표현으로 입력이 오는지가 크루스칼·프림 선택을 결정
- 🗺️ **지도(MOC):** [[Phase-4 MOC]] · [[00 Algorithm MOC]]
