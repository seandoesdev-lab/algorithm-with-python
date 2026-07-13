# -*- coding: utf-8 -*-
"""
Day 25 - DFS (깊이 우선 탐색): 실행 가능한 예제 모음

DFS의 세 가지 대표 구현을 담았다:
  (A) 재귀 DFS      - 호출 스택이 되돌아가기를 자동 처리
  (B) 스택 DFS      - 재귀 깊이 한계를 피하는 반복 버전
  (C) 격자 DFS      - 상하좌우 이웃 순회(섬/영역 문제의 골격)
  (D) 연결 요소 세기 - 미방문 정점마다 DFS 시작 횟수 = 요소 수

콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

import sys
from collections import defaultdict

# 정점이 매우 많은 경우를 대비한 재귀 한도 상향(예제에서는 안전 차원).
sys.setrecursionlimit(10 ** 6)


# ===========================================================================
# (A) 재귀 DFS (인접 리스트) - 방문 순서 반환
# ===========================================================================
def dfs_recursive(graph, start):
    visited, order = set(), []

    def go(u):
        visited.add(u)                     # 진입 즉시 방문 표시
        order.append(u)
        for v in graph[u]:                 # 이웃을 정렬해 두면 순서가 결정적
            if v not in visited:
                go(v)

    go(start)
    return order


# ===========================================================================
# (B) 스택 DFS (반복) - 재귀 없이 LIFO로 깊이 우선
# ===========================================================================
def dfs_iterative(graph, start):
    visited, order = {start}, []
    stack = [start]
    while stack:
        u = stack.pop()                    # 가장 최근에 넣은 것을 꺼냄(LIFO)
        order.append(u)
        # 재귀(오름차순)와 같은 순서를 만들려면 역순으로 push.
        for v in sorted(graph[u], reverse=True):
            if v not in visited:
                visited.add(v)             # push 시점에 방문 표시(중복 push 방지)
                stack.append(v)
    return order


# ===========================================================================
# (C) 격자 DFS - 섬(1로 연결된 영역)의 개수
# ===========================================================================
def count_islands(grid):
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]  # 상 하 좌 우

    def dfs(r, c):
        seen[r][c] = True
        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc] and grid[nr][nc] == 1:
                dfs(nr, nc)

    count = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1 and not seen[r][c]:
                dfs(r, c)                  # 새 섬 하나를 통째로 방문
                count += 1
    return count


# ===========================================================================
# (D) 연결 요소(connected component) 개수 - 일반 무방향 그래프
# ===========================================================================
def count_components(n, edges):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    visited = set()

    def go(u):
        visited.add(u)
        for v in graph[u]:
            if v not in visited:
                go(v)

    comp = 0
    for u in range(n):
        if u not in visited:
            go(u)
            comp += 1
    return comp


# ===========================================================================
# (E) 경로 존재 여부 - start에서 goal로 도달 가능한가
# ===========================================================================
def has_path(graph, start, goal):
    visited = set()

    def go(u):
        if u == goal:
            return True
        visited.add(u)
        for v in graph[u]:
            if v not in visited and go(v):
                return True
        return False

    return go(start)


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
    print("[A] 재귀 DFS 방문 순서:", dfs_recursive(graph, 1))
    print("[B] 스택 DFS 방문 순서:", dfs_iterative(graph, 1))

    grid = [
        [1, 1, 0, 0, 1],
        [1, 0, 0, 1, 1],
        [0, 0, 1, 0, 0],
        [1, 0, 0, 0, 1],
    ]
    print("[C] 섬의 개수:", count_islands(grid))

    # 정점 0..5, 간선으로 {0,1,2}와 {3,4} 두 덩어리 + 고립 정점 5
    edges = [(0, 1), (1, 2), (3, 4)]
    print("[D] 연결 요소 개수(정점 6개):", count_components(6, edges))

    print("[E] 1 -> 6 경로 존재?:", "O" if has_path(graph, 1, 6) else "X")
    print("[E] 6 -> 1 경로 존재?:", "O" if has_path(graph, 6, 1) else "X")

    print("all examples ran OK")


if __name__ == "__main__":
    _demo()
