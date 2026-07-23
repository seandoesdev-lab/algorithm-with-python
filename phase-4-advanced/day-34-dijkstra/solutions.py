# -*- coding: utf-8 -*-
"""
Day 34 - 최단 경로: 다익스트라 (Dijkstra) 해설

플랫폼 시그니처 유지:
  - LeetCode  : class Solution 의 메서드
  - 프로그래머스 : def solution(...)
각 문제에 assert 자체 테스트 포함. 가능한 곳은 다중 접근 + 복잡도 비교.

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

import heapq
from collections import deque

INF = float("inf")


# ===========================================================================
# 1. Shortest Path in Binary Matrix (LeetCode #1091)
#    모든 이동 비용 = 1 -> BFS 로 최단 (다익스트라 불필요).
#    시간 O(n^2), 공간 O(n^2).
# ===========================================================================
class SolutionBinaryMatrix:
    def shortestPathBinaryMatrix(self, grid):
        n = len(grid)
        if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return -1
        seen = [[False] * n for _ in range(n)]
        seen[0][0] = True
        q = deque([(0, 0, 1)])                      # (r, c, 지금까지 밟은 칸 수)
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]     # 8방향
        while q:
            r, c, d = q.popleft()
            if r == n - 1 and c == n - 1:
                return d
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc] and grid[nr][nc] == 0:
                    seen[nr][nc] = True
                    q.append((nr, nc, d + 1))
        return -1


# ===========================================================================
# 2. Network Delay Time (LeetCode #743) - 표준 다익스트라
#    답 = max(dist[1..n]). 하나라도 INF 면 -1.
#    시간 O((V+E) log V).
# ===========================================================================
class SolutionNetworkDelay:
    def networkDelayTime(self, times, n, k) -> int:
        graph = [[] for _ in range(n + 1)]
        for u, v, w in times:
            graph[u].append((v, w))
        dist = [INF] * (n + 1)
        dist[k] = 0
        pq = [(0, k)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(pq, (d + w, v))
        ans = max(dist[1:])                          # 가장 늦게 받는 노드
        return ans if ans < INF else -1


# ===========================================================================
# 3. 배달 (프로그래머스 #12978) - 무방향 다익스트라
#    양방향 간선을 둘 다 넣는 것이 핵심. dist[i] <= K 인 마을 수.
# ===========================================================================
def solution(N, road, K):
    graph = [[] for _ in range(N + 1)]
    for a, b, c in road:
        graph[a].append((b, c))
        graph[b].append((a, c))                      # 무방향: 양쪽 모두
    dist = [INF] * (N + 1)
    dist[1] = 0
    pq = [(0, 1)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return sum(1 for x in dist[1:] if x <= K)


# ===========================================================================
# 4. Path With Minimum Effort (LeetCode #1631) - minimax 격자 다익스트라
#    접근 A: 완화 식을 max(cur, |높이차|) 로 바꾼 다익스트라.
#    접근 B: 이분 탐색 + BFS (effort <= x 로 도달 가능한가?).
# ===========================================================================
class SolutionMinEffort:
    def minimumEffortPath(self, heights) -> int:
        R, C = len(heights), len(heights[0])
        effort = [[INF] * C for _ in range(R)]
        effort[0][0] = 0
        pq = [(0, 0, 0)]                             # (effort, r, c)
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        while pq:
            e, r, c = heapq.heappop(pq)
            if r == R - 1 and c == C - 1:
                return e
            if e > effort[r][c]:
                continue
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    ne = max(e, abs(heights[nr][nc] - heights[r][c]))
                    if ne < effort[nr][nc]:
                        effort[nr][nc] = ne
                        heapq.heappush(pq, (ne, nr, nc))
        return 0

    def minimumEffortPath_binsearch(self, heights) -> int:
        R, C = len(heights), len(heights[0])
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        def reachable(limit):
            seen = [[False] * C for _ in range(R)]
            seen[0][0] = True
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if r == R - 1 and c == C - 1:
                    return True
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < R and 0 <= nc < C and not seen[nr][nc]
                            and abs(heights[nr][nc] - heights[r][c]) <= limit):
                        seen[nr][nc] = True
                        q.append((nr, nc))
            return False

        lo, hi = 0, 10 ** 6
        while lo < hi:                               # 최소 limit 이분 탐색
            mid = (lo + hi) // 2
            if reachable(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


# ===========================================================================
# 5. Cheapest Flights Within K Stops (LeetCode #787)
#    제약(경유 <= K) 최단 경로. 정석은 벨만-포드식 (K+1) 회 완화.
#    접근 A: 벨만-포드 라운드 (스냅샷으로 라운드당 간선 1개씩).
#    접근 B: (비용, 도시, 남은 경유) 상태 다익스트라.
# ===========================================================================
class SolutionCheapestFlights:
    def findCheapestPrice(self, n, flights, src, dst, k) -> int:
        dist = [INF] * n
        dist[src] = 0
        for _ in range(k + 1):                       # 간선 최대 k+1 개
            snap = dist[:]                           # 이전 라운드 스냅샷만 사용
            for u, v, w in flights:
                if snap[u] + w < dist[v]:
                    dist[v] = snap[u] + w
        return dist[dst] if dist[dst] < INF else -1

    def findCheapestPrice_dijkstra(self, n, flights, src, dst, k) -> int:
        graph = [[] for _ in range(n)]
        for u, v, w in flights:
            graph[u].append((v, w))
        # (누적비용, 도시, 남은 간선 사용 가능 수)
        pq = [(0, src, k + 1)]                        # 남은 간선 사용 횟수 = k+1
        best = {}                                    # (도시, 남은횟수) -> 최소비용
        while pq:
            cost, u, stops = heapq.heappop(pq)
            if u == dst:
                return cost
            if stops == 0:
                continue
            if best.get((u, stops), INF) < cost:
                continue
            for v, w in graph[u]:
                nc = cost + w
                if nc < best.get((v, stops - 1), INF):
                    best[(v, stops - 1)] = nc
                    heapq.heappush(pq, (nc, v, stops - 1))
        return -1


# ===========================================================================
# 6. Swim in Rising Water (LeetCode #778) - minimax 다익스트라
#    경로상 최대 고도를 최소화. 완화 nt = max(cur_t, grid[nr][nc]).
# ===========================================================================
class SolutionSwim:
    def swimInWater(self, grid) -> int:
        n = len(grid)
        best = [[INF] * n for _ in range(n)]
        best[0][0] = grid[0][0]
        pq = [(grid[0][0], 0, 0)]                    # (현재까지 최대고도, r, c)
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        while pq:
            t, r, c = heapq.heappop(pq)
            if r == n - 1 and c == n - 1:
                return t
            if t > best[r][c]:
                continue
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    nt = max(t, grid[nr][nc])
                    if nt < best[nr][nc]:
                        best[nr][nc] = nt
                        heapq.heappush(pq, (nt, nr, nc))
        return -1


def run_tests():
    print("=" * 60)
    print("Day 34 - Dijkstra 해설 self-test")
    print("=" * 60)

    # 1. Shortest Path in Binary Matrix
    bm = SolutionBinaryMatrix()
    assert bm.shortestPathBinaryMatrix([[0, 1], [1, 0]]) == 2
    assert bm.shortestPathBinaryMatrix([[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
    assert bm.shortestPathBinaryMatrix([[1, 0, 0], [1, 1, 0], [1, 1, 0]]) == -1
    assert bm.shortestPathBinaryMatrix([[0]]) == 1
    print("[1] Shortest Path Binary Matrix (BFS)  OK")

    # 2. Network Delay Time
    nd = SolutionNetworkDelay()
    assert nd.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert nd.networkDelayTime([[1, 2, 1]], 2, 1) == 1
    assert nd.networkDelayTime([[1, 2, 1]], 2, 2) == -1      # 1 도달 불가
    print("[2] Network Delay Time (Dijkstra)      OK")

    # 3. 배달 (프로그래머스)
    assert solution(5, [[1, 2, 1], [2, 3, 3], [5, 2, 2],
                        [1, 4, 2], [5, 3, 1], [5, 4, 2]], 3) == 4
    assert solution(6, [[1, 2, 1], [1, 3, 2], [2, 3, 2], [3, 4, 3],
                        [3, 5, 2], [3, 5, 3], [5, 6, 1]], 4) == 4
    print("[3] 배달 (무방향 Dijkstra)             OK")

    # 4. Path With Minimum Effort - 두 접근 동일
    me = SolutionMinEffort()
    cases4 = [
        ([[1, 2, 2], [3, 8, 2], [5, 3, 5]], 2),
        ([[1, 2, 3], [3, 8, 4], [5, 3, 5]], 1),
        ([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1],
          [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]], 0),
    ]
    for grid, exp in cases4:
        assert me.minimumEffortPath([row[:] for row in grid]) == exp
        assert me.minimumEffortPath_binsearch([row[:] for row in grid]) == exp
    print("[4] Path With Minimum Effort           OK  (Dijkstra == 이분+BFS)")

    # 5. Cheapest Flights Within K Stops - 두 접근 동일
    cf = SolutionCheapestFlights()
    cases5 = [
        (4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1, 700),
        (3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1, 200),
        (3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0, 500),
        (2, [[1, 0, 10]], 0, 1, 1, -1),                 # 도달 불가
    ]
    for n, fl, s, d, k, exp in cases5:
        assert cf.findCheapestPrice(n, fl, s, d, k) == exp
        assert cf.findCheapestPrice_dijkstra(n, fl, s, d, k) == exp
    print("[5] Cheapest Flights K Stops           OK  (벨만포드 == 상태 Dijkstra)")

    # 6. Swim in Rising Water
    sw = SolutionSwim()
    assert sw.swimInWater([[0, 2], [1, 3]]) == 3
    assert sw.swimInWater([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5],
                           [12, 13, 14, 15, 16], [11, 17, 18, 19, 20],
                           [10, 9, 8, 7, 6]]) == 16
    assert sw.swimInWater([[0]]) == 0
    print("[6] Swim in Rising Water (minimax)     OK")

    print("=" * 60)
    print("모든 테스트 통과 (All tests passed)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
