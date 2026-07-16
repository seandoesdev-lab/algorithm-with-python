# -*- coding: utf-8 -*-
"""
Day 28 - 그래프 표현과 순회 (Graph Representation & Traversal): 실행 가능한 예제

두 단계로 나눠 본다:
  (1) 표현(represent) - 간선 목록 -> 인접 리스트 / 인접 행렬
  (2) 순회(traverse)  - DFS(재귀/스택) / BFS(큐), visited로 사이클 차단

표준 라이브러리만 사용한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다(한글 OK).
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from collections import defaultdict, deque


# ---------------------------------------------------------------------------
# 1) 표현: 간선 목록(edge list) -> 인접 리스트(adjacency list)
#    무방향이면 (u, v)를 양쪽에 두 번 넣는다.
# ---------------------------------------------------------------------------
def build_adj_list(n, edges, directed=False):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)          # 무방향: 반대 방향도 추가
    return adj


# ---------------------------------------------------------------------------
# 2) 표현: 간선 목록 -> 인접 행렬(adjacency matrix)
#    matrix[u][v] = 1 이면 u-v 연결. "직접 연결?"을 O(1)에 답한다.
# ---------------------------------------------------------------------------
def build_adj_matrix(n, edges, directed=False):
    m = [[0] * n for _ in range(n)]
    for u, v in edges:
        m[u][v] = 1
        if not directed:
            m[v][u] = 1
    return m


# ---------------------------------------------------------------------------
# 3) 순회: DFS (재귀). visited가 사이클에서 무한 루프를 막는다.
# ---------------------------------------------------------------------------
def dfs_recursive(start, adj, n):
    visited = [False] * n
    order = []

    def dfs(u):
        visited[u] = True
        order.append(u)
        for nxt in adj[u]:
            if not visited[nxt]:
                dfs(nxt)

    dfs(start)
    return order


# ---------------------------------------------------------------------------
# 4) 순회: DFS (명시적 스택). 재귀 깊이 한계를 피하는 반복 버전.
# ---------------------------------------------------------------------------
def dfs_iterative(start, adj, n):
    visited = [False] * n
    order = []
    stack = [start]
    visited[start] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for nxt in adj[u]:
            if not visited[nxt]:
                visited[nxt] = True
                stack.append(nxt)
    return order


# ---------------------------------------------------------------------------
# 5) 순회: BFS (큐). 방문 표시는 "큐에 넣는 순간"에 한다.
# ---------------------------------------------------------------------------
def bfs(start, adj, n):
    visited = [False] * n
    order = []
    q = deque([start])
    visited[start] = True
    while q:
        u = q.popleft()
        order.append(u)
        for nxt in adj[u]:
            if not visited[nxt]:
                visited[nxt] = True       # 넣을 때 표시(중복 삽입 방지)
                q.append(nxt)
    return order


# ---------------------------------------------------------------------------
# 6) 응용: 연결 요소(connected components) 개수 세기
#    모든 정점을 훑으며 아직 방문 안 한 정점마다 새 순회를 시작한다.
# ---------------------------------------------------------------------------
def count_components(n, adj):
    visited = [False] * n
    count = 0
    for s in range(n):
        if not visited[s]:
            count += 1                    # 새 무리 발견
            stack = [s]
            visited[s] = True
            while stack:
                u = stack.pop()
                for nxt in adj[u]:
                    if not visited[nxt]:
                        visited[nxt] = True
                        stack.append(nxt)
    return count


# ---------------------------------------------------------------------------
# 7) 응용: 격자 = 암시적 그래프(implicit graph) - 섬의 개수
# ---------------------------------------------------------------------------
def num_islands(grid):
    if not grid or not grid[0]:
        return 0
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    dr, dc = (-1, 1, 0, 0), (0, 0, -1, 1)
    cnt = 0
    for i in range(R):
        for j in range(C):
            if grid[i][j] == "1" and not seen[i][j]:
                cnt += 1
                q = deque([(i, j)])
                seen[i][j] = True
                while q:
                    r, c = q.popleft()
                    for d in range(4):
                        nr, nc = r + dr[d], c + dc[d]
                        if (0 <= nr < R and 0 <= nc < C
                                and not seen[nr][nc] and grid[nr][nc] == "1"):
                            seen[nr][nc] = True
                            q.append((nr, nc))
    return cnt


# ---------------------------------------------------------------------------
# 8) 문자열 라벨 그래프: defaultdict(list)로 인접 리스트 (공항 코드 등)
# ---------------------------------------------------------------------------
def build_labeled_adj(edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)                  # 방향 그래프 예시
    return adj


# ---------------------------------------------------------------------------
# 데모 실행
# ---------------------------------------------------------------------------
def _demo():
    # 예제 그래프(무방향):  0-1, 0-2, 1-3, 2-3  (사각형 사이클)
    n = 4
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]

    print("=== 1) 인접 리스트 표현 ===")
    adj = build_adj_list(n, edges)
    for u in range(n):
        print("정점", u, "-> 이웃", adj[u])

    print()
    print("=== 2) 인접 행렬 표현 ===")
    mat = build_adj_matrix(n, edges)
    for row in mat:
        print(row)

    print()
    print("=== 3) DFS 순회 (재귀), start=0 ===")
    print("방문 순서:", dfs_recursive(0, adj, n))

    print()
    print("=== 4) DFS 순회 (스택), start=0 ===")
    print("방문 순서:", dfs_iterative(0, adj, n))

    print()
    print("=== 5) BFS 순회 (큐), start=0 ===")
    print("방문 순서:", bfs(0, adj, n))

    print()
    print("=== 6) 연결 요소 개수 ===")
    # 0-1-2-3 한 무리 + 4-5 한 무리 + 6 혼자 = 3개
    n2 = 7
    edges2 = [(0, 1), (1, 2), (2, 3), (4, 5)]
    adj2 = build_adj_list(n2, edges2)
    print("무리 수:", count_components(n2, adj2), "(정답 3)")

    print()
    print("=== 7) 격자 섬의 개수 ===")
    grid = [
        ["1", "1", "0", "0"],
        ["1", "0", "0", "1"],
        ["0", "0", "1", "1"],
    ]
    print("섬 개수:", num_islands(grid), "(정답 2)")

    print()
    print("=== 8) 문자열 라벨 그래프(방향) ===")
    ladj = build_labeled_adj([("ICN", "JFK"), ("ICN", "HND"), ("JFK", "LAX")])
    for k in ["ICN", "JFK"]:
        print(k, "->", ladj[k])

    # 간단 검증
    assert dfs_recursive(0, adj, n)[0] == 0
    assert sorted(bfs(0, adj, n)) == [0, 1, 2, 3]
    assert count_components(n2, adj2) == 3
    assert num_islands(grid) == 2

    print()
    print("모든 예제 실행 완료 OK")


if __name__ == "__main__":
    _demo()
