# -*- coding: utf-8 -*-
"""
Day 37 - 최소 신장 트리 (MST: Kruskal / Prim) 해설

플랫폼 시그니처 유지:
  - LeetCode  : class Solution 의 메서드
  - 프로그래머스 : def solution(...)
    (한 파일에 프로그래머스 문제가 둘이라 42861 을 solution 으로 두고,
     86971 은 solution_power_grid 로 둔다. 실제 제출 시엔 solution 으로 rename.)

각 문제에 assert 자체 테스트 포함. 가능한 곳은 다중 접근 + 복잡도 비교.

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

import heapq


# ===========================================================================
# 공용 DSU (경로 압축 + 사이즈 합치기) - Day 36 템플릿
# ===========================================================================
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:       # 경로 압축
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                    # 이미 같은 그룹 -> 사이클
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.count -= 1
        return True


# ===========================================================================
# 1. Min Cost to Connect All Points (LeetCode #1584)
#    완전 그래프 MST. 접근 A: 크루스칼 O(n^2 log n) / 접근 B: 프림 O(n^2).
#    n <= 1000 이라 간선이 약 50만 개 -> 프림 배열판이 정석.
# ===========================================================================
class SolutionConnectPoints:
    def minCostConnectPoints(self, points):
        """접근 B (권장): 프림 O(n^2). 간선을 만들지 않는다."""
        n = len(points)
        if n <= 1:
            return 0
        INF = float('inf')
        dist = [INF] * n                    # 트리에 붙는 최소 비용
        used = [False] * n
        dist[0] = 0
        total = 0
        for _ in range(n):
            u, best = -1, INF
            for i in range(n):              # 안 쓴 정점 중 dist 최소
                if not used[i] and dist[i] < best:
                    best, u = dist[i], i
            used[u] = True
            total += best
            ux, uy = points[u]
            for v in range(n):              # u 기준 dist 갱신
                if not used[v]:
                    vx, vy = points[v]
                    d = abs(ux - vx) + abs(uy - vy)
                    if d < dist[v]:
                        dist[v] = d
        return total

    def minCostConnectPoints_kruskal(self, points):
        """접근 A: 모든 쌍 간선 생성 후 크루스칼."""
        n = len(points)
        if n <= 1:
            return 0
        edges = []
        for i in range(n):
            xi, yi = points[i]
            for j in range(i + 1, n):
                xj, yj = points[j]
                edges.append((abs(xi - xj) + abs(yi - yj), i, j))
        edges.sort()                        # (w, i, j) 라 가중치 우선 정렬
        dsu = DSU(n)
        total, cnt = 0, 0
        for w, a, b in edges:
            if dsu.union(a, b):
                total += w
                cnt += 1
                if cnt == n - 1:            # V-1 개 채우면 종료
                    break
        return total


# ===========================================================================
# 2. 섬 연결하기 (프로그래머스 #42861) - 크루스칼 정석
#    costs[i] = [a, b, cost]. 0-based 섬 번호.
#    시간 O(E log E).
# ===========================================================================
def solution(n, costs):
    dsu = DSU(n)
    total, cnt = 0, 0
    for a, b, w in sorted(costs, key=lambda c: c[2]):   # 비용 오름차순!
        if dsu.union(a, b):                 # 사이클 아니면 채택
            total += w
            cnt += 1
            if cnt == n - 1:
                break
    return total


# ===========================================================================
# 3. 전력망을 둘로 나누기 (프로그래머스 #86971)
#    간선 n-1 개 트리 -> 하나 끊으면 반드시 컴포넌트 2 개.
#    각 전선을 빼보고 한쪽 크기 c 로 |n - 2c| 최솟값. 1-based 주의.
#    시간 O(n^2 * alpha).
# ===========================================================================
def solution_power_grid(n, wires):
    best = n
    for i in range(len(wires)):
        dsu = DSU(n + 1)                    # 1-based -> 0 번은 버림
        for j, (a, b) in enumerate(wires):
            if i == j:                      # i 번 전선을 끊는다
                continue
            dsu.union(a, b)
        root = dsu.find(wires[i][0])        # 끊긴 한쪽 대표
        cnt = sum(1 for v in range(1, n + 1) if dsu.find(v) == root)
        best = min(best, abs(n - 2 * cnt))  # |cnt - (n-cnt)|
    return best


# ===========================================================================
# 4. Path With Minimum Effort (LeetCode #1631) - 최소 병목 경로
#    접근 A: 크루스칼. 시작/끝이 처음 연결되는 순간의 가중치가 답.
#    접근 B: 이분 탐색 + DFS 도달성 검사.
#    접근 C: 변형 다익스트라 (합 대신 max 로 완화).
# ===========================================================================
class SolutionMinEffort:
    def minimumEffortPath(self, heights):
        """접근 A: 크루스칼 O(RC log(RC))."""
        R, C = len(heights), len(heights[0])
        if R * C == 1:
            return 0
        edges = []
        for r in range(R):
            for c in range(C):
                idx = r * C + c             # 셀 -> 1 차원 인덱스
                if r + 1 < R:
                    edges.append(
                        (abs(heights[r][c] - heights[r + 1][c]), idx, idx + C))
                if c + 1 < C:
                    edges.append(
                        (abs(heights[r][c] - heights[r][c + 1]), idx, idx + 1))
        edges.sort()
        dsu = DSU(R * C)
        target = R * C - 1
        for w, a, b in edges:
            dsu.union(a, b)
            if dsu.find(0) == dsu.find(target):   # 방금 연결됨
                return w
        return 0

    def minimumEffortPath_bs(self, heights):
        """접근 B: 이분 탐색 + DFS  O(RC log(maxH))."""
        R, C = len(heights), len(heights[0])
        lo = 0
        hi = (max(max(row) for row in heights)
              - min(min(row) for row in heights))

        def reachable(limit):
            seen = [[False] * C for _ in range(R)]
            stack = [(0, 0)]
            seen[0][0] = True
            while stack:
                r, c = stack.pop()
                if r == R - 1 and c == C - 1:
                    return True
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < R and 0 <= nc < C and not seen[nr][nc]
                            and abs(heights[nr][nc] - heights[r][c]) <= limit):
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            return False

        while lo < hi:                      # 최소 만족 limit 을 찾는다
            mid = (lo + hi) // 2
            if reachable(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo

    def minimumEffortPath_dijkstra(self, heights):
        """접근 C: 변형 다익스트라. 합이 아니라 max 로 완화."""
        R, C = len(heights), len(heights[0])
        INF = float('inf')
        best = [[INF] * C for _ in range(R)]
        best[0][0] = 0
        heap = [(0, 0, 0)]                  # (effort, r, c)
        while heap:
            e, r, c = heapq.heappop(heap)
            if e > best[r][c]:              # 낡은 항목 스킵
                continue
            if r == R - 1 and c == C - 1:
                return e
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    # 더하기가 아니라 max 인 것이 병목 문제의 핵심
                    ne = max(e, abs(heights[nr][nc] - heights[r][c]))
                    if ne < best[nr][nc]:
                        best[nr][nc] = ne
                        heapq.heappush(heap, (ne, nr, nc))
        return 0


# ===========================================================================
# 5. Checking Existence of Edge Length Limited Paths (LeetCode #1697)
#    오프라인 쿼리: 간선/쿼리를 각각 정렬해 간선을 한 번만 훑는다.
#    시간 O(E log E + Q log Q).
# ===========================================================================
class SolutionDistanceLimited:
    def distanceLimitedPathsExist(self, n, edgeList, queries):
        edges = sorted(edgeList, key=lambda e: e[2])
        order = sorted(range(len(queries)), key=lambda i: queries[i][2])
        dsu = DSU(n)
        res = [False] * len(queries)
        j = 0
        for qi in order:                    # limit 작은 쿼리부터
            p, q, limit = queries[qi]
            while j < len(edges) and edges[j][2] < limit:   # 부등호는 <
                dsu.union(edges[j][0], edges[j][1])
                j += 1
            res[qi] = dsu.find(p) == dsu.find(q)   # 원래 인덱스로 복원
        return res


# ===========================================================================
# 6. Find Critical and Pseudo-Critical Edges in MST (LeetCode #1489)
#    base MST 비용을 구한 뒤 간선마다
#      - 빼고 계산해서 커지면 critical
#      - 강제로 넣고 계산해서 같으면 pseudo-critical
#    시간 O(E^2 * alpha).
# ===========================================================================
class SolutionCriticalEdges:
    def _mst(self, n, indexed, skip=-1, force=None):
        """indexed = [(w, a, b, 원래인덱스), ...] 가중치 오름차순 정렬 상태."""
        dsu = DSU(n)
        total = 0
        if force is not None:               # 간선 강제 포함
            fw, fa, fb = force
            dsu.union(fa, fb)
            total = fw
        for w, a, b, i in indexed:
            if i == skip:                   # 간선 강제 제외
                continue
            if dsu.union(a, b):
                total += w
        return total if dsu.count == 1 else float('inf')   # 끊기면 INF

    def findCriticalAndPseudoCriticalEdges(self, n, edges):
        indexed = sorted(
            (w, a, b, i) for i, (a, b, w) in enumerate(edges))
        base = self._mst(n, indexed)
        critical, pseudo = [], []
        for w, a, b, i in indexed:
            if self._mst(n, indexed, skip=i) > base:
                critical.append(i)          # 빼면 비용 증가/단절
            elif self._mst(n, indexed, force=(w, a, b)) == base:
                pseudo.append(i)            # 넣어도 비용 동일
        return [sorted(critical), sorted(pseudo)]


# ===========================================================================
# 자체 테스트
# ===========================================================================
def run_tests():
    print("=" * 62)
    print("Day 37 - MST (Kruskal / Prim) 해설 self-test")
    print("=" * 62)

    # 1. Min Cost to Connect All Points - 두 접근 동일
    cp = SolutionConnectPoints()
    cases1 = [
        ([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]], 20),
        ([[3, 12], [-2, 5], [-4, 1]], 18),
        ([[0, 0], [1, 1], [1, 0], [-1, 1]], 4),
        ([[-1000000, -1000000], [1000000, 1000000]], 4000000),
        ([[0, 0]], 0),
    ]
    for pts, exp in cases1:
        assert cp.minCostConnectPoints(pts) == exp
        assert cp.minCostConnectPoints_kruskal(pts) == exp
    print("[1] Min Cost to Connect All Points (Prim == Kruskal)  OK")

    # 2. 섬 연결하기 (프로그래머스 42861)
    assert solution(4, [[0, 1, 1], [0, 2, 2], [1, 2, 5], [1, 3, 1]]) == 4
    assert solution(1, []) == 0
    assert solution(3, [[0, 1, 5], [1, 2, 3], [0, 2, 4]]) == 7
    print("[2] 섬 연결하기 (크루스칼 정석)                       OK")

    # 3. 전력망을 둘로 나누기 (프로그래머스 86971)
    assert solution_power_grid(
        9, [[1, 3], [2, 3], [3, 4], [4, 5], [4, 6], [4, 7], [7, 8],
            [7, 9]]) == 3
    assert solution_power_grid(4, [[1, 2], [2, 3], [3, 4]]) == 0
    assert solution_power_grid(
        7, [[1, 2], [2, 7], [3, 7], [3, 4], [4, 5], [6, 7]]) == 1
    assert solution_power_grid(2, [[1, 2]]) == 0
    print("[3] 전력망을 둘로 나누기 (간선 제거 + 컴포넌트)       OK")

    # 4. Path With Minimum Effort - 세 접근 동일
    me = SolutionMinEffort()
    cases4 = [
        ([[1, 2, 2], [3, 8, 2], [5, 3, 5]], 2),
        ([[1, 2, 3], [3, 8, 4], [5, 3, 5]], 1),
        ([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1],
          [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]], 0),
        ([[3]], 0),
    ]
    for grid, exp in cases4:
        assert me.minimumEffortPath(grid) == exp
        assert me.minimumEffortPath_bs(grid) == exp
        assert me.minimumEffortPath_dijkstra(grid) == exp
    print("[4] Path With Minimum Effort (UF == 이분 == 다익)     OK")

    # 5. Checking Existence of Edge Length Limited Paths
    dl = SolutionDistanceLimited()
    assert dl.distanceLimitedPathsExist(
        3, [[0, 1, 2], [1, 2, 4], [2, 0, 8], [1, 0, 16]],
        [[0, 1, 2], [0, 2, 5]]) == [False, True]
    assert dl.distanceLimitedPathsExist(
        5, [[0, 1, 10], [1, 2, 5], [2, 3, 9], [3, 4, 13]],
        [[0, 4, 14], [1, 4, 13]]) == [True, False]
    print("[5] Edge Length Limited Paths (오프라인 쿼리)         OK")

    # 6. Find Critical and Pseudo-Critical Edges in MST
    ce = SolutionCriticalEdges()
    assert ce.findCriticalAndPseudoCriticalEdges(
        5, [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3],
            [3, 4, 3], [1, 4, 6]]) == [[0, 1], [2, 3, 4, 5]]
    assert ce.findCriticalAndPseudoCriticalEdges(
        4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]]) == [[], [0, 1, 2, 3]]
    print("[6] Critical / Pseudo-Critical Edges                  OK")

    print("=" * 62)
    print("모든 테스트 통과 (All tests passed)")
    print("=" * 62)
    print("핵심 정리")
    print("  - 간선 리스트 입력   -> 크루스칼 (정렬 + union)")
    print("  - 완전 그래프        -> 프림 배열판 O(V^2)")
    print("  - 경로상 최대 최소화 -> 크루스칼로 s,t 연결 순간 포착")
    print("  - 쿼리 많음          -> 오프라인 정렬 후 간선 1 회 훑기")
    print("  - 간선 포함/제외     -> union 선행 가산 / 순회 skip")
    print("=" * 62)


if __name__ == "__main__":
    run_tests()
