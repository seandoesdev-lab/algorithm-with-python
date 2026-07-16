# -*- coding: utf-8 -*-
"""
Day 28 - 그래프 표현과 순회 (Graph Representation & Traversal): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(DFS vs BFS, 리스트 vs 행렬, 차수 vs 순회)을
두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from collections import defaultdict, deque


# ===========================================================================
# 1. Find Center of Star Graph (LeetCode #1791)
#    중심은 모든 간선에 등장 -> 첫 두 간선의 공통 정점.
# ===========================================================================
class SolutionFindCenter:
    def findCenter(self, edges):
        a, b = edges[0]
        c, d = edges[1]
        return a if a in (c, d) else b


# ===========================================================================
# 2. Find if Path Exists in Graph (LeetCode #1971)
#    (A) BFS  (B) DFS(반복). 무방향이므로 양방향 인접 리스트.
# ===========================================================================
class SolutionPathExists:
    def validPath(self, n, edges, source, destination):   # BFS
        if source == destination:
            return True
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = [False] * n
        q = deque([source])
        visited[source] = True
        while q:
            u = q.popleft()
            if u == destination:
                return True
            for nxt in adj[u]:
                if not visited[nxt]:
                    visited[nxt] = True
                    q.append(nxt)
        return False

    def validPath_dfs(self, n, edges, source, destination):  # DFS(스택)
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = [False] * n
        stack = [source]
        visited[source] = True
        while stack:
            u = stack.pop()
            if u == destination:
                return True
            for nxt in adj[u]:
                if not visited[nxt]:
                    visited[nxt] = True
                    stack.append(nxt)
        return visited[destination]


# ===========================================================================
# 3. Find the Town Judge (LeetCode #997)
#    순회 없이 차수(진입-진출)만으로. score == n-1 인 사람이 재판관.
# ===========================================================================
class SolutionTownJudge:
    def findJudge(self, n, trust):
        score = [0] * (n + 1)
        for a, b in trust:
            score[a] -= 1          # a는 남을 신뢰 -> 진출차수
            score[b] += 1          # b는 신뢰받음 -> 진입차수
        for i in range(1, n + 1):
            if score[i] == n - 1:
                return i
        return -1


# ===========================================================================
# 4. Number of Provinces (LeetCode #547)
#    인접 행렬 위의 연결 요소 세기. DFS(반복).
# ===========================================================================
class SolutionProvinces:
    def findCircleNum(self, isConnected):
        n = len(isConnected)
        visited = [False] * n
        count = 0
        for s in range(n):
            if not visited[s]:
                count += 1
                stack = [s]
                visited[s] = True
                while stack:
                    u = stack.pop()
                    for v in range(n):
                        if isConnected[u][v] == 1 and not visited[v]:
                            visited[v] = True
                            stack.append(v)
        return count


# ===========================================================================
# 5. Number of Islands (LeetCode #200)
#    격자 = 암시적 그래프. BFS로 각 섬을 침몰(방문 표시).
# ===========================================================================
class SolutionNumIslands:
    def numIslands(self, grid):
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
                                    and not seen[nr][nc]
                                    and grid[nr][nc] == "1"):
                                seen[nr][nc] = True
                                q.append((nr, nc))
        return cnt


# ===========================================================================
# 6. Keys and Rooms (LeetCode #841)
#    rooms가 곧 인접 리스트(방향). 0에서 도달 정점 수 == n 이면 True.
# ===========================================================================
class SolutionKeysRooms:
    def canVisitAllRooms(self, rooms):
        n = len(rooms)
        visited = [False] * n
        stack = [0]
        visited[0] = True
        cnt = 1
        while stack:
            u = stack.pop()
            for key in rooms[u]:
                if not visited[key]:
                    visited[key] = True
                    cnt += 1
                    stack.append(key)
        return cnt == n


# ===========================================================================
# 7. Clone Graph (LeetCode #133)
#    원본->복제 매핑 dict가 visited를 겸한다(사이클 무한복제 방지).
# ===========================================================================
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class SolutionCloneGraph:
    def cloneGraph(self, node):
        if node is None:
            return None
        clones = {}                       # 원본 -> 복제

        def dfs(orig):
            if orig in clones:
                return clones[orig]
            copy = Node(orig.val)
            clones[orig] = copy           # 이웃 복제 전에 먼저 등록(사이클 대비)
            for nb in orig.neighbors:
                copy.neighbors.append(dfs(nb))
            return copy

        return dfs(node)


# ===========================================================================
# 8. All Paths From Source to Target (LeetCode #797)
#    DAG라 사이클 없음 -> visited 불필요. DFS + 경로 백트래킹.
# ===========================================================================
class SolutionAllPaths:
    def allPathsSourceTarget(self, graph):
        n = len(graph)
        res, path = [], [0]

        def dfs(u):
            if u == n - 1:
                res.append(path[:])       # 복사본 기록
                return
            for nxt in graph[u]:
                path.append(nxt)          # choose
                dfs(nxt)                  # explore
                path.pop()                # undo

        dfs(0)
        return res


# ===========================================================================
# 9. 네트워크 (프로그래머스 #43162)
#    인접 행렬(computers) 위 연결 요소 개수 = 네트워크 수.
# ===========================================================================
def solution_network(n, computers):
    visited = [False] * n
    count = 0
    for s in range(n):
        if not visited[s]:
            count += 1
            stack = [s]
            visited[s] = True
            while stack:
                u = stack.pop()
                for v in range(n):
                    if computers[u][v] == 1 and not visited[v]:
                        visited[v] = True
                        stack.append(v)
    return count


# ===========================================================================
# 10. 여행경로 (프로그래머스 #43164)
#     문자열 라벨 인접 리스트 + 사전순 정렬 + DFS로 티켓 소모.
#     정점이 아니라 "간선(티켓)"을 다 써야 완성.
# ===========================================================================
def solution_itinerary(tickets):
    adj = defaultdict(list)
    for src, dst in tickets:
        adj[src].append(dst)
    for src in adj:
        adj[src].sort(reverse=True)       # pop()으로 사전순 앞부터 꺼내려 역정렬
    total = len(tickets)
    route = []

    def dfs(airport):
        while adj[airport]:
            nxt = adj[airport].pop()      # 사전순 가장 앞선 목적지
            dfs(nxt)
        route.append(airport)             # 후위: 막다르면 경로에 추가

    dfs("ICN")
    route.reverse()                       # 후위로 쌓았으니 뒤집으면 정방향
    # 모든 티켓을 다 쓴 경우에만 유효(경로 길이 = 티켓 수 + 1)
    return route if len(route) == total + 1 else []


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    # 1. Find Center of Star Graph
    fc = SolutionFindCenter()
    assert fc.findCenter([[1, 2], [2, 3], [4, 2]]) == 2
    assert fc.findCenter([[1, 2], [5, 1], [1, 3], [1, 4]]) == 1

    # 2. Find if Path Exists in Graph
    pe = SolutionPathExists()
    assert pe.validPath(3, [[0, 1], [1, 2], [2, 0]], 0, 2) is True
    assert pe.validPath(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5) is False
    assert pe.validPath_dfs(3, [[0, 1], [1, 2], [2, 0]], 0, 2) is True
    assert pe.validPath_dfs(1, [], 0, 0) is True

    # 3. Find the Town Judge
    tj = SolutionTownJudge()
    assert tj.findJudge(2, [[1, 2]]) == 2
    assert tj.findJudge(3, [[1, 3], [2, 3]]) == 3
    assert tj.findJudge(3, [[1, 3], [2, 3], [3, 1]]) == -1
    assert tj.findJudge(1, []) == 1

    # 4. Number of Provinces
    pv = SolutionProvinces()
    assert pv.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert pv.findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3

    # 5. Number of Islands
    ni = SolutionNumIslands()
    g1 = [["1", "1", "1", "1", "0"],
          ["1", "1", "0", "1", "0"],
          ["1", "1", "0", "0", "0"],
          ["0", "0", "0", "0", "0"]]
    assert ni.numIslands([row[:] for row in g1]) == 1
    g2 = [["1", "1", "0", "0", "0"],
          ["1", "1", "0", "0", "0"],
          ["0", "0", "1", "0", "0"],
          ["0", "0", "0", "1", "1"]]
    assert ni.numIslands([row[:] for row in g2]) == 3

    # 6. Keys and Rooms
    kr = SolutionKeysRooms()
    assert kr.canVisitAllRooms([[1], [2], [3], []]) is True
    assert kr.canVisitAllRooms([[1, 3], [3, 0, 1], [2], [0]]) is False

    # 7. Clone Graph
    cg = SolutionCloneGraph()
    # 4노드 그래프: 1-2, 1-4, 2-3, 3-4 (무방향)
    n1, n2, n3, n4 = Node(1), Node(2), Node(3), Node(4)
    n1.neighbors = [n2, n4]
    n2.neighbors = [n1, n3]
    n3.neighbors = [n2, n4]
    n4.neighbors = [n1, n3]
    clone = cg.cloneGraph(n1)
    assert clone is not n1 and clone.val == 1
    assert [nb.val for nb in clone.neighbors] == [2, 4]
    # 복제본이 원본과 다른 객체인지(깊은 복사) 확인
    assert clone.neighbors[0] is not n2
    assert cg.cloneGraph(None) is None

    # 8. All Paths From Source to Target
    ap = SolutionAllPaths()
    assert sorted(ap.allPathsSourceTarget([[1, 2], [3], [3], []])) == \
        [[0, 1, 3], [0, 2, 3]]
    assert ap.allPathsSourceTarget([[1], []]) == [[0, 1]]

    # 9. 네트워크
    assert solution_network(3, [[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
    assert solution_network(3, [[1, 1, 0], [1, 1, 1], [0, 1, 1]]) == 1

    # 10. 여행경로
    assert solution_itinerary(
        [["ICN", "JFK"], ["HND", "IAD"], ["JFK", "HND"]]) == \
        ["ICN", "JFK", "HND", "IAD"]
    assert solution_itinerary(
        [["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"],
         ["ATL", "ICN"], ["ATL", "SFO"]]) == \
        ["ICN", "ATL", "ICN", "SFO", "ATL", "SFO"]

    print("Day 28 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()
