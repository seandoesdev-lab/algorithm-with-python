"""Day 38 - 위상 정렬 (Topological Sort) 연습문제 해설.

실행: PYTHONIOENCODING=cp949 python solutions.py

문제 목록 (출처: 프로그래머스 / LeetCode)
  1) LeetCode 207  Course Schedule                 - 사이클 판별
  2) LeetCode 210  Course Schedule II              - 위상 순서 출력
  3) 프로그래머스 49191  순위                       - 도달 가능성으로 순위 확정
  4) LeetCode 802  Find Eventual Safe States       - 역방향 위상 소거
  5) LeetCode 2050 Parallel Courses III            - 위상 순서 위 DP
  6) LeetCode 310  Minimum Height Trees            - 잎 소거

각 문제는 플랫폼 시그니처를 그대로 쓰고, 가능한 경우 여러 접근을 비교한다.
주의: cp949 콘솔 안전을 위해 print 문자열에는 ASCII 기호만 사용한다.
"""

from collections import deque

# ===========================================================================
# 1) LeetCode 207 - Course Schedule
#    https://leetcode.com/problems/course-schedule/
#
#    prerequisites[i] = [a, b]  ->  "b 를 먼저 들어야 a 를 들을 수 있다"
#    따라서 간선은 b -> a 이고 indeg[a] 가 증가한다. (방향 뒤집기가 최다 오답)
#
#    모든 과목 수강 가능? == 위상 정렬이 존재하는가 == DAG 인가 == 사이클이 없는가
# ===========================================================================
class Solution207:
    def canFinish(self, numCourses, prerequisites):
        """접근 1: 칸 알고리즘. 시간 O(V+E), 공간 O(V+E)."""
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)               # b -> a
            indeg[a] += 1

        q = deque(v for v in range(numCourses) if indeg[v] == 0)
        seen = 0
        while q:
            u = q.popleft()
            seen += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        # 못 꺼낸 정점이 남았다면 그것들은 사이클에 갇혀 있다
        return seen == numCourses

    def canFinish_dfs(self, numCourses, prerequisites):
        """접근 2: DFS 3색. 시간 O(V+E), 재귀 스택 O(V).

        bool visited 하나로는 'GRAY(지금 스택 위)' 와 'BLACK(이미 끝남)' 을
        구분할 수 없어 정상 DAG 를 사이클로 오판한다. 반드시 3색.
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        adj = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            adj[b].append(a)

        state = [WHITE] * numCourses

        def has_cycle(u):
            state[u] = GRAY
            for v in adj[u]:
                if state[v] == GRAY:       # back edge
                    return True
                if state[v] == WHITE and has_cycle(v):
                    return True
            state[u] = BLACK
            return False

        return not any(state[s] == WHITE and has_cycle(s)
                       for s in range(numCourses))


def test_207():
    print("[1] LeetCode 207 - Course Schedule")
    s = Solution207()
    cases = [
        (2, [[1, 0]], True),
        (2, [[1, 0], [0, 1]], False),
        (1, [], True),                      # 간선 없음 = 고립 정점
        (5, [[1, 0], [2, 1], [3, 2], [4, 3]], True),      # 사슬
        (3, [[0, 1], [1, 2], [2, 0]], False),             # 3-사이클
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]], True),      # 다이아몬드
    ]
    for n, pre, expected in cases:
        got_bfs = s.canFinish(n, pre)
        got_dfs = s.canFinish_dfs(n, pre)
        assert got_bfs == expected, (n, pre, got_bfs)
        assert got_dfs == expected, (n, pre, got_dfs)
    print("  칸 / DFS 3색 두 접근 모두 통과 - OK")
    print("  n=2, [[1,0]]      ->", s.canFinish(2, [[1, 0]]))
    print("  n=2, [[1,0],[0,1]]->", s.canFinish(2, [[1, 0], [0, 1]]))
    print()


# ===========================================================================
# 2) LeetCode 210 - Course Schedule II
#    https://leetcode.com/problems/course-schedule-ii/
#
#    207 과 같은 입력. 이번엔 실제 수강 순서를 반환한다.
#    유효한 순서가 여러 개면 아무거나 OK, 불가능하면 빈 배열.
# ===========================================================================
class Solution210:
    def findOrder(self, numCourses, prerequisites):
        """접근 1: 칸 알고리즘. order 를 그대로 반환. O(V+E)."""
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)
            indeg[a] += 1

        # 선행이 전혀 없는 과목(고립 정점)도 반드시 포함되어야 한다
        q = deque(v for v in range(numCourses) if indeg[v] == 0)

        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return order if len(order) == numCourses else []

    def findOrder_dfs(self, numCourses, prerequisites):
        """접근 2: DFS post-order 역순. 뒤집는 것을 잊으면 정확히 역순이 나온다."""
        WHITE, GRAY, BLACK = 0, 1, 2
        adj = [[] for _ in range(numCourses)]
        for a, b in prerequisites:
            adj[b].append(a)

        state = [WHITE] * numCourses
        out = []
        cyclic = False

        def visit(u):
            nonlocal cyclic
            state[u] = GRAY
            for v in adj[u]:
                if state[v] == GRAY:
                    cyclic = True
                    return
                if state[v] == WHITE:
                    visit(v)
                    if cyclic:
                        return
            state[u] = BLACK
            out.append(u)                   # 되돌아 나오는 순간 기록

        for s in range(numCourses):
            if state[s] == WHITE:
                visit(s)
                if cyclic:
                    return []
        return out[::-1]

    def findOrder_smallest(self, numCourses, prerequisites):
        """접근 3: 사전 순 최소가 필요할 때. deque -> heapq. O((V+E) log V)."""
        import heapq
        adj = [[] for _ in range(numCourses)]
        indeg = [0] * numCourses
        for a, b in prerequisites:
            adj[b].append(a)
            indeg[a] += 1

        heap = [v for v in range(numCourses) if indeg[v] == 0]
        heapq.heapify(heap)
        order = []
        while heap:
            u = heapq.heappop(heap)
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    heapq.heappush(heap, v)
        return order if len(order) == numCourses else []


def _valid_course_order(n, prerequisites, order):
    """반환된 순서가 실제로 모든 선행 조건을 만족하는지 검증한다."""
    if len(order) != n or set(order) != set(range(n)):
        return False
    pos = {c: i for i, c in enumerate(order)}
    return all(pos[b] < pos[a] for a, b in prerequisites)


def test_210():
    print("[2] LeetCode 210 - Course Schedule II")
    s = Solution210()

    n, pre = 4, [[1, 0], [2, 0], [3, 1], [3, 2]]
    for name, fn in [("칸", s.findOrder),
                     ("DFS", s.findOrder_dfs),
                     ("사전순최소", s.findOrder_smallest)]:
        got = fn(n, pre)
        assert _valid_course_order(n, pre, got), (name, got)
        print("  {:10s}: {}".format(name, got))

    assert s.findOrder(1, []) == [0]
    assert s.findOrder(2, [[1, 0], [0, 1]]) == []       # 사이클 -> 빈 배열
    assert s.findOrder_dfs(2, [[1, 0], [0, 1]]) == []
    # 고립 정점: 과목 2 는 선행 관계가 전혀 없다
    assert sorted(s.findOrder(3, [[1, 0]])) == [0, 1, 2]
    # 사전 순 최소는 실제로 최소여야 한다
    assert s.findOrder_smallest(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) == [0, 1, 2, 3]
    print("  세 접근 모두 유효한 순서 생성 - OK")
    print()


# ===========================================================================
# 3) 프로그래머스 49191 - 순위 (Level 3)
#    https://school.programmers.co.kr/learn/courses/30/lessons/49191
#
#    results[i] = [A, B] : A 가 B 를 이겼다.
#    어떤 선수의 순위가 확정되려면 나머지 n-1 명 전부와 승패 관계가
#    (직접이든 간접이든) 결정되어야 한다.
#      -> (내가 이기는 사람 수) + (나를 이기는 사람 수) == n-1
# ===========================================================================
def solution(n, results):
    """접근 1: 플로이드-워셜 전이 폐쇄. 시간 O(n^3), 공간 O(n^2).

    n <= 100 이므로 100^3 = 100만으로 넉넉하다. 코드가 가장 짧다.
    선수 번호는 1..n (1-based) 이므로 배열을 n+1 크기로 잡는다.
    """
    # reach[a][b] = True  <=>  a 가 b 를 (간접 포함) 이긴다
    reach = [[False] * (n + 1) for _ in range(n + 1)]
    for a, b in results:
        reach[a][b] = True

    # k 를 경유지로 삼아 도달 관계를 전파한다
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            if not reach[i][k]:
                continue                    # i->k 가 없으면 k 경유 불가
            for j in range(1, n + 1):
                if reach[k][j]:
                    reach[i][j] = True

    answer = 0
    for x in range(1, n + 1):
        known = 0
        for y in range(1, n + 1):
            if x == y:
                continue
            if reach[x][y] or reach[y][x]:  # 승패가 어느 쪽으로든 결정됨
                known += 1
        if known == n - 1:
            answer += 1
    return answer


def solution_bfs(n, results):
    """접근 2: 정점마다 양방향 BFS. 시간 O(n*(n+E)), 공간 O(n+E).

    정방향에서 '내가 이기는 사람', 역방향에서 '나를 이기는 사람' 을 센다.
    개념적으로 더 명확하고, n 이 커지면 플로이드보다 빠르다.
    """
    win = [[] for _ in range(n + 1)]        # 정방향: a 가 이긴 상대들
    lose = [[] for _ in range(n + 1)]       # 역방향: a 를 이긴 상대들
    for a, b in results:
        win[a].append(b)
        lose[b].append(a)

    def count_reachable(start, graph):
        visited = [False] * (n + 1)
        visited[start] = True
        q = deque([start])
        cnt = 0
        while q:
            u = q.popleft()
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    cnt += 1
                    q.append(v)
        return cnt

    answer = 0
    for x in range(1, n + 1):
        if count_reachable(x, win) + count_reachable(x, lose) == n - 1:
            answer += 1
    return answer


def test_49191():
    print("[3] 프로그래머스 49191 - 순위")
    cases = [
        # 문제의 예제
        ((5, [[4, 3], [4, 2], [3, 2], [1, 2], [2, 5]]), 2),
        # 완전한 사슬 1>2>3 -> 전원 확정
        ((3, [[1, 2], [2, 3]]), 3),
        # 경기 기록이 하나도 없으면 아무도 확정 불가
        ((3, []), 0),
        # 2명, 한 경기 -> 둘 다 확정
        ((2, [[1, 2]]), 2),
        # 1명이면 비교 대상이 없으므로 확정
        ((1, []), 1),
    ]
    for (n, results), expected in cases:
        got_floyd = solution(n, results)
        got_bfs = solution_bfs(n, results)
        assert got_floyd == expected, (n, results, got_floyd, expected)
        assert got_bfs == expected, (n, results, got_bfs, expected)
    print("  플로이드 O(n^3) / 양방향 BFS 두 접근 모두 통과 - OK")
    print("  예제 n=5 -> 확정 가능한 선수 수:",
          solution(5, [[4, 3], [4, 2], [3, 2], [1, 2], [2, 5]]))
    print()


# ===========================================================================
# 4) LeetCode 802 - Find Eventual Safe States
#    https://leetcode.com/problems/find-eventual-safe-states/
#
#    graph[i] = i 에서 나가는 간선의 도착점들.
#    안전한 노드 = 어떤 경로를 따라가도 반드시 종착 노드에서 끝나는 노드.
#
#    핵심: 간선을 뒤집어 칸을 돌린다. out-degree 0(종착 노드)부터 벗겨진다.
#          207 의 "진입 차수가 0 이 안 된다" 의 거울상.
# ===========================================================================
class Solution802:
    def eventualSafeNodes(self, graph):
        """접근 1: 역방향 그래프 + 칸. 시간 O(V+E), 공간 O(V+E)."""
        n = len(graph)
        rev = [[] for _ in range(n)]
        outdeg = [0] * n
        for u in range(n):
            for v in graph[u]:
                rev[v].append(u)            # 간선 뒤집기
                outdeg[u] += 1

        q = deque(u for u in range(n) if outdeg[u] == 0)   # 종착 노드부터
        safe = [False] * n
        while q:
            u = q.popleft()
            safe[u] = True
            for p in rev[u]:                # 원래 u 로 향하던 노드들
                outdeg[p] -= 1
                if outdeg[p] == 0:          # 모든 출구가 안전 -> p 도 안전
                    q.append(p)
        return [u for u in range(n) if safe[u]]

    def eventualSafeNodes_dfs(self, graph):
        """접근 2: DFS 3색 메모이제이션. 시간 O(V+E).

        state: 0 미방문 / 1 방문중(GRAY) / 2 안전 / 3 위험
        """
        n = len(graph)
        state = [0] * n

        def dfs(u):
            if state[u] == 1:               # 방문중을 다시 만남 -> 사이클
                return False
            if state[u] >= 2:
                return state[u] == 2
            state[u] = 1
            for v in graph[u]:
                if not dfs(v):
                    state[u] = 3            # 출구 하나라도 위험하면 위험
                    return False
            state[u] = 2
            return True

        return [u for u in range(n) if dfs(u)]


def test_802():
    print("[4] LeetCode 802 - Find Eventual Safe States")
    s = Solution802()
    cases = [
        ([[1, 2], [2, 3], [5], [0], [5], [], []], [2, 4, 5, 6]),
        ([[], [0, 2, 3, 4], [3], [4], []], [0, 1, 2, 3, 4]),   # 사이클 없음
        ([[1], [2], [0]], []),                                 # 전부 사이클
        ([[]], [0]),                                           # 단일 종착 노드
    ]
    for graph, expected in cases:
        assert s.eventualSafeNodes(graph) == expected, graph
        assert s.eventualSafeNodes_dfs(graph) == expected, graph
    print("  역방향 칸 / DFS 3색 두 접근 모두 통과 - OK")
    print("  graph=[[1,2],[2,3],[5],[0],[5],[],[]] ->",
          s.eventualSafeNodes([[1, 2], [2, 3], [5], [0], [5], [], []]))
    print()


# ===========================================================================
# 5) LeetCode 2050 - Parallel Courses III
#    https://leetcode.com/problems/parallel-courses-iii/
#
#    relations[j] = [prev, next] (1-based), time[i] = 과목 i+1 의 소요 개월.
#    선행이 전부 끝나야 시작 가능하고, 동시 수강이 가능하다.
#    -> 답은 DAG 최장 경로(critical path). 합이 아니라 max 다.
# ===========================================================================
class Solution2050:
    def minimumTime(self, n, relations, time):
        """칸 알고리즘 위에서 DP. 시간 O(V+E), 공간 O(V+E).

        finish[v] = max(선행 u 들의 finish[u]) + time[v]
        칸이 u 를 꺼내는 시점에 finish[u] 는 이미 최종 확정값이다.
        """
        adj = [[] for _ in range(n + 1)]    # 1-based
        indeg = [0] * (n + 1)
        for prev, nxt in relations:
            adj[prev].append(nxt)
            indeg[nxt] += 1

        finish = [0] * (n + 1)
        q = deque()
        for v in range(1, n + 1):
            if indeg[v] == 0:
                finish[v] = time[v - 1]     # 선행 없음 -> 0 시점에 즉시 시작
                q.append(v)

        while q:
            u = q.popleft()
            for v in adj[u]:
                # time 은 0-indexed 이므로 v-1
                if finish[u] + time[v - 1] > finish[v]:
                    finish[v] = finish[u] + time[v - 1]
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        # 끝나는 지점이 여러 개일 수 있으므로 전체 최댓값
        return max(finish[1:])


def test_2050():
    print("[5] LeetCode 2050 - Parallel Courses III")
    s = Solution2050()
    cases = [
        ((3, [[1, 3], [2, 3]], [3, 2, 5]), 8),
        ((5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]), 12),
        ((1, [], [7]), 7),                              # 과목 하나
        ((3, [], [4, 9, 2]), 9),                        # 전부 병렬 -> 최대값
        ((3, [[1, 2], [2, 3]], [1, 2, 3]), 6),          # 사슬 -> 단순 합
    ]
    for (n, rel, t), expected in cases:
        got = s.minimumTime(n, rel, t)
        assert got == expected, (n, rel, t, got, expected)
    print("  위상 순서 위 DP - OK")
    print("  n=3, relations=[[1,3],[2,3]], time=[3,2,5] ->",
          s.minimumTime(3, [[1, 3], [2, 3]], [3, 2, 5]))
    print("  (1 과 2 를 동시에 시작 -> 3개월 뒤 3 시작 -> 3+5 = 8)")
    print()


# ===========================================================================
# 6) LeetCode 310 - Minimum Height Trees
#    https://leetcode.com/problems/minimum-height-trees/
#
#    무방향 트리에서 높이가 최소가 되는 루트를 모두 반환. 답은 항상 1~2 개.
#    모든 노드를 루트로 BFS 하면 O(V^2) 로 시간 초과 -> 잎 소거로 O(V).
# ===========================================================================
class Solution310:
    def findMinHeightTrees(self, n, edges):
        """잎 소거(leaf peeling). 시간 O(V+E), 공간 O(V+E).

        칸 알고리즘과 골격이 같다. 차이는 'indegree 0' 대신 'degree 1'.
        트리의 중심은 지름(가장 긴 경로)의 중간점이므로,
        양쪽 끝에서 한 층씩 좁혀 들어가면 중심에 도달한다.
        """
        if n == 1:
            return [0]                      # 간선이 없다. 엣지 케이스 필수

        adj = [[] for _ in range(n)]
        deg = [0] * n
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            deg[u] += 1
            deg[v] += 1

        leaves = deque(v for v in range(n) if deg[v] == 1)
        remaining = n
        while remaining > 2:                # 2 개 이하가 남으면 그것이 중심
            # 반드시 '현재 큐 크기만큼만' = 한 층씩 벗긴다
            for _ in range(len(leaves)):
                u = leaves.popleft()
                remaining -= 1
                for v in adj[u]:
                    deg[v] -= 1
                    if deg[v] == 1:         # 새로 잎이 된 노드
                        leaves.append(v)
        return sorted(leaves)

    def findMinHeightTrees_brute(self, n, edges):
        """검증용 무식한 방법: 모든 노드를 루트로 BFS. O(V^2). 작은 입력 전용."""
        if n == 1:
            return [0]
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        def height(root):
            visited = [False] * n
            visited[root] = True
            q = deque([root])
            h = -1
            while q:
                for _ in range(len(q)):
                    u = q.popleft()
                    for v in adj[u]:
                        if not visited[v]:
                            visited[v] = True
                            q.append(v)
                h += 1
            return h

        heights = [height(r) for r in range(n)]
        best = min(heights)
        return [r for r in range(n) if heights[r] == best]


def test_310():
    print("[6] LeetCode 310 - Minimum Height Trees")
    s = Solution310()
    cases = [
        ((4, [[1, 0], [1, 2], [1, 3]]), [1]),
        ((6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]), [3, 4]),
        ((1, []), [0]),                                 # 노드 하나
        ((2, [[0, 1]]), [0, 1]),                        # 노드 둘
        ((5, [[0, 1], [1, 2], [2, 3], [3, 4]]), [2]),   # 경로 5개 -> 중심 1개
        ((4, [[0, 1], [1, 2], [2, 3]]), [1, 2]),        # 경로 4개 -> 중심 2개
    ]
    for (n, edges), expected in cases:
        got = s.findMinHeightTrees(n, edges)
        assert got == expected, (n, edges, got, expected)
        # 무식한 방법과 교차 검증
        assert got == s.findMinHeightTrees_brute(n, edges), (n, edges)
    print("  잎 소거 O(V) / 전수 BFS O(V^2) 결과 일치 - OK")
    print("  n=6, edges=[[3,0],[3,1],[3,2],[3,4],[5,4]] ->",
          s.findMinHeightTrees(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]))
    print()


# ===========================================================================
if __name__ == "__main__":
    print("=" * 62)
    print("Day 38 - 위상 정렬 연습문제 해설")
    print("=" * 62)
    print()

    test_207()
    test_210()
    test_49191()
    test_802()
    test_2050()
    test_310()

    print("=" * 62)
    print("접근법 비교 요약")
    print("  207  사이클 판별      : 칸 O(V+E) / DFS 3색 O(V+E)")
    print("  210  위상 순서 출력   : 칸 O(V+E) / DFS 역순 / 힙 O((V+E)logV)")
    print("  49191 순위 확정       : 플로이드 O(n^3) / 양방향 BFS O(n(n+E))")
    print("  802  안전한 노드      : 역방향 칸 O(V+E) / DFS 3색 O(V+E)")
    print("  2050 최소 완료 시간   : 위상 순서 위 DP O(V+E)")
    print("  310  최소 높이 트리   : 잎 소거 O(V) / 전수 BFS O(V^2)")
    print()
    print("공통 함정")
    print("  - 간선 방향: '먼저 하는 쪽 -> 나중 하는 쪽'. 뒤집으면 조용한 오답")
    print("  - len(order) != V 검사 누락 -> 사이클을 정답으로 착각")
    print("  - 고립 정점을 초기 큐에 넣지 않으면 사이클로 오판")
    print("  - 1-based(프로그래머스) vs 0-based(LeetCode) 혼동")
    print("  - DFS 판별에 bool visited 하나만 쓰면 안 된다 (3색 필수)")
    print("=" * 62)
