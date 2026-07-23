# -*- coding: utf-8 -*-
"""
Day 34 - 최단 경로: 다익스트라 (Dijkstra) 예제

핵심 골격 5종:
  (1) 다익스트라 - 우선순위 큐 (인접 리스트)
  (2) 경로 복원 (parent 추적)
  (3) BFS - 모든 간선 가중치 1일 때의 최단 경로 (힙 불필요, 대비용)
  (4) minimax 변형 - 경로상 최대 간선을 최소화
  (5) 다익스트라 - 배열 스캔 O(V^2) (힙 없이, 밀집 그래프용)

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python examples.py
"""

import heapq
from collections import deque

INF = float("inf")


# ---------------------------------------------------------------------------
# (1) 다익스트라 - 우선순위 큐 (인접 리스트, 1-indexed)
#     graph[u] = [(v, w), ...]   w >= 0
# ---------------------------------------------------------------------------
def dijkstra(graph, start, n):
    dist = [INF] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]                     # (거리, 정점)
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:                   # 낡은 항목 -> 지연 삭제(lazy deletion)
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:              # 완화(relaxation)
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


# ---------------------------------------------------------------------------
# (2) 경로 복원 - parent 배열로 실제 최단 경로까지 재구성
# ---------------------------------------------------------------------------
def dijkstra_path(graph, start, end, n):
    dist = [INF] * (n + 1)
    parent = [-1] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    if dist[end] == INF:
        return INF, []
    path, cur = [], end
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    return dist[end], path[::-1]


# ---------------------------------------------------------------------------
# (3) BFS - 모든 간선 가중치가 1이면 이게 곧 최단 경로 (힙 불필요)
#     graph[u] = [v, ...]
# ---------------------------------------------------------------------------
def bfs_shortest(graph, start, n):
    dist = [-1] * (n + 1)
    dist[start] = 0
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


# ---------------------------------------------------------------------------
# (4) minimax 변형 - 경로상 "최대 간선"을 최소화 (합이 아니라 max 누적)
# ---------------------------------------------------------------------------
def dijkstra_minimax(graph, start, n):
    worst = [INF] * (n + 1)
    worst[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > worst[u]:
            continue
        for v, w in graph[u]:
            nd = max(d, w)                # 핵심: 합(+) 대신 최댓값(max)
            if nd < worst[v]:
                worst[v] = nd
                heapq.heappush(pq, (nd, v))
    return worst


# ---------------------------------------------------------------------------
# (5) 다익스트라 - 배열 스캔 O(V^2) (힙 없이). 밀집 그래프(E ~ V^2)에 유리.
# ---------------------------------------------------------------------------
def dijkstra_array(graph, start, n):
    dist = [INF] * (n + 1)
    dist[start] = 0
    visited = [False] * (n + 1)
    for _ in range(n):
        # 아직 확정 안 된 정점 중 거리 최소를 선형 탐색
        u, best = -1, INF
        for i in range(1, n + 1):
            if not visited[i] and dist[i] < best:
                best, u = dist[i], i
        if u == -1:
            break
        visited[u] = True
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


def _build_sample():
    """
    예제 그래프 (방향 그래프, 1-indexed):
        1 --4--> 2
        1 --1--> 3
        3 --2--> 2
        3 --1--> 4
        2 --5--> 4
    최단 거리(시작=1): [_, 0, 3, 1, 2]
    """
    n = 4
    edges = [(1, 2, 4), (1, 3, 1), (3, 2, 2), (3, 4, 1), (2, 4, 5)]
    graph = [[] for _ in range(n + 1)]
    for a, b, w in edges:
        graph[a].append((b, w))
    return graph, n


def main():
    print("=" * 60)
    print("Day 34 - Dijkstra 예제 데모")
    print("=" * 60)

    graph, n = _build_sample()

    # (1) 기본 다익스트라
    dist = dijkstra(graph, 1, n)
    print("[1] dijkstra(start=1)   dist[1..4] =", dist[1:])
    print("    기대값                          = [0, 3, 1, 2]")

    # (2) 경로 복원
    cost, path = dijkstra_path(graph, 1, 4, n)
    print("[2] 1 -> 4 최단비용 =", cost, ", 경로 =", path)
    print("    기대: 비용 2, 경로 [1, 3, 4]")

    # (5) 배열 스캔 버전이 힙 버전과 동일한 답
    dist2 = dijkstra_array(graph, 1, n)
    print("[5] dijkstra_array 동일? ", "O" if dist2 == dist else "X")

    # (3) BFS: 가중치 1 그래프
    #   1-2, 1-3, 3-4  (무방향)
    ug = [[] for _ in range(5)]
    for a, b in [(1, 2), (1, 3), (3, 4)]:
        ug[a].append(b)
        ug[b].append(a)
    bdist = bfs_shortest(ug, 1, 4)
    print("[3] BFS(간선=1) dist[1..4] =", bdist[1:], " 기대 [0, 1, 1, 2]")

    # (4) minimax: 경로상 최대 간선 최소화
    #   1 --10--> 2 --10--> 3   (직행)
    #   1 --3-->  4 --3-->  3   (우회지만 최대 간선이 작다)
    mg = [[] for _ in range(5)]
    for a, b, w in [(1, 2, 10), (2, 3, 10), (1, 4, 3), (4, 3, 3)]:
        mg[a].append((b, w))
        mg[b].append((a, w))
    md = dijkstra_minimax(mg, 1, 4)
    print("[4] minimax 1->3 최대간선 =", md[3], " 기대 3 (우회로가 유리)")

    print("=" * 60)
    print("데모 종료")
    print("=" * 60)


if __name__ == "__main__":
    main()
