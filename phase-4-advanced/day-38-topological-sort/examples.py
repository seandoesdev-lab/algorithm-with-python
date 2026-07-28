"""Day 38 - 위상 정렬 (Topological Sort) 예제 모음.

실행: PYTHONIOENCODING=cp949 python examples.py

다루는 내용
  1) 칸 알고리즘(Kahn) - 진입 차수 기반 위상 정렬 + 사이클 판별
  2) 사전 순 최소 위상 순서 (heapq)
  3) DFS 기반 위상 정렬 - post-order 역순 + 3색 사이클 판별
  4) 위상 순서 유일성 판정 (큐 크기가 항상 1인가)
  5) 칸의 레벨 순회 - 동시에 처리 가능한 작업 묶음
  6) DAG 최장 경로 DP - 작업 완료 최소 시간(critical path)
  7) DAG 최단 경로 - 음수 간선이 있어도 O(V+E)
  8) 역방향 그래프 위상 소거 - out-degree 0 부터 벗기기
  9) 모든 위상 순서 열거 (백트래킹, 작은 V 전용)
 10) 잎 소거(leaf peeling) - 무방향 트리의 중심 찾기

주의: cp949 콘솔 안전을 위해 print 문자열에는 ASCII 기호만 사용한다.
"""

import heapq
from collections import deque

# ---------------------------------------------------------------------------
# 공통 예제 그래프 (concept.md 의 그림과 동일)
#
#    0 ----> 2 ----> 3 ----> 5
#            ^       ^
#            |       |
#    1 ------+-------+----> 4
#
# 간선: 0->2, 1->2, 2->3, 1->3, 3->5, 1->4
# ---------------------------------------------------------------------------
N_DAG = 6
EDGES_DAG = [(0, 2), (1, 2), (2, 3), (1, 3), (3, 5), (1, 4)]

# 사이클이 있는 그래프: 0->1, 1->2, 2->1
N_CYC = 3
EDGES_CYC = [(0, 1), (1, 2), (2, 1)]


def build_adj(n, edges):
    """간선 목록 -> (인접 리스트, 진입 차수 배열)."""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1          # 진입 차수는 항상 '나중에 오는' 쪽에 더한다
    return adj, indeg


def is_valid_topo(n, edges, order):
    """order 가 유효한 위상 순서인지 독립적으로 검증한다."""
    if order is None or len(order) != n or set(order) != set(range(n)):
        return False
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u, v in edges)


# ---------------------------------------------------------------------------
# 1) 칸 알고리즘 (Kahn) - 위상 정렬의 기본형
# ---------------------------------------------------------------------------
def topo_kahn(n, edges):
    """반환: 위상 순서 리스트. 사이클이면 None.

    시간 O(V+E), 공간 O(V+E).
    """
    adj, indeg = build_adj(n, edges)

    # 고립 정점(간선이 하나도 없는 정점)도 진입 차수 0 이므로 반드시 포함된다
    q = deque(v for v in range(n) if indeg[v] == 0)

    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1              # u 가 확정됐으니 v 의 빚 하나를 갚아준다
            if indeg[v] == 0:          # 선행이 전부 끝났다 -> 이제 처리 가능
                q.append(v)

    # 길이 검사를 빼먹으면 사이클 그래프에서 짧은 리스트를 정답인 척 반환한다
    return order if len(order) == n else None


def demo_kahn():
    print("[1] 칸 알고리즘 (Kahn)")
    order = topo_kahn(N_DAG, EDGES_DAG)
    print("  DAG 위상 순서 :", order)
    print("  유효한 순서인가:", is_valid_topo(N_DAG, EDGES_DAG, order))

    bad = topo_kahn(N_CYC, EDGES_CYC)
    print("  사이클 그래프  :", bad, "(None = 위상 정렬 불가)")

    # 고립 정점 포함 예: 정점 3개, 간선 0->1, 정점 2는 고립
    print("  고립 정점 포함 :", topo_kahn(3, [(0, 1)]))
    print()


# ---------------------------------------------------------------------------
# 2) 사전 순 최소 위상 순서 - deque 를 최소 힙으로 교체
# ---------------------------------------------------------------------------
def topo_smallest(n, edges):
    """가능한 위상 순서 중 사전 순으로 가장 앞선 것. 시간 O((V+E) log V)."""
    adj, indeg = build_adj(n, edges)

    heap = [v for v in range(n) if indeg[v] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        u = heapq.heappop(heap)        # 지금 가능한 정점 중 가장 작은 번호
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)
    return order if len(order) == n else None


def demo_smallest():
    print("[2] 사전 순 최소 위상 순서 (heapq)")
    plain = topo_kahn(N_DAG, EDGES_DAG)
    small = topo_smallest(N_DAG, EDGES_DAG)
    print("  일반 칸(deque):", plain)
    print("  사전 순 최소  :", small)
    print("  둘 다 유효한가:", is_valid_topo(N_DAG, EDGES_DAG, plain),
          is_valid_topo(N_DAG, EDGES_DAG, small))
    print("  -> 답이 여러 개인 것이 정상이다")
    print()


# ---------------------------------------------------------------------------
# 3) DFS 기반 위상 정렬 - post-order 역순, 3색 사이클 판별
# ---------------------------------------------------------------------------
WHITE, GRAY, BLACK = 0, 1, 2       # 미방문 / 재귀 스택 위 / 완료


def topo_dfs(n, edges):
    """반환: 위상 순서 리스트. 사이클이면 None.

    bool visited 하나로는 'GRAY(스택 위)' 와 'BLACK(이미 끝남)' 을 구분할 수
    없어 사이클을 놓친다. 방향 그래프 사이클 판별은 반드시 3색이다.
    """
    adj, _ = build_adj(n, edges)

    state = [WHITE] * n
    out = []
    has_cycle = False

    def visit(u):
        nonlocal has_cycle
        state[u] = GRAY
        for v in adj[u]:
            if state[v] == GRAY:       # back edge -> 사이클
                has_cycle = True
                return
            if state[v] == WHITE:
                visit(v)
                if has_cycle:
                    return
        state[u] = BLACK
        out.append(u)                  # 되돌아 나오는 순간 기록 (post-order)

    for s in range(n):
        if state[s] == WHITE:
            visit(s)
            if has_cycle:
                return None
    return out[::-1]                   # 뒤집어야 위상 순서가 된다


def demo_dfs():
    print("[3] DFS 기반 위상 정렬 (post-order 역순)")
    order = topo_dfs(N_DAG, EDGES_DAG)
    print("  DFS 위상 순서 :", order)
    print("  유효한 순서인가:", is_valid_topo(N_DAG, EDGES_DAG, order))
    print("  사이클 그래프  :", topo_dfs(N_CYC, EDGES_CYC), "(None = 사이클)")
    print("  -> 칸과 결과가 달라도 둘 다 정답이다")
    print()


# ---------------------------------------------------------------------------
# 4) 위상 순서가 유일한가 - 큐 크기가 매 단계 정확히 1
# ---------------------------------------------------------------------------
def topo_is_unique(n, edges):
    """유일하면 True. 선택지가 2개 이상인 순간이 있거나 사이클이면 False."""
    adj, indeg = build_adj(n, edges)
    q = deque(v for v in range(n) if indeg[v] == 0)

    seen = 0
    while q:
        if len(q) > 1:                 # 지금 어느 것을 먼저 해도 된다 -> 답이 여럿
            return False
        u = q.popleft()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return seen == n


def demo_unique():
    print("[4] 위상 순서 유일성 판정")
    # 사슬 0->1->2 는 순서가 하나로 확정된다 (해밀턴 경로가 존재)
    chain = [(0, 1), (1, 2)]
    print("  사슬 0->1->2  :", topo_is_unique(3, chain), "(유일)")
    print("  예제 DAG      :", topo_is_unique(N_DAG, EDGES_DAG), "(여러 개)")
    print("  사이클 그래프  :", topo_is_unique(N_CYC, EDGES_CYC), "(불가)")
    print("  -> 유일 <=> 인접한 모든 쌍이 간선으로 강제됨(해밀턴 경로)")
    print()


# ---------------------------------------------------------------------------
# 5) 칸의 레벨 순회 - 동시에 처리 가능한 작업 묶음
# ---------------------------------------------------------------------------
def topo_levels(n, edges):
    """반환: 레벨 리스트의 리스트. 사이클이면 None.

    한 레벨 안의 작업들은 서로 의존이 없어 병렬 처리가 가능하다.
    레벨 수 = '최소 몇 단계(학기)가 필요한가' 의 답.
    """
    adj, indeg = build_adj(n, edges)
    q = deque(v for v in range(n) if indeg[v] == 0)

    levels = []
    seen = 0
    while q:
        level = []
        for _ in range(len(q)):        # 지금 큐에 있는 만큼만 = 한 층
            u = q.popleft()
            level.append(u)
            seen += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        levels.append(level)
    return levels if seen == n else None


def demo_levels():
    print("[5] 칸의 레벨 순회 (동시 처리 가능한 묶음)")
    levels = topo_levels(N_DAG, EDGES_DAG)
    for i, level in enumerate(levels):
        print("  레벨", i, ":", level)
    print("  필요한 최소 단계 수:", len(levels))
    print()


# ---------------------------------------------------------------------------
# 6) DAG 최장 경로 DP - 작업 완료 최소 시간 (critical path)
# ---------------------------------------------------------------------------
def dag_min_finish_time(n, edges, cost):
    """cost[i] = 작업 i 소요 시간. 선행 작업이 모두 끝나야 시작할 수 있다.

    전부 끝내는 최소 시간 = DAG 최장 경로. 시간 O(V+E).
    사이클이면 -1.
    """
    adj, indeg = build_adj(n, edges)

    finish = [0] * n
    q = deque()
    for v in range(n):
        if indeg[v] == 0:
            finish[v] = cost[v]        # 선행 없음 -> 0 시점에 즉시 시작
            q.append(v)

    done = 0
    while q:
        u = q.popleft()
        done += 1
        for v in adj[u]:
            # u 를 꺼낸 시점에 finish[u] 는 이미 최종 확정값이다.
            # 이것이 위상 순서가 DP 를 성립시키는 이유.
            finish[v] = max(finish[v], finish[u] + cost[v])
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return max(finish) if done == n else -1


def demo_dag_dp():
    print("[6] DAG 최장 경로 DP (작업 완료 최소 시간)")
    cost = [3, 2, 5, 4, 1, 2]          # 정점 0~5 의 소요 시간
    print("  각 작업 소요 시간:", cost)
    print("  전부 끝내는 최소 시간:", dag_min_finish_time(N_DAG, EDGES_DAG, cost))
    # 손계산: 0(3) -> 2(5) -> 3(4) -> 5(2) = 14
    #         1(2) -> 2(5) -> 3(4) -> 5(2) = 13  -> 최대 14
    print("  (critical path 0->2->3->5 = 3+5+4+2 = 14)")
    print("  사이클이면      :", dag_min_finish_time(N_CYC, EDGES_CYC, [1, 1, 1]))
    print("  -> 일반 그래프 최장 경로는 NP-난해지만 DAG 면 O(V+E)")
    print()


# ---------------------------------------------------------------------------
# 7) DAG 최단 경로 - 음수 간선이 있어도 O(V+E)
# ---------------------------------------------------------------------------
INF = float("inf")


def dag_shortest_path(n, weighted_edges, src):
    """weighted_edges = [(u, v, w), ...]. 음수 w 도 허용된다.

    다익스트라는 음수에서 깨지고 벨만-포드는 O(VE) 인데,
    DAG 라면 위상 순서 한 번 훑기로 O(V+E) 에 끝난다.
    """
    edges = [(u, v) for u, v, _ in weighted_edges]
    order = topo_kahn(n, edges)
    if order is None:
        return None                    # DAG 가 아니면 이 방법을 쓸 수 없다

    adj = [[] for _ in range(n)]
    for u, v, w in weighted_edges:
        adj[u].append((v, w))

    dist = [INF] * n
    dist[src] = 0
    for u in order:                    # 위상 순서대로 훑으면 완화가 한 번이면 충분
        if dist[u] == INF:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


def demo_dag_shortest():
    print("[7] DAG 최단 경로 (음수 간선 허용, O(V+E))")
    wedges = [(0, 2, 3), (1, 2, 1), (2, 3, -4), (1, 3, 2), (3, 5, 6), (1, 4, 5)]
    dist = dag_shortest_path(N_DAG, wedges, src=0)
    shown = ["INF" if d == INF else str(d) for d in dist]
    print("  간선(음수 -4 포함):", wedges)
    print("  0 번에서의 최단 거리:", shown)
    print("  -> 0->2(3) ->3(-4) = -1, ->5(6) = 5")
    print()


# ---------------------------------------------------------------------------
# 8) 역방향 그래프 위상 소거 - out-degree 0 부터 벗겨내기
# ---------------------------------------------------------------------------
def eventual_safe_nodes(graph):
    """graph[i] = i 에서 나가는 간선의 도착 정점 목록.

    '어떤 경로를 따라가도 반드시 종착점(나가는 간선 없음)에 도달하는' 정점을
    찾는다. 간선을 뒤집어 칸을 돌리면 out-degree 0 부터 벗겨진다.
    LeetCode 802 의 골격.
    """
    n = len(graph)
    rev = [[] for _ in range(n)]
    outdeg = [0] * n
    for u in range(n):
        for v in graph[u]:
            rev[v].append(u)           # 간선 뒤집기
            outdeg[u] += 1

    q = deque(u for u in range(n) if outdeg[u] == 0)   # 종착점부터 시작
    safe = [False] * n
    while q:
        u = q.popleft()
        safe[u] = True
        for p in rev[u]:               # u 로 들어오던 정점들
            outdeg[p] -= 1
            if outdeg[p] == 0:         # 모든 출구가 안전 -> p 도 안전
                q.append(p)
    return [u for u in range(n) if safe[u]]


def demo_reverse():
    print("[8] 역방향 그래프 위상 소거 (안전한 정점 찾기)")
    graph = [[1, 2], [2, 3], [5], [0], [5], [], []]
    print("  graph :", graph)
    print("  안전한 정점:", eventual_safe_nodes(graph))
    print("  -> 정답 [2,4,5,6]. 0,1,3 은 사이클 0->1->3->0 에 갇혀 있다")
    print()


# ---------------------------------------------------------------------------
# 9) 모든 위상 순서 열거 (백트래킹) - V 가 작을 때만
# ---------------------------------------------------------------------------
def all_topo_orders(n, edges):
    """가능한 모든 위상 순서를 반환. 최악 O(V!) 이므로 V <= 10 정도만."""
    adj, indeg = build_adj(n, edges)
    indeg = list(indeg)
    used = [False] * n
    result = []
    path = []

    def backtrack():
        if len(path) == n:
            result.append(path[:])
            return
        for u in range(n):
            if not used[u] and indeg[u] == 0:
                used[u] = True                 # u 를 지금 선택
                for v in adj[u]:
                    indeg[v] -= 1
                path.append(u)

                backtrack()

                path.pop()                     # 되돌리기
                for v in adj[u]:
                    indeg[v] += 1
                used[u] = False

    backtrack()
    return result


def demo_all_orders():
    print("[9] 모든 위상 순서 열거 (백트래킹)")
    small_edges = [(0, 1), (0, 2)]     # 0 다음에 1,2 는 아무 순서나 가능
    orders = all_topo_orders(3, small_edges)
    print("  간선 0->1, 0->2 의 모든 위상 순서:", orders)
    total = len(all_topo_orders(N_DAG, EDGES_DAG))
    print("  예제 DAG 의 위상 순서 개수:", total)
    print("  사이클 그래프의 개수      :", len(all_topo_orders(N_CYC, EDGES_CYC)))
    print()


# ---------------------------------------------------------------------------
# 10) 잎 소거(leaf peeling) - 무방향 트리의 중심 찾기
# ---------------------------------------------------------------------------
def tree_centroids(n, undirected_edges):
    """무방향 트리에서 차수 1 인 잎을 한 층씩 벗겨 남는 1~2 개를 반환.

    칸 알고리즘과 골격이 같다. 차이는 'indegree 0' 대신 'degree 1'.
    LeetCode 310 Minimum Height Trees 의 핵심.
    """
    if n == 1:
        return [0]

    adj = [[] for _ in range(n)]
    deg = [0] * n
    for u, v in undirected_edges:
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    leaves = deque(v for v in range(n) if deg[v] == 1)
    remaining = n
    while remaining > 2:                       # 남은 정점이 2 개 이하가 되면 멈춤
        for _ in range(len(leaves)):
            u = leaves.popleft()
            remaining -= 1
            for v in adj[u]:
                deg[v] -= 1
                if deg[v] == 1:                # 새로 잎이 된 정점
                    leaves.append(v)
    return sorted(leaves)


def demo_peeling():
    print("[10] 잎 소거 - 무방향 트리의 중심")
    #   0
    #   |
    #   1 -- 2
    #   |
    #   3
    tree1 = [(0, 1), (1, 2), (1, 3)]
    print("  트리 0-1, 1-2, 1-3 의 중심:", tree_centroids(4, tree1))

    #  0 -- 1 -- 2 -- 3 -- 4  (경로 그래프, 정점 5개 -> 중심 1개)
    tree2 = [(0, 1), (1, 2), (2, 3), (3, 4)]
    print("  경로 0-1-2-3-4 의 중심   :", tree_centroids(5, tree2))

    tree3 = [(0, 1), (1, 2), (2, 3)]          # 정점 4 개 경로 -> 중심 2 개
    print("  경로 0-1-2-3 의 중심     :", tree_centroids(4, tree3))
    print("  -> 남는 정점은 항상 1 개 또는 2 개")
    print()


# ---------------------------------------------------------------------------
# 자체 검증
# ---------------------------------------------------------------------------
def run_selftest():
    print("[selftest] 자체 검증")

    # 칸과 DFS 모두 유효한 위상 순서를 만든다
    assert is_valid_topo(N_DAG, EDGES_DAG, topo_kahn(N_DAG, EDGES_DAG))
    assert is_valid_topo(N_DAG, EDGES_DAG, topo_dfs(N_DAG, EDGES_DAG))
    assert is_valid_topo(N_DAG, EDGES_DAG, topo_smallest(N_DAG, EDGES_DAG))

    # 사이클이면 셋 다 None
    assert topo_kahn(N_CYC, EDGES_CYC) is None
    assert topo_dfs(N_CYC, EDGES_CYC) is None
    assert topo_smallest(N_CYC, EDGES_CYC) is None

    # 사전 순 최소는 실제로 모든 위상 순서 중 최소여야 한다
    assert topo_smallest(N_DAG, EDGES_DAG) == min(all_topo_orders(N_DAG, EDGES_DAG))

    # 고립 정점을 빠뜨리면 안 된다
    assert sorted(topo_kahn(3, [(0, 1)])) == [0, 1, 2]

    # 유일성
    assert topo_is_unique(3, [(0, 1), (1, 2)]) is True
    assert topo_is_unique(N_DAG, EDGES_DAG) is False
    assert topo_is_unique(N_CYC, EDGES_CYC) is False

    # 레벨 순회의 정점 총합은 n
    levels = topo_levels(N_DAG, EDGES_DAG)
    assert sum(len(x) for x in levels) == N_DAG
    assert topo_levels(N_CYC, EDGES_CYC) is None

    # DAG 최장 경로
    assert dag_min_finish_time(N_DAG, EDGES_DAG, [3, 2, 5, 4, 1, 2]) == 14
    assert dag_min_finish_time(N_CYC, EDGES_CYC, [1, 1, 1]) == -1
    # 사슬 0->1->2 는 단순 합
    assert dag_min_finish_time(3, [(0, 1), (1, 2)], [1, 2, 3]) == 6

    # DAG 최단 경로 (음수 간선 포함)
    wedges = [(0, 2, 3), (1, 2, 1), (2, 3, -4), (1, 3, 2), (3, 5, 6), (1, 4, 5)]
    dist = dag_shortest_path(N_DAG, wedges, src=0)
    assert dist[0] == 0 and dist[2] == 3 and dist[3] == -1 and dist[5] == 5
    assert dist[1] == INF and dist[4] == INF

    # 역방향 소거
    assert eventual_safe_nodes([[1, 2], [2, 3], [5], [0], [5], [], []]) == [2, 4, 5, 6]
    assert eventual_safe_nodes([[], [0, 2, 3, 4], [3], [4], []]) == [0, 1, 2, 3, 4]

    # 모든 위상 순서 열거
    assert sorted(all_topo_orders(3, [(0, 1), (0, 2)])) == [[0, 1, 2], [0, 2, 1]]
    assert all_topo_orders(N_CYC, EDGES_CYC) == []
    for od in all_topo_orders(N_DAG, EDGES_DAG):
        assert is_valid_topo(N_DAG, EDGES_DAG, od)

    # 잎 소거
    assert tree_centroids(1, []) == [0]
    assert tree_centroids(2, [(0, 1)]) == [0, 1]
    assert tree_centroids(4, [(0, 1), (1, 2), (1, 3)]) == [1]
    assert tree_centroids(5, [(0, 1), (1, 2), (2, 3), (3, 4)]) == [2]
    assert tree_centroids(4, [(0, 1), (1, 2), (2, 3)]) == [1, 2]

    print("  all assertions passed - OK")
    print()


if __name__ == "__main__":
    print("=" * 62)
    print("Day 38 - 위상 정렬 (Topological Sort)")
    print("=" * 62)
    print()

    demo_kahn()
    demo_smallest()
    demo_dfs()
    demo_unique()
    demo_levels()
    demo_dag_dp()
    demo_dag_shortest()
    demo_reverse()
    demo_all_orders()
    demo_peeling()
    run_selftest()

    print("=" * 62)
    print("핵심 정리")
    print("  - 위상 정렬은 DAG 에서만 존재한다 (사이클 <-> 불가)")
    print("  - 칸: indegree 0 을 큐에 넣고, 꺼낼 때마다 이웃의 빚을 갚는다")
    print("  - len(order) != V 검사를 빼먹으면 조용한 오답")
    print("  - DFS 판별은 반드시 3색(WHITE/GRAY/BLACK)")
    print("  - 간선 방향은 '먼저 하는 쪽 -> 나중 하는 쪽'")
    print("  - 위상 순서는 DAG DP 의 계산 순서를 공짜로 준다")
    print("=" * 62)
