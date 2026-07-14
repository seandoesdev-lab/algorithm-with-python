# -*- coding: utf-8 -*-
"""
Day 26 - BFS (너비 우선 탐색): 실행 가능한 예제 모음

BFS의 다섯 가지 대표 구현을 담았다:
  (A) 기본 BFS       - 큐(FIFO)로 가까운 것부터 방문
  (B) 최단 거리 BFS  - 처음 도달한 거리가 곧 최단
  (C) 격자 BFS       - 상하좌우 이웃, 최소 이동 횟수
  (D) 다중 소스 BFS  - 여러 출발점에서 동시에 퍼짐
  (E) 레벨 순회 BFS  - 큐를 겹 단위로 끊어 층별 처리

콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from collections import deque


# ===========================================================================
# (A) 기본 BFS (인접 리스트) - 방문 순서 반환
# ===========================================================================
def bfs_order(graph, start):
    visited, order = {start}, []
    q = deque([start])
    while q:
        u = q.popleft()                    # FIFO: 가장 먼저 넣은 것을 꺼냄
        order.append(u)
        for v in graph[u]:
            if v not in visited:
                visited.add(v)             # enqueue 시점에 방문 표시
                q.append(v)
    return order


# ===========================================================================
# (B) 최단 거리 BFS - 각 정점까지의 최소 간선 수
# ===========================================================================
def bfs_dist(graph, start):
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:              # 처음 도달 = 최단
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


# ===========================================================================
# (C) 격자 BFS - 시작(0,0)에서 각 칸까지 최소 이동 횟수(못 가면 -1)
#     grid[r][c] == 1 이면 이동 가능, 0 이면 벽.
# ===========================================================================
def grid_shortest(grid):
    R, C = len(grid), len(grid[0])
    dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]  # 상 하 좌 우
    dist = [[-1] * C for _ in range(R)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if (0 <= nr < R and 0 <= nc < C
                    and dist[nr][nc] == -1 and grid[nr][nc] == 1):
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist


# ===========================================================================
# (D) 다중 소스 BFS - 여러 출발점에서 동시에 퍼지는 최단 거리
# ===========================================================================
def multi_source_dist(grid, sources):
    R, C = len(grid), len(grid[0])
    dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
    dist = [[-1] * C for _ in range(R)]
    q = deque()
    for (sr, sc) in sources:               # 모든 소스를 거리 0으로 함께 넣기
        dist[sr][sc] = 0
        q.append((sr, sc))
    while q:
        r, c = q.popleft()
        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist


# ===========================================================================
# (E) 레벨 순회 BFS - 그래프를 거리(레벨)별 묶음으로 반환
# ===========================================================================
def bfs_levels(graph, start):
    visited = {start}
    q = deque([start])
    levels = []
    while q:
        size = len(q)                      # 지금 큐 = 현재 레벨 전체
        cur = []
        for _ in range(size):
            u = q.popleft()
            cur.append(u)
            for v in graph[u]:
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        levels.append(cur)
    return levels


# ===========================================================================
# 데모 실행
# ===========================================================================
def _demo():
    # 예제 그래프:
    #       1
    #      / \
    #     2   3
    #    / \   \
    #   4   5   6
    graph = {
        1: [2, 3],
        2: [4, 5],
        3: [6],
        4: [],
        5: [],
        6: [],
    }
    print("[A] BFS 방문 순서:", bfs_order(graph, 1))
    print("[B] 1에서의 최단 거리:", bfs_dist(graph, 1))
    print("[E] 레벨별 묶음:", bfs_levels(graph, 1))

    grid = [
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 1, 0],
    ]
    dist = grid_shortest(grid)
    print("[C] (0,0)->(3,3) 최단 이동:", dist[3][3])
    print("[C] (0,0)->(0,4) 최단 이동:", dist[0][4])

    # 다중 소스: 두 근원 (0,0), (3,4)에서 동시에 퍼짐
    open_grid = [[0] * 5 for _ in range(4)]
    md = multi_source_dist(open_grid, [(0, 0), (3, 4)])
    print("[D] 다중 소스에서 (1,2)까지 최단:", md[1][2])

    print("all examples ran OK")


if __name__ == "__main__":
    _demo()
