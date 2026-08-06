# -*- coding: utf-8 -*-
"""Day 44 - 트리 DP (Tree DP: 서브트리 집계·리루팅) 예제 모음

실행:  PYTHONIOENCODING=cp949 python examples.py

다루는 것
  0. 공통 유틸 - 무향 트리에 루트를 정해 parent/depth/BFS순서 만들기 (재귀 0줄)
  1. 순수 집계형   - 서브트리 크기·합·높이
  2. 경로형        - 트리 지름 (올려보내는 값 != 정답), BFS 두 번 방식과 교차 검증
  3. 상태 추가형   - 최대 가중 독립 집합 (House Robber III 의 일반형)
  4. 다중 상태형   - 최소 카메라 수 (3-state DP) vs 그리디
  5. 리루팅        - 모든 노드에서 다른 모든 노드까지의 거리 합, 나이브와 대조
  6. 재귀 한도     - 체인 트리에서 재귀가 죽고 반복이 사는 것을 실제로 보여준다

표준 라이브러리만 사용한다.
"""

from collections import deque
import random
import sys
import time


# =====================================================================
# 0. 공통 유틸
# =====================================================================
def root_tree(adj, root=0):
    """무향 트리에 루트를 정해 parent / depth / BFS순서를 만든다.

    BFS 순서는 "부모가 자식보다 항상 앞"이므로
    reversed(order) 로 돌면 후위 순회와 같은 효과가 난다. 재귀가 필요 없다.
    """
    n = len(adj)
    parent, depth = [-1] * n, [0] * n
    visited = [False] * n
    visited[root] = True
    order = [root]
    dq = deque([root])
    while dq:
        v = dq.popleft()
        for w in adj[v]:
            if not visited[w]:
                visited[w] = True
                parent[w] = v
                depth[w] = depth[v] + 1
                order.append(w)
                dq.append(w)
    return parent, depth, order


def build_adj(n, edges):
    """무향 인접 리스트를 만든다."""
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def random_tree(n, seed=None):
    """항상 유효한 무작위 트리를 만든다 (parent[i] = randint(0, i-1) 트릭).

    i 의 부모를 반드시 자기보다 작은 번호로 잡으므로 사이클이 생길 수 없다.
    """
    rng = random.Random(seed)
    edges = [(i, rng.randint(0, i - 1)) for i in range(1, n)]
    return build_adj(n, edges), edges


def chain_tree(n):
    """0 - 1 - 2 - ... - (n-1) 체인. 재귀 킬러."""
    return build_adj(n, [(i, i + 1) for i in range(n - 1)])


# =====================================================================
# 1. 순수 집계형 - 서브트리 크기 / 합 / 높이
# =====================================================================
def subtree_size_and_sum(adj, weight, root=0):
    """서브트리 노드 수와 서브트리 가중치 합. O(N)."""
    n = len(adj)
    parent, _, order = root_tree(adj, root)
    size = [1] * n
    total = weight[:]
    for v in reversed(order):          # 자식이 부모보다 먼저 처리된다
        p = parent[v]
        if p != -1:
            size[p] += size[v]         # "밀기(push)" 스타일
            total[p] += total[v]
    return size, total


def subtree_height(adj, root=0):
    """각 노드의 서브트리 높이(아래로 몇 칸). 잎은 0."""
    n = len(adj)
    parent, _, order = root_tree(adj, root)
    height = [0] * n
    for v in reversed(order):
        p = parent[v]
        if p != -1 and height[v] + 1 > height[p]:
            height[p] = height[v] + 1
    return height


def demo_aggregate():
    print("=" * 62)
    print("1. 순수 집계형 - 서브트리 크기 / 합 / 높이")
    print("=" * 62)
    #        0
    #      /   \
    #     1     2
    #    / \     \
    #   3   4     5
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    adj = build_adj(6, edges)
    weight = [10, 20, 30, 40, 50, 60]
    size, total = subtree_size_and_sum(adj, weight)
    height = subtree_height(adj)
    print("  트리: 0-(1,2), 1-(3,4), 2-(5)")
    print("  weight  =", weight)
    print("  size    =", size, "  <- 서브트리 노드 수")
    print("  total   =", total, "  <- 서브트리 가중치 합")
    print("  height  =", height, "  <- 서브트리 높이(잎=0)")
    assert size == [6, 3, 2, 1, 1, 1]
    assert total[0] == sum(weight)
    assert total[1] == 20 + 40 + 50
    assert height == [2, 1, 1, 0, 0, 0]
    print("  검증 OK")
    print()


# =====================================================================
# 2. 경로형 - 트리 지름 (올려보내는 값 != 정답)
# =====================================================================
def tree_diameter_dp(adj, root=0):
    """트리 DP 로 지름(가장 먼 두 노드 사이 간선 수)을 구한다. O(N).

    down[v] : v 에서 아래로 "한 갈래"만 타고 내려가는 최장 -> 부모에게 올려보낸다
    best    : v 에서 "두 갈래"로 꺾이는 최장               -> 정답에 기록한다
    """
    n = len(adj)
    parent, _, order = root_tree(adj, root)
    down = [0] * n
    best = 0
    for v in reversed(order):
        top1 = top2 = 0                    # 자식 방향 깊이 상위 2개
        for w in adj[v]:
            if w == parent[v]:
                continue
            d = down[w] + 1
            if d > top1:
                top1, top2 = d, top1
            elif d > top2:
                top2 = d
        down[v] = top1                     # 부모에게는 한 갈래만
        if top1 + top2 > best:
            best = top1 + top2             # 정답에는 두 갈래
    return best


def tree_diameter_two_bfs(adj):
    """BFS 두 번으로 지름 구하기 (가중치가 모두 음이 아닐 때만 성립).

    아무 노드에서 가장 먼 노드 u 를 찾고, u 에서 가장 먼 거리가 곧 지름이다.
    """
    def farthest(src):
        n = len(adj)
        dist = [-1] * n
        dist[src] = 0
        dq = deque([src])
        far, fard = src, 0
        while dq:
            v = dq.popleft()
            for w in adj[v]:
                if dist[w] == -1:
                    dist[w] = dist[v] + 1
                    if dist[w] > fard:
                        far, fard = w, dist[w]
                    dq.append(w)
        return far, fard

    u, _ = farthest(0)
    _, d = farthest(u)
    return d


def demo_diameter():
    print("=" * 62)
    print("2. 경로형 - 트리 지름 (올려보내는 값 != 정답)")
    print("=" * 62)
    #        a=0
    #      /     \
    #     b=1     c=2
    #    /  \
    #   d=3  e=4
    #        /
    #       f=5
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5)]
    adj = build_adj(6, edges)
    d1 = tree_diameter_dp(adj)
    d2 = tree_diameter_two_bfs(adj)
    print("  트리 DP   지름 =", d1, "  (최장 경로 5-4-1-0-2)")
    print("  BFS 두 번 지름 =", d2)
    assert d1 == d2 == 4

    print("  체인 10개짜리 지름 =", tree_diameter_dp(chain_tree(10)), "(기대 9)")
    assert tree_diameter_dp(chain_tree(10)) == 9

    # 무작위 트리 교차 검증 - 두 방식이 항상 같아야 한다
    for seed in range(40):
        size = random.Random(seed).randint(2, 60)
        adj_r, _ = random_tree(size, seed=seed)
        assert tree_diameter_dp(adj_r) == tree_diameter_two_bfs(adj_r), seed
    print("  무작위 트리 40개 교차 검증(트리DP vs BFS두번) OK")
    print()


# =====================================================================
# 3. 상태 추가형 - 최대 가중 독립 집합 (House Robber III 의 일반형)
# =====================================================================
def max_weight_independent_set(adj, weight, root=0):
    """인접한 두 노드를 동시에 고를 수 없을 때 가중치 합의 최댓값. O(N).

    skip[v] = v 를 안 쓸 때 v 의 서브트리 최댓값
    take[v] = v 를 쓸 때   v 의 서브트리 최댓값
    """
    n = len(adj)
    parent, _, order = root_tree(adj, root)
    skip = [0] * n
    take = weight[:]
    for v in reversed(order):
        p = parent[v]
        if p != -1:
            skip[p] += max(skip[v], take[v])   # 부모가 안 쓰면 자식은 자유
            take[p] += skip[v]                 # 부모가 쓰면 자식은 못 쓴다
    return max(skip[root], take[root])


def mwis_bruteforce(adj, weight):
    """모든 부분집합을 시도하는 나이브(검증 전용). n 이 작을 때만."""
    n = len(adj)
    best = 0
    for mask in range(1 << n):
        ok = True
        for v in range(n):
            if not (mask >> v) & 1:
                continue
            for w in adj[v]:
                if w > v and (mask >> w) & 1:   # 인접한 둘을 같이 골랐다
                    ok = False
                    break
            if not ok:
                break
        if ok:
            s = sum(weight[v] for v in range(n) if (mask >> v) & 1)
            if s > best:
                best = s
    return best


def demo_independent_set():
    print("=" * 62)
    print("3. 상태 추가형 - 최대 가중 독립 집합 (dp[v][0/1])")
    print("=" * 62)
    #      3(0)
    #     /    \
    #    2(1)   3(2)
    #      \      \
    #      3(3)   1(4)
    edges = [(0, 1), (0, 2), (1, 3), (2, 4)]
    adj = build_adj(5, edges)
    weight = [3, 2, 3, 3, 1]
    got = max_weight_independent_set(adj, weight)
    print("  LeetCode #337 예제1 트리, 기대 7, 결과 =", got)
    assert got == 7

    for seed in range(30):
        n = random.Random(seed * 7).randint(1, 12)
        adj_r, _ = random_tree(n, seed=seed)
        w = [random.Random(seed * 13 + i).randint(0, 30) for i in range(n)]
        assert max_weight_independent_set(adj_r, w) == mwis_bruteforce(adj_r, w), seed
    print("  무작위 트리 30개 교차 검증(트리DP vs 부분집합 전수) OK")
    print()


# =====================================================================
# 4. 다중 상태형 - 최소 카메라 수 (3-state DP) vs 그리디
#    무향 인접 리스트 버전 (이진 트리가 아니라 일반 트리로 일반화했다)
# =====================================================================
INF = float("inf")


def min_cameras_dp(adj, root=0):
    """모든 노드를 감시하는 최소 카메라 수. 3-state 트리 DP. O(N).

    A[v] = v 에 카메라를 설치한다
    B[v] = v 에 카메라는 없지만 감시되고 있다 (자식 중 누군가에 카메라)
    C[v] = v 에 카메라도 없고 감시되지도 않는다 (부모가 책임진다.
           단 v 의 자식들은 모두 감시되어 있어야 한다)
    """
    n = len(adj)
    parent, _, order = root_tree(adj, root)
    A = [1] * n          # 자기 자신에 카메라 1대
    B = [0] * n
    C = [0] * n
    for v in reversed(order):
        kids = [w for w in adj[v] if w != parent[v]]
        if not kids:                       # 잎
            A[v], B[v], C[v] = 1, INF, 0   # 잎은 자식이 없으니 감시받을 수 없다
            continue
        a = 1
        c = 0
        # B 는 "자식 중 최소 한 명은 카메라(A)" 이므로
        # 먼저 모두 min(A, B) 로 두고, 카메라가 하나도 없으면 가장 손해가 적은
        # 자식 하나를 A 로 바꾸는 비용(delta)을 더한다.
        base = 0
        has_camera = False
        delta = INF
        for w in kids:
            a += min(A[w], B[w], C[w])     # 내가 카메라면 자식은 무엇이든 OK
            c += B[w]                      # 자식들은 감시되어 있되 카메라는 없다
            base += min(A[w], B[w])
            if A[w] <= B[w]:
                has_camera = True
            else:
                delta = min(delta, A[w] - B[w])
        if has_camera:
            b = base
        elif delta < INF:
            b = base + delta
        else:
            b = INF
        A[v], B[v], C[v] = a, b, c
    return min(A[root], B[root])           # C[root] 는 안 된다 - 루트 위에 부모가 없다


def min_cameras_greedy(adj, root=0):
    """아래에서 위로 올라가며 "감시 안 된 자식이 있으면 나에게 카메라". O(N).

    상태: 0 = 감시 안 됨, 1 = 감시됨(카메라 없음), 2 = 카메라 있음
    """
    n = len(adj)
    parent, _, order = root_tree(adj, root)
    state = [0] * n
    count = 0
    for v in reversed(order):
        kids = [w for w in adj[v] if w != parent[v]]
        if any(state[w] == 0 for w in kids):
            state[v] = 2                   # 감시 안 된 자식이 있다 -> 내가 카메라
            count += 1
        elif any(state[w] == 2 for w in kids):
            state[v] = 1                   # 자식 카메라가 나를 감시한다
        else:
            state[v] = 0                   # 부모가 책임진다
    if state[root] == 0:                   # 루트 위에는 부모가 없다
        count += 1
    return count


def demo_cameras():
    print("=" * 62)
    print("4. 다중 상태형 - 최소 카메라 수 (3-state DP vs 그리디)")
    print("=" * 62)
    # LeetCode #968 예제1: [0,0,null,0,0]  ->  0-1, 1-2, 1-3   답 1
    adj1 = build_adj(4, [(0, 1), (1, 2), (1, 3)])
    # LeetCode #968 예제2: 체인 5개                            답 2
    adj2 = chain_tree(5)
    print("  예제1 (0-1, 1-(2,3)):  DP =", min_cameras_dp(adj1),
          " 그리디 =", min_cameras_greedy(adj1), " (기대 1)")
    print("  예제2 (체인 5개):      DP =", min_cameras_dp(adj2),
          " 그리디 =", min_cameras_greedy(adj2), " (기대 2)")
    assert min_cameras_dp(adj1) == min_cameras_greedy(adj1) == 1
    assert min_cameras_dp(adj2) == min_cameras_greedy(adj2) == 2
    assert min_cameras_dp(build_adj(1, [])) == 1      # 노드 1개면 카메라 1대

    for seed in range(60):
        n = random.Random(seed * 3 + 1).randint(1, 40)
        adj_r, _ = random_tree(n, seed=seed)
        assert min_cameras_dp(adj_r) == min_cameras_greedy(adj_r), seed
    print("  무작위 트리 60개 교차 검증(3-state DP vs 그리디) OK")
    print()


# =====================================================================
# 5. 리루팅 - 모든 노드에서 다른 모든 노드까지의 거리 합 (LeetCode #834)
# =====================================================================
def sum_of_distances_rerooting(n, edges):
    """리루팅 2-pass. O(N).

    1차(아래->위): cnt[v] = 서브트리 크기,  ans[root] = 루트 기준 거리 합
    2차(위->아래): ans[c] = ans[p] - cnt[c] + (n - cnt[c])
                   c 쪽 노드는 1 씩 가까워지고 나머지는 1 씩 멀어진다
    """
    adj = build_adj(n, edges)
    parent, _, order = root_tree(adj, 0)
    cnt = [1] * n
    ans = [0] * n
    for v in reversed(order):              # 1차
        p = parent[v]
        if p != -1:
            cnt[p] += cnt[v]
            ans[p] += ans[v] + cnt[v]
    for v in order[1:]:                    # 2차 - 순서가 정반대!
        p = parent[v]
        ans[v] = ans[p] - cnt[v] + (n - cnt[v])
    return ans


def sum_of_distances_naive(n, edges):
    """각 노드에서 BFS 를 한 번씩. O(N^2). 검증 전용."""
    adj = build_adj(n, edges)
    out = []
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        dq = deque([s])
        while dq:
            v = dq.popleft()
            for w in adj[v]:
                if dist[w] == -1:
                    dist[w] = dist[v] + 1
                    dq.append(w)
        out.append(sum(dist))
    return out


def demo_rerooting():
    print("=" * 62)
    print("5. 리루팅 - 모든 노드까지의 거리 합 (LeetCode #834)")
    print("=" * 62)
    n, edges = 6, [(0, 1), (0, 2), (2, 3), (2, 4), (2, 5)]
    got = sum_of_distances_rerooting(n, edges)
    print("  n=6, edges=[[0,1],[0,2],[2,3],[2,4],[2,5]]")
    print("  결과   =", got)
    print("  기대   = [8, 12, 6, 10, 10, 10]")
    assert got == [8, 12, 6, 10, 10, 10]
    assert sum_of_distances_rerooting(1, []) == [0]
    assert sum_of_distances_rerooting(2, [(1, 0)]) == [1, 1]

    for seed in range(40):
        m = random.Random(seed * 11).randint(1, 50)
        _, edges_r = random_tree(m, seed=seed)
        assert sum_of_distances_rerooting(m, edges_r) == sum_of_distances_naive(m, edges_r), seed
    print("  무작위 트리 40개 교차 검증(리루팅 vs 나이브 O(N^2)) OK")

    # 실측: 리루팅이 나이브보다 얼마나 빠른가
    m = 1200
    _, edges_big = random_tree(m, seed=99)
    t0 = time.perf_counter()
    fast = sum_of_distances_rerooting(m, edges_big)
    t1 = time.perf_counter()
    slow = sum_of_distances_naive(m, edges_big)
    t2 = time.perf_counter()
    assert fast == slow
    print("  n=1200 실측:  리루팅 %.4fs  나이브 %.4fs" % (t1 - t0, t2 - t1))
    print("  (n 이 커질수록 격차가 제곱으로 벌어진다)")
    print()


# =====================================================================
# 6. 재귀 한도 - 체인 트리에서 재귀는 죽고 반복은 산다
# =====================================================================
def demo_recursion_limit():
    print("=" * 62)
    print("6. 재귀 한도 - 체인 트리에서 재귀 vs 반복")
    print("=" * 62)
    n = 5000
    adj = chain_tree(n)
    print("  체인 길이 =", n, ",  현재 재귀 한도 =", sys.getrecursionlimit())

    def rec_depth(v, p):
        best = 0
        for w in adj[v]:
            if w != p:
                d = rec_depth(w, v) + 1
                if d > best:
                    best = d
        return best

    try:
        rec_depth(0, -1)
        print("  재귀 DFS: 성공 (이 환경의 한도가 충분했다)")
    except RecursionError:
        print("  재귀 DFS: RecursionError 발생! - 체인 깊이가 재귀 한도를 넘었다")

    got = tree_diameter_dp(adj)
    print("  반복 트리 DP: 정상 동작, 지름 =", got, "(기대", n - 1, ")")
    assert got == n - 1
    print("  결론: 복잡도는 둘 다 O(N) 이지만 재귀는 '죽고' 반복은 '산다'")
    print()


if __name__ == "__main__":
    demo_aggregate()
    demo_diameter()
    demo_independent_set()
    demo_cameras()
    demo_rerooting()
    demo_recursion_limit()
    print("=" * 62)
    print("모든 예제 실행 완료 - Day 44 트리 DP")
    print("=" * 62)
