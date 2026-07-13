# -*- coding: utf-8 -*-
"""
Day 25 - DFS (깊이 우선 탐색): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(재귀 DFS vs 스택 DFS, visited 배열 vs 격자 덮어쓰기)을
두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

import sys
from collections import defaultdict

sys.setrecursionlimit(10 ** 6)


# ===========================================================================
# 1. Flood Fill (LeetCode #733)
#    시작 칸과 같은 색으로 연결된 영역을 새 색으로. O(R*C).
# ===========================================================================
class SolutionFloodFill:
    def floodFill(self, image, sr, sc, color):
        R, C = len(image), len(image[0])
        start = image[sr][sc]
        if start == color:                 # 이미 같은 색: 무한 재귀 방지
            return image
        dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]

        def dfs(r, c):
            image[r][c] = color
            for d in range(4):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < R and 0 <= nc < C and image[nr][nc] == start:
                    dfs(nr, nc)

        dfs(sr, sc)
        return image


# ===========================================================================
# 2. Number of Islands (LeetCode #200)
#    재귀 DFS(격자 덮어쓰기) vs 스택 DFS. 둘 다 O(R*C).
# ===========================================================================
class SolutionNumIslands:
    def numIslands(self, grid):
        """재귀 DFS. 방문한 땅을 '0'으로 덮어써 visited 대체."""
        if not grid:
            return 0
        R, C = len(grid), len(grid[0])
        dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]

        def sink(r, c):
            grid[r][c] = "0"               # 방문 = 물로 변경
            for d in range(4):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == "1":
                    sink(nr, nc)

        count = 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == "1":
                    sink(r, c)
                    count += 1
        return count

    def numIslands_stack(self, grid):
        """스택 DFS. 재귀 깊이 한계를 피한다."""
        if not grid:
            return 0
        R, C = len(grid), len(grid[0])
        seen = [[False] * C for _ in range(R)]
        dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
        count = 0
        for sr in range(R):
            for sc in range(C):
                if grid[sr][sc] != "1" or seen[sr][sc]:
                    continue
                seen[sr][sc] = True
                stack = [(sr, sc)]
                while stack:
                    r, c = stack.pop()
                    for d in range(4):
                        nr, nc = r + dr[d], c + dc[d]
                        if (0 <= nr < R and 0 <= nc < C
                                and not seen[nr][nc] and grid[nr][nc] == "1"):
                            seen[nr][nc] = True
                            stack.append((nr, nc))
                count += 1
        return count


# ===========================================================================
# 3. Max Area of Island (LeetCode #695)
#    DFS가 방문 칸 수를 반환하게. O(R*C).
# ===========================================================================
class SolutionMaxArea:
    def maxAreaOfIsland(self, grid):
        R, C = len(grid), len(grid[0])
        dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]

        def area(r, c):
            if not (0 <= r < R and 0 <= c < C) or grid[r][c] != 1:
                return 0
            grid[r][c] = 0                 # 방문 처리
            total = 1
            for d in range(4):
                total += area(r + dr[d], c + dc[d])
            return total

        best = 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 1:
                    best = max(best, area(r, c))
        return best


# ===========================================================================
# 4. 타겟 넘버 (프로그래머스 #43165)
#    상태 공간 DFS: 각 수에 +/- 두 갈래. O(2^n).
# ===========================================================================
def solution_target(numbers, target):
    n = len(numbers)

    def dfs(i, acc):
        if i == n:
            return 1 if acc == target else 0
        return dfs(i + 1, acc + numbers[i]) + dfs(i + 1, acc - numbers[i])

    return dfs(0, 0)


# ===========================================================================
# 5. 네트워크 (프로그래머스 #43162)
#    인접 행렬 연결 요소. O(n^2).
# ===========================================================================
def solution_network(n, computers):
    visited = [False] * n

    def dfs(u):
        visited[u] = True
        for v in range(n):
            if computers[u][v] == 1 and not visited[v]:
                dfs(v)

    count = 0
    for u in range(n):
        if not visited[u]:
            dfs(u)
            count += 1
    return count


# ===========================================================================
# 6. Number of Provinces (LeetCode #547)
#    네트워크와 동일한 골격(인접 행렬 연결 요소). O(n^2).
# ===========================================================================
class SolutionProvinces:
    def findCircleNum(self, isConnected):
        n = len(isConnected)
        visited = [False] * n

        def dfs(u):
            visited[u] = True
            for v in range(n):
                if isConnected[u][v] == 1 and not visited[v]:
                    dfs(v)

        count = 0
        for u in range(n):
            if not visited[u]:
                dfs(u)
                count += 1
        return count


# ===========================================================================
# 7. Path Sum (LeetCode #112)
#    트리 DFS: 리프에서 남은 합이 0인지. O(N).
# ===========================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class SolutionPathSum:
    def hasPathSum(self, root, targetSum):
        if root is None:
            return False
        if root.left is None and root.right is None:   # 리프
            return targetSum == root.val
        remain = targetSum - root.val
        return (self.hasPathSum(root.left, remain)
                or self.hasPathSum(root.right, remain))


# ===========================================================================
# 8. Keys and Rooms (LeetCode #841)
#    도달 가능성 DFS: 방문한 방 수 == 전체 방 수. O(V+E).
# ===========================================================================
class SolutionKeysRooms:
    def canVisitAllRooms(self, rooms):
        visited = set()

        def dfs(u):
            visited.add(u)
            for key in rooms[u]:
                if key not in visited:
                    dfs(key)

        dfs(0)
        return len(visited) == len(rooms)


# ===========================================================================
# 9. 여행경로 (프로그래머스 #43164)
#    DFS + 백트래킹: 티켓(간선) 단위 사용 표시. 정렬로 사전순 최소.
# ===========================================================================
def solution_itinerary(tickets):
    graph = defaultdict(list)
    for src, dst in tickets:
        graph[src].append(dst)
    for src in graph:
        graph[src].sort()                  # 알파벳 순으로 먼저 시도
    total = len(tickets)
    route = ["ICN"]

    # 같은 구간 티켓이 중복될 수 있으므로 리스트 인덱스 단위로 사용 표시한다.
    used_idx = {src: [False] * len(dsts) for src, dsts in graph.items()}

    def dfs(airport, depth):
        if depth == total:
            return True                    # 모든 티켓 사용 완료
        for i, nxt in enumerate(graph[airport]):
            if used_idx[airport][i]:
                continue
            used_idx[airport][i] = True
            route.append(nxt)
            if dfs(nxt, depth + 1):
                return True
            route.pop()                    # 되돌리기(backtrack)
            used_idx[airport][i] = False
        return False

    dfs("ICN", 0)
    return route


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    # 1. Flood Fill
    ff = SolutionFloodFill()
    assert ff.floodFill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == \
        [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    assert ff.floodFill([[0, 0, 0], [0, 0, 0]], 0, 0, 0) == \
        [[0, 0, 0], [0, 0, 0]]             # 같은 색: 그대로

    # 2. Number of Islands (두 접근 모두)
    ni = SolutionNumIslands()
    g1 = [["1", "1", "0", "0", "0"],
          ["1", "1", "0", "0", "0"],
          ["0", "0", "1", "0", "0"],
          ["0", "0", "0", "1", "1"]]
    g2 = [row[:] for row in g1]
    assert ni.numIslands(g1) == 3
    assert ni.numIslands_stack(g2) == 3

    # 3. Max Area of Island
    ma = SolutionMaxArea()
    grid = [[0, 0, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 1, 0]]
    assert ma.maxAreaOfIsland(grid) == 3
    assert ma.maxAreaOfIsland([[0, 0], [0, 0]]) == 0

    # 4. 타겟 넘버
    assert solution_target([1, 1, 1, 1, 1], 3) == 5
    assert solution_target([4, 1, 2, 1], 4) == 2

    # 5. 네트워크 / 6. Number of Provinces (동일 입력 -> 동일 답)
    net = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    assert solution_network(3, net) == 2
    prov = SolutionProvinces()
    assert prov.findCircleNum(net) == 2
    net2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert solution_network(3, net2) == 3
    assert prov.findCircleNum(net2) == 3

    # 7. Path Sum
    #        5
    #       / \
    #      4   8
    #     /
    #    11
    #   /  \
    #  7    2
    root = TreeNode(5,
                    TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2))),
                    TreeNode(8))
    ps = SolutionPathSum()
    assert ps.hasPathSum(root, 22) is True     # 5+4+11+2
    assert ps.hasPathSum(root, 100) is False
    assert ps.hasPathSum(None, 0) is False

    # 8. Keys and Rooms
    kr = SolutionKeysRooms()
    assert kr.canVisitAllRooms([[1], [2], [3], []]) is True
    assert kr.canVisitAllRooms([[1, 3], [3, 0, 1], [2], [0]]) is False

    # 9. 여행경로
    assert solution_itinerary(
        [["ICN", "JFK"], ["HND", "IAD"], ["JFK", "HND"]]) == \
        ["ICN", "JFK", "HND", "IAD"]
    assert solution_itinerary(
        [["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"],
         ["ATL", "ICN"], ["ATL", "SFO"]]) == \
        ["ICN", "ATL", "ICN", "SFO", "ATL", "SFO"]

    print("Day 25 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()
