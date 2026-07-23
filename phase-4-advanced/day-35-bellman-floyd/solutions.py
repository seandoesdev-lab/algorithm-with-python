# -*- coding: utf-8 -*-
"""
Day 35 - 최단 경로: 벨만-포드 & 플로이드-워셜 해설

플랫폼 시그니처 유지:
  - LeetCode  : class Solution 의 메서드
  - 프로그래머스 : def solution(...)
각 문제에 assert 자체 테스트 포함. 가능한 곳은 다중 접근 + 복잡도 비교.

cp949 콘솔 안전: print 출력은 ASCII( = - O X )만 사용. (한글 설명은 OK)
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from collections import defaultdict, deque

INF = float("inf")


# ===========================================================================
# 1. Network Delay Time (LeetCode #743) - 벨만-포드 (다익스트라 대비)
#    답 = max(dist[1..n]); 하나라도 INF 면 -1.
#    시간 O(V*E).
# ===========================================================================
class SolutionNetworkDelay:
    def networkDelayTime(self, times, n, k) -> int:
        dist = [INF] * (n + 1)
        dist[0] = 0            # 0번 인덱스는 안 씀 (max 계산에서 제외)
        dist[k] = 0
        for _ in range(n - 1):                       # V-1 라운드
            updated = False
            for u, v, w in times:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            if not updated:
                break
        ans = max(dist[1:])
        return ans if ans < INF else -1


# ===========================================================================
# 2. Cheapest Flights Within K Stops (LeetCode #787) - K-제약 벨만-포드
#    K+1 라운드, 매 라운드 직전 스냅샷으로만 완화 (라운드당 간선 1개씩).
#    시간 O(K * E).
# ===========================================================================
class SolutionCheapestFlights:
    def findCheapestPrice(self, n, flights, src, dst, k) -> int:
        dist = [INF] * n
        dist[src] = 0
        for _ in range(k + 1):                       # 간선 최대 k+1 개
            snap = dist[:]                           # 직전 라운드 스냅샷만 사용
            for u, v, w in flights:
                if snap[u] != INF and snap[u] + w < dist[v]:
                    dist[v] = snap[u] + w
        return dist[dst] if dist[dst] < INF else -1


# ===========================================================================
# 3. Find the City ... Threshold Distance (LeetCode #1334) - 플로이드-워셜
#    모든 쌍 최단 거리 후, threshold 이하 이웃 수 최소 도시(동률이면 큰 번호).
#    시간 O(n^3).
# ===========================================================================
class SolutionFindCity:
    def findTheCity(self, n, edges, distanceThreshold) -> int:
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:                        # 무방향: 양쪽 초기화
            dist[u][v] = min(dist[u][v], w)
            dist[v][u] = min(dist[v][u], w)
        for kk in range(n):                          # k 최외곽
            for i in range(n):
                if dist[i][kk] == INF:
                    continue
                for j in range(n):
                    if dist[i][kk] + dist[kk][j] < dist[i][j]:
                        dist[i][j] = dist[i][kk] + dist[kk][j]
        best_city, best_cnt = -1, INF
        for i in range(n):
            cnt = sum(1 for j in range(n)
                      if j != i and dist[i][j] <= distanceThreshold)
            if cnt <= best_cnt:                      # <= 로 큰 번호 우선
                best_cnt, best_city = cnt, i
        return best_city


# ===========================================================================
# 4. 순위 (프로그래머스 #49191) - 플로이드-워셜 도달성(전이 폐포)
#    beats[i][j] = i가 j를 (직접/간접) 이긴다.
#    이긴 수 + 진 수 == n-1 이면 순위 확정.
# ===========================================================================
def solution(n, results):
    beats = [[False] * (n + 1) for _ in range(n + 1)]
    for a, b in results:
        beats[a][b] = True
    for k in range(1, n + 1):                        # k 최외곽
        for i in range(1, n + 1):
            if not beats[i][k]:
                continue
            for j in range(1, n + 1):
                if beats[k][j]:
                    beats[i][j] = True
    fixed = 0
    for i in range(1, n + 1):
        win = sum(1 for j in range(1, n + 1) if beats[i][j])
        lose = sum(1 for j in range(1, n + 1) if beats[j][i])
        if win + lose == n - 1:
            fixed += 1
    return fixed


# ===========================================================================
# 5. Course Schedule IV (LeetCode #1462) - 전이 폐포
#    접근 A: 플로이드-워셜 도달성 (질의 O(1) 조회).
#    접근 B: 각 노드 BFS 로 도달 집합.
# ===========================================================================
class SolutionCourseIV:
    def checkIfPrerequisite(self, numCourses, prerequisites, queries):
        reach = [[False] * numCourses for _ in range(numCourses)]
        for a, b in prerequisites:
            reach[a][b] = True
        for k in range(numCourses):
            for i in range(numCourses):
                if not reach[i][k]:
                    continue
                for j in range(numCourses):
                    if reach[k][j]:
                        reach[i][j] = True
        return [reach[u][v] for u, v in queries]

    def checkIfPrerequisite_bfs(self, numCourses, prerequisites, queries):
        graph = defaultdict(list)
        for a, b in prerequisites:
            graph[a].append(b)
        reach = [[False] * numCourses for _ in range(numCourses)]
        for s in range(numCourses):                  # s 에서 BFS
            q = deque([s])
            while q:
                u = q.popleft()
                for v in graph[u]:
                    if not reach[s][v]:
                        reach[s][v] = True
                        q.append(v)
        return [reach[u][v] for u, v in queries]


# ===========================================================================
# 6. Evaluate Division (LeetCode #399) - 플로이드-워셜 곱(product) 변형
#    ratio[i][j] = i / j. 완화: ratio[i][j] = ratio[i][k] * ratio[k][j].
# ===========================================================================
class SolutionEvalDivision:
    def calcEquation(self, equations, values, queries):
        idx = {}
        for a, b in equations:
            if a not in idx:
                idx[a] = len(idx)
            if b not in idx:
                idx[b] = len(idx)
        m = len(idx)
        ratio = [[0.0] * m for _ in range(m)]
        for i in range(m):
            ratio[i][i] = 1.0
        for (a, b), v in zip(equations, values):
            ia, ib = idx[a], idx[b]
            ratio[ia][ib] = v
            ratio[ib][ia] = 1.0 / v
        for k in range(m):                           # k 최외곽, 곱 전파
            for i in range(m):
                if ratio[i][k] == 0.0:
                    continue
                for j in range(m):
                    if ratio[k][j] != 0.0:
                        ratio[i][j] = ratio[i][k] * ratio[k][j]
        ans = []
        for c, d in queries:
            if c in idx and d in idx and ratio[idx[c]][idx[d]] != 0.0:
                ans.append(ratio[idx[c]][idx[d]])
            else:
                ans.append(-1.0)
        return ans


def run_tests():
    print("=" * 60)
    print("Day 35 - Bellman-Ford & Floyd-Warshall 해설 self-test")
    print("=" * 60)

    # 1. Network Delay Time
    nd = SolutionNetworkDelay()
    assert nd.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2
    assert nd.networkDelayTime([[1, 2, 1]], 2, 1) == 1
    assert nd.networkDelayTime([[1, 2, 1]], 2, 2) == -1      # 1 도달 불가
    print("[1] Network Delay Time (Bellman-Ford)  OK")

    # 2. Cheapest Flights Within K Stops
    cf = SolutionCheapestFlights()
    assert cf.findCheapestPrice(
        4, [[0, 1, 100], [1, 2, 100], [2, 0, 100],
            [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700
    assert cf.findCheapestPrice(
        3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200
    assert cf.findCheapestPrice(
        3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0) == 500
    assert cf.findCheapestPrice(2, [[1, 0, 10]], 0, 1, 1) == -1
    print("[2] Cheapest Flights K Stops (스냅샷)   OK")

    # 3. Find the City
    fc = SolutionFindCity()
    assert fc.findTheCity(
        4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4) == 3
    assert fc.findTheCity(
        5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2],
            [2, 3, 1], [3, 4, 1]], 2) == 0
    print("[3] Find the City (Floyd-Warshall)     OK")

    # 4. 순위 (프로그래머스)
    assert solution(5, [[4, 3], [4, 2], [3, 2], [1, 2], [2, 5]]) == 2
    assert solution(2, [[1, 2]]) == 2                # 둘 다 확정
    assert solution(3, [[1, 2]]) == 0                # 아무도 확정 못 함
    print("[4] 순위 (도달성 Floyd-Warshall)        OK")

    # 5. Course Schedule IV - 두 접근 동일
    ci = SolutionCourseIV()
    cases5 = [
        (2, [[1, 0]], [[0, 1], [1, 0]], [False, True]),
        (3, [[1, 2], [1, 0], [2, 0]],
         [[1, 0], [1, 2]], [True, True]),
        (5, [[0, 1], [1, 2], [2, 3], [3, 4]],
         [[0, 4], [4, 0], [1, 3], [3, 0]], [True, False, True, False]),
    ]
    for nc, pre, q, exp in cases5:
        assert ci.checkIfPrerequisite(nc, pre, q) == exp
        assert ci.checkIfPrerequisite_bfs(nc, pre, q) == exp
    print("[5] Course Schedule IV (전이 폐포)      OK  (Floyd == BFS)")

    # 6. Evaluate Division
    ed = SolutionEvalDivision()
    r = ed.calcEquation([["a", "b"], ["b", "c"]], [2.0, 3.0],
                        [["a", "c"], ["b", "a"], ["a", "e"],
                         ["a", "a"], ["x", "x"]])
    expected = [6.0, 0.5, -1.0, 1.0, -1.0]
    assert all(abs(x - y) < 1e-9 for x, y in zip(r, expected)), r
    r2 = ed.calcEquation([["a", "b"], ["b", "c"], ["bc", "cd"]],
                         [1.5, 2.5, 5.0],
                         [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]])
    exp2 = [3.75, 0.4, 5.0, 0.2]
    assert all(abs(x - y) < 1e-9 for x, y in zip(r2, exp2)), r2
    print("[6] Evaluate Division (곱 변형)         OK")

    print("=" * 60)
    print("모든 테스트 통과 (All tests passed)")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
