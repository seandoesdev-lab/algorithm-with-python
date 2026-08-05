"""Day 43 - 최소 공통 조상 (LCA: Lowest Common Ancestor) 예제 모음

실행:  PYTHONIOENCODING=cp949 python examples.py

다루는 것
  1) BFS 로 루트 정하기 (parent / depth / 방문순서) - 재귀 없음
  2) 나이브 LCA (루트 경로의 공통 접두사) - 검증 기준선
  3) 한 칸씩 올라가기 O(h)
  4) 이진 상승 (Binary Lifting) - 오늘의 핵심
  5) 오일러 투어 + 희소 배열 - 질의 O(1)
  6) 타잔 오프라인 LCA (Union-Find)
  7) 응용: 거리, 가중치 경로 합, 경로의 k 번째 노드, 경로 판정
  8) 무작위 트리 교차 검증
  9) 체인 트리에서 "한 칸씩 vs 이진 상승" 실측

주의: cp949 콘솔 안전을 위해 출력에는 ASCII 기호만 사용한다.
"""

import random
import time
from collections import deque

SEP = "=" * 66
SUB = "-" * 66


# ==========================================================================
# 1) 루트 정하기 - BFS 로 parent / depth / 방문순서. 재귀 0줄 = 깊이 무제한
# ==========================================================================
def root_tree(adj, root=0):
    """무향 트리 adj 에 root 를 지정해 parent, depth, BFS 방문순서를 만든다.

    parent[root] = -1.
    order 는 BFS 순서이므로 "부모가 항상 자식보다 앞"이다.
    reversed(order) 로 순회하면 후위 순회와 같은 효과(자식이 먼저) - 트리 DP 에 유용.
    """
    n = len(adj)
    parent = [-1] * n
    depth = [0] * n
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


def children_of(parent, order):
    """parent 배열에서 children 리스트를 만든다 (order[0] 이 루트)."""
    children = [[] for _ in parent]
    for v in order[1:]:
        children[parent[v]].append(v)
    return children


# ==========================================================================
# 2) 나이브 LCA - 루트에서의 경로를 만들어 공통 접두사의 마지막을 취한다
#    질의당 O(N). 다른 구현을 검증할 때 쓰는 "정답 기준선".
# ==========================================================================
def path_to_root(parent, x):
    """루트 -> x 순서의 경로."""
    p = []
    while x != -1:
        p.append(x)
        x = parent[x]
    p.reverse()
    return p


def lca_naive(parent, u, v):
    pu, pv = path_to_root(parent, u), path_to_root(parent, v)
    res = -1
    for a, b in zip(pu, pv):
        if a != b:
            break
        res = a
    return res


# ==========================================================================
# 3) 한 칸씩 올라가기 - 질의당 O(h). 체인 트리에서는 O(N) 이 되어 위험하다.
# ==========================================================================
def lca_climb(parent, depth, u, v):
    while depth[u] > depth[v]:
        u = parent[u]
    while depth[v] > depth[u]:
        v = parent[v]
    while u != v:
        u, v = parent[u], parent[v]
    return u


# ==========================================================================
# 4) 이진 상승 (Binary Lifting) - 오늘의 핵심
#    up[k][v] = v 의 2^k 번째 조상.  up[k][v] = up[k-1][up[k-1][v]]
#    전처리 O(N log N), 질의 O(log N)
# ==========================================================================
class BinaryLiftingLCA:
    def __init__(self, adj, root=0):
        n = len(adj)
        self.n = n
        self.root = root
        self.parent, self.depth, self.order = root_tree(adj, root)
        # 2^LOG > n 을 보장. 고정값 20 을 쓰면 메모리 낭비 또는 부족이 생긴다.
        self.LOG = max(1, n.bit_length())
        up = [[-1] * n for _ in range(self.LOG)]
        up[0] = self.parent[:]                    # 기저: 1칸 위 = 직접 부모
        for k in range(1, self.LOG):
            prev, cur = up[k - 1], up[k]
            for v in range(n):
                mid = prev[v]
                cur[v] = prev[mid] if mid != -1 else -1
        self.up = up

    def kth_ancestor(self, v, k):
        """v 의 k 번째 조상. 범위를 벗어나면 -1. O(log k)"""
        up = self.up
        i = 0
        while k and v != -1:
            if k & 1:
                v = up[i][v]
            k >>= 1
            i += 1
        return v

    def lca(self, u, v):
        depth, up = self.depth, self.up
        # [1단계] 깊은 쪽(u)을 끌어올려 깊이를 맞춘다
        if depth[u] < depth[v]:
            u, v = v, u
        u = self.kth_ancestor(u, depth[u] - depth[v])
        if u == v:                    # v 가 u 의 조상이었다. 이 검사는 필수!
            return u
        # [2단계] 큰 점프부터, "다를 때만" 함께 올라간다
        for k in range(self.LOG - 1, -1, -1):
            if up[k][u] != up[k][v]:
                u, v = up[k][u], up[k][v]
        return up[0][u]               # u 가 아니라 부모. 지금 u,v 는 LCA 의 자식이다.

    def dist(self, u, v):
        """두 노드 사이 간선 수."""
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]

    def kth_on_path(self, u, v, k):
        """u 에서 v 로 가는 경로에서 u 로부터 k 번째 노드 (k=0 이면 u)."""
        L = self.lca(u, v)
        up_len = self.depth[u] - self.depth[L]
        down_len = self.depth[v] - self.depth[L]
        if k > up_len + down_len:
            return -1
        if k <= up_len:
            return self.kth_ancestor(u, k)
        return self.kth_ancestor(v, up_len + down_len - k)

    def on_path(self, u, v, w):
        """w 가 u-v 경로 위에 있는가? (삼각 등식)"""
        return self.dist(u, w) + self.dist(w, v) == self.dist(u, v)


# ==========================================================================
# 5) 오일러 투어 + 희소 배열 - 트리를 배열로 펼쳐 RMQ 로 환원. 질의 O(1)
# ==========================================================================
class EulerRMQLCA:
    def __init__(self, adj, root=0):
        n = len(adj)
        parent, depth, order = root_tree(adj, root)
        self.depth = depth
        children = children_of(parent, order)

        # 반복문 오일러 투어. 길이는 정확히 2N-1.
        euler = [root]
        first = [-1] * n
        first[root] = 0
        stack = [(root, 0)]                  # (노드, 다음에 볼 자식 인덱스)
        while stack:
            v, i = stack.pop()
            if i < len(children[v]):
                stack.append((v, i + 1))
                w = children[v][i]
                first[w] = len(euler)
                euler.append(w)
                stack.append((w, 0))
            elif stack:
                # 자식을 다 끝내고 부모로 돌아온다 -> 부모를 다시 기록 (핵심!)
                euler.append(stack[-1][0])
        self.euler, self.first = euler, first

        # 희소 배열: table[k][i] = 구간 [i, i+2^k) 에서 depth 가 최소인 euler 인덱스
        m = len(euler)
        LOG = max(1, m.bit_length())
        table = [list(range(m))]
        for k in range(1, LOG):
            span = 1 << k
            if span > m:
                break
            half = span >> 1
            prev = table[-1]
            row = [0] * (m - span + 1)
            for i in range(m - span + 1):
                a, b = prev[i], prev[i + half]
                row[i] = a if depth[euler[a]] <= depth[euler[b]] else b
            table.append(row)
        self.table = table

    def lca(self, u, v):
        l, r = self.first[u], self.first[v]
        if l > r:
            l, r = r, l
        k = (r - l + 1).bit_length() - 1
        a = self.table[k][l]
        b = self.table[k][r - (1 << k) + 1]     # 겹쳐도 된다: min 은 멱등(idempotent)
        e, d = self.euler, self.depth
        return e[a] if d[e[a]] <= d[e[b]] else e[b]


# ==========================================================================
# 6) 타잔 오프라인 LCA - Union-Find 로 한 번의 DFS 에 모든 질의를 답한다
#    전체 O((N+Q)*a(N)).  단, 질의를 미리 전부 알아야 한다(오프라인).
# ==========================================================================
def tarjan_offline_lca(adj, queries, root=0):
    n = len(adj)
    parent_uf = list(range(n))          # Union-Find 의 부모
    ancestor = list(range(n))           # 각 집합의 대표 조상
    visited = [False] * n

    qmap = [[] for _ in range(n)]
    for idx, (u, v) in enumerate(queries):
        qmap[u].append((v, idx))
        qmap[v].append((u, idx))
    ans = [-1] * len(queries)

    def find(x):
        while parent_uf[x] != x:
            parent_uf[x] = parent_uf[parent_uf[x]]      # 경로 압축 (반복문)
            x = parent_uf[x]
        return x

    tree_parent, _, order = root_tree(adj, root)
    children = children_of(tree_parent, order)

    stack = [(root, 0)]
    while stack:
        v, i = stack.pop()
        if i == 0:
            visited[v] = True
            ancestor[v] = v
        if i < len(children[v]):
            stack.append((v, i + 1))
            stack.append((children[v][i], 0))
        else:
            # v 의 서브트리 처리가 끝났다 -> v 의 질의를 확정한다
            for w, idx in qmap[v]:
                if ans[idx] == -1 and visited[w]:
                    ans[idx] = ancestor[find(w)]
            if stack:                              # 부모 집합으로 합친다
                p = stack[-1][0]
                parent_uf[v] = p
                ancestor[find(p)] = p
    return ans


# ==========================================================================
# 7) 가중치 트리의 경로 합 - 루트 기준 누적 합 + LCA (Day 14 의 트리 버전)
# ==========================================================================
def weighted_root_sums(wadj, root=0):
    """wadj[v] = [(이웃, 가중치), ...] 로부터 루트까지의 가중치 합 S[] 를 만든다."""
    n = len(wadj)
    S = [0] * n
    parent = [-1] * n
    visited = [False] * n
    visited[root] = True
    dq = deque([root])
    while dq:
        v = dq.popleft()
        for w, c in wadj[v]:
            if not visited[w]:
                visited[w] = True
                parent[w] = v
                S[w] = S[v] + c
                dq.append(w)
    return S, parent


def path_weight(S, lca_fn, u, v):
    """u-v 경로의 가중치 합 = S[u] + S[v] - 2*S[LCA]"""
    return S[u] + S[v] - 2 * S[lca_fn(u, v)]


# ==========================================================================
# 트리 생성 도우미
# ==========================================================================
def make_adj(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj


def random_tree(n, rng):
    """parent[i] = rng.randrange(i) 로 만들면 항상 유효한 트리다 (사이클 불가)."""
    edges = [(i, rng.randrange(i)) for i in range(1, n)]
    return make_adj(n, edges), edges


def chain_tree(n):
    """0 - 1 - 2 - ... - (n-1) 체인. h = n-1 로 최악의 트리."""
    return make_adj(n, [(i, i - 1) for i in range(1, n)])


# ==========================================================================
# 예제 실행
# ==========================================================================
def demo_basic():
    print(SEP)
    print("[1] 기본 예제 트리에서 네 가지 구현 비교 + 타잔")
    print(SEP)
    #              0
    #            /   \
    #           1     2
    #          / \     \
    #         3   4     5
    #            / \
    #           6   7
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (4, 6), (4, 7)]
    n = 8
    adj = make_adj(n, edges)
    parent, depth, order = root_tree(adj, 0)

    print("트리 구조 (루트 0):")
    print("               0")
    print("             /   \\")
    print("            1     2")
    print("           / \\     \\")
    print("          3   4     5")
    print("             / \\")
    print("            6   7")
    print()
    print("parent =", parent)
    print("depth  =", depth)
    print("BFS 순서 =", order)
    print()

    bl = BinaryLiftingLCA(adj, 0)
    er = EulerRMQLCA(adj, 0)

    print("오일러 투어 (길이 = 2N-1 =", 2 * n - 1, "):")
    print("  euler =", er.euler)
    print("  len   =", len(er.euler))
    print("  first =", er.first)
    print()

    pairs = [(6, 7), (3, 7), (3, 5), (4, 7), (2, 2), (0, 5)]
    print("쌍       나이브  한칸씩  이진상승  오일러+RMQ")
    for u, v in pairs:
        a = lca_naive(parent, u, v)
        b = lca_climb(parent, depth, u, v)
        c = bl.lca(u, v)
        d = er.lca(u, v)
        assert a == b == c == d, (u, v, a, b, c, d)
        print("({}, {})  {:>6} {:>7} {:>9} {:>11}".format(u, v, a, b, c, d))
    print()
    print("네 구현이 모두 일치한다 (assert 통과)")

    print()
    print("타잔 오프라인 LCA (질의를 미리 다 아는 경우):")
    tj = tarjan_offline_lca(adj, pairs, 0)
    print("  질의:", pairs)
    print("  결과:", tj)
    assert tj == [lca_naive(parent, u, v) for u, v in pairs]
    print("  나이브와 일치 (assert 통과)")
    print()


def demo_binary_lifting_table():
    print(SEP)
    print("[2] 이진 상승 표를 눈으로 보기 - 체인 트리 0-1-2-...-7")
    print(SEP)
    adj = chain_tree(8)
    bl = BinaryLiftingLCA(adj, 0)
    print("LOG =", bl.LOG, "  (2^LOG > n = 8 이어야 한다)")
    print()
    for k in range(bl.LOG):
        print("up[{}] (= {}칸 위 조상): {}".format(k, 1 << k, bl.up[k]))
    print()
    print("노드 7 에서 k 칸 위 조상:")
    for k in range(9):
        print("  k = {} -> {}".format(k, bl.kth_ancestor(7, k)))
    print()
    print("5 = 4 + 1 = 2^2 + 2^0  ->  점프 2번으로 끝난다 (한 칸씩 5번 대신)")
    print()


def demo_applications():
    print(SEP)
    print("[3] LCA 응용 - 거리 / 경로의 k 번째 노드 / 경로 판정 / 가중치 경로 합")
    print(SEP)
    #        0
    #      / | \
    #     1  2  3
    #    /|     |
    #   4 5     6
    #   |
    #   7
    edges = [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (3, 6), (4, 7)]
    n = 8
    adj = make_adj(n, edges)
    bl = BinaryLiftingLCA(adj, 0)

    print("dist(u, v) = depth[u] + depth[v] - 2*depth[LCA]")
    for u, v in [(7, 5), (7, 6), (2, 2), (0, 7)]:
        L = bl.lca(u, v)
        print("  dist({}, {}) = {}   (LCA = {})".format(u, v, bl.dist(u, v), L))
    print()

    print("경로 7 -> 6 의 노드를 순서대로 (kth_on_path):")
    total = bl.dist(7, 6)
    path = [bl.kth_on_path(7, 6, k) for k in range(total + 1)]
    print("  ", path, "  (간선 {}개)".format(total))
    print()

    print("w 가 7-6 경로 위에 있는가? (삼각 등식 dist(u,w)+dist(w,v)==dist(u,v))")
    for w in range(n):
        mark = "YES" if bl.on_path(7, 6, w) else "no "
        print("  w = {} -> {}".format(w, mark))
    print()

    print("가중치 트리의 경로 합: path = S[u] + S[v] - 2*S[LCA]")
    wedges = [(0, 1, 5), (0, 2, 3), (0, 3, 8), (1, 4, 2), (1, 5, 7), (3, 6, 1), (4, 7, 4)]
    wadj = [[] for _ in range(n)]
    for a, b, c in wedges:
        wadj[a].append((b, c))
        wadj[b].append((a, c))
    S, _ = weighted_root_sums(wadj, 0)
    print("  S (루트까지 가중치 합) =", S)
    for u, v in [(7, 5), (7, 6), (5, 2)]:
        print("  path_weight({}, {}) = {}".format(u, v, path_weight(S, bl.lca, u, v)))
    print()
    # 경로를 직접 따라 더한 값과 대조한다
    w = {}
    for a, b, c in wedges:
        w[(a, b)] = w[(b, a)] = c
    for u, v in [(7, 5), (7, 6), (5, 2)]:
        nodes = [bl.kth_on_path(u, v, k) for k in range(bl.dist(u, v) + 1)]
        brute = sum(w[(nodes[i], nodes[i + 1])] for i in range(len(nodes) - 1))
        assert brute == path_weight(S, bl.lca, u, v), (u, v, brute)
    print("경로를 직접 더한 값과 공식이 일치한다 (assert 통과)")
    print()


def demo_cross_validation():
    print(SEP)
    print("[4] 무작위 트리 교차 검증 - 나이브 vs 한칸씩 vs 이진상승 vs 오일러 vs 타잔")
    print(SEP)
    rng = random.Random(43)
    total_pairs = 0
    for _ in range(30):
        n = rng.randint(1, 40)
        adj, _ = random_tree(n, rng)
        parent, depth, _ = root_tree(adj, 0)
        bl = BinaryLiftingLCA(adj, 0)
        er = EulerRMQLCA(adj, 0)
        pairs = [(u, v) for u in range(n) for v in range(n)]
        expect = [lca_naive(parent, u, v) for u, v in pairs]
        tj = tarjan_offline_lca(adj, pairs, 0)
        for (u, v), e in zip(pairs, expect):
            assert lca_climb(parent, depth, u, v) == e, ("climb", n, u, v)
            assert bl.lca(u, v) == e, ("lifting", n, u, v)
            assert er.lca(u, v) == e, ("euler", n, u, v)
        assert tj == expect, ("tarjan", n)
        assert len(er.euler) == 2 * n - 1, ("euler len", n, len(er.euler))
        total_pairs += len(pairs)
    print("무작위 트리 30개 x 모든 노드 쌍 = {}개 질의".format(total_pairs))
    print("다섯 구현이 전부 일치했다. 오일러 투어 길이도 매번 2N-1 이었다.")
    print()

    print("경계 케이스 점검:")
    adj1 = make_adj(1, [])
    bl1 = BinaryLiftingLCA(adj1, 0)
    print("  노드 1개 트리: lca(0,0) =", bl1.lca(0, 0), " dist =", bl1.dist(0, 0))
    adj2 = make_adj(2, [(0, 1)])
    bl2 = BinaryLiftingLCA(adj2, 0)
    print("  노드 2개 트리: lca(0,1) =", bl2.lca(0, 1), " lca(1,1) =", bl2.lca(1, 1))
    print("  (조상 관계에서는 조상 자신이 답이다 - 자기 자신도 조상으로 센다)")
    print()


def demo_benchmark():
    print(SEP)
    print("[5] 실측 - 체인 트리(최악)에서 '한 칸씩' vs '이진 상승'")
    print(SEP)
    n = 20000
    q = 2000
    adj = chain_tree(n)
    parent, depth, _ = root_tree(adj, 0)

    rng = random.Random(1234)
    pairs = [(rng.randrange(n), rng.randrange(n)) for _ in range(q)]

    t0 = time.perf_counter()
    bl = BinaryLiftingLCA(adj, 0)
    t_build = time.perf_counter() - t0

    t0 = time.perf_counter()
    r1 = [lca_climb(parent, depth, u, v) for u, v in pairs]
    t_climb = time.perf_counter() - t0

    t0 = time.perf_counter()
    r2 = [bl.lca(u, v) for u, v in pairs]
    t_lift = time.perf_counter() - t0

    assert r1 == r2
    print("체인 트리 N = {}, 질의 Q = {}  (h = N-1 = {})".format(n, q, n - 1))
    print()
    print("  이진 상승 전처리      : {:.4f} s   (LOG = {})".format(t_build, bl.LOG))
    print("  한 칸씩 올라가기 질의 : {:.4f} s".format(t_climb))
    print("  이진 상승 질의        : {:.4f} s".format(t_lift))
    if t_lift > 0:
        print("  질의 속도 비 (한칸씩 / 이진상승) : 약 {:.1f} 배".format(t_climb / t_lift))
    print()
    print("전처리를 포함해도 이진 상승이 압도적이다.")
    print("N = 10^5, Q = 10^5 라면 한 칸씩은 10^10 연산으로 아예 불가능하다.")
    print()

    print(SUB)
    print("균형 트리에서는? (완전 이진 트리, h ~ log N)")
    m = 20000
    bal_edges = [(i, (i - 1) // 2) for i in range(1, m)]
    bal = make_adj(m, bal_edges)
    bparent, bdepth, _ = root_tree(bal, 0)
    bbl = BinaryLiftingLCA(bal, 0)
    bpairs = [(rng.randrange(m), rng.randrange(m)) for _ in range(q)]

    t0 = time.perf_counter()
    b1 = [lca_climb(bparent, bdepth, u, v) for u, v in bpairs]
    tb_climb = time.perf_counter() - t0
    t0 = time.perf_counter()
    b2 = [bbl.lca(u, v) for u, v in bpairs]
    tb_lift = time.perf_counter() - t0
    assert b1 == b2
    print("  완전 이진 트리 N = {} (최대 깊이 {})".format(m, max(bdepth)))
    print("  한 칸씩   : {:.4f} s".format(tb_climb))
    print("  이진 상승 : {:.4f} s".format(tb_lift))
    print()
    print("균형 트리에서는 차이가 거의 없거나 오히려 한 칸씩이 빠를 수 있다.")
    print("이진 상승이 필요한 이유는 '평균'이 아니라 '최악(체인)' 때문이다.")
    print("코딩테스트는 최악 입력을 반드시 넣는다.")
    print()


def demo_recursion_limit():
    print(SEP)
    print("[6] 파이썬 재귀 깊이 - 오늘의 최대 실전 함정")
    print(SEP)
    import sys
    print("기본 재귀 한도 sys.getrecursionlimit() =", sys.getrecursionlimit())
    print()

    n = 3000
    adj = chain_tree(n)

    def rec_depth(v, p, d, out):
        out[v] = d
        for w in adj[v]:
            if w != p:
                rec_depth(w, v, d + 1, out)

    out = [0] * n
    try:
        rec_depth(0, -1, 0, out)
        print("재귀 DFS 성공 (n = {})".format(n))
    except RecursionError:
        print("재귀 DFS 실패: RecursionError (n = {} 체인)".format(n))
        print("  -> 노드가 10^5 인 체인 트리에서는 확정적으로 죽는다")
    print()

    parent, depth, order = root_tree(adj, 0)
    print("BFS 방식은 문제없이 성공했다. depth[n-1] =", depth[n - 1])
    print()
    print("트리 DP 도 재귀 없이 된다: reversed(BFS 순서) 로 순회하면")
    print("자식이 부모보다 먼저 처리되므로 후위 순회와 같은 효과다.")
    subtree = [1] * n
    for v in reversed(order):
        if parent[v] != -1:
            subtree[parent[v]] += subtree[v]
    print("  서브트리 크기 subtree[0] =", subtree[0], "(= n =", n, ")")
    print("  subtree[n//2] =", subtree[n // 2], "(체인이므로 n - n//2 =", n - n // 2, ")")
    assert subtree[0] == n and subtree[n // 2] == n - n // 2
    print("  assert 통과. 재귀 0줄로 트리 DP 완료.")
    print()


def demo_summary():
    print(SEP)
    print("[7] 오늘의 판단 기준")
    print(SEP)
    rows = [
        ("질의 1회, 이진 트리 객체", "후위 순회 재귀 6줄 (#236)"),
        ("질의 1회, BST", "값 비교로 한 방향 O(h) (#235)"),
        ("질의 몇 번, 트리 작음", "parent/depth 만들고 한 칸씩 O(h)"),
        ("질의 많음 (N,Q <= 10^5)", "이진 상승 O(N log N) + O(log N)"),
        ("k 번째 조상 질의", "이진 상승 표 그대로 (#1483)"),
        ("질의가 극단적으로 많음", "오일러 투어 + 희소 배열 -> O(1)"),
        ("갱신이 섞임", "오일러 투어 + 세그먼트 트리 (Day 40)"),
        ("질의를 미리 다 안다", "타잔 오프라인 + Union-Find (Day 36)"),
        ("트리가 아닌 일반 그래프", "분기점 전수 조사 + 플로이드 (Day 35)"),
        ("파이썬에서 트리가 깊다", "BFS + reversed(order). 재귀 금지"),
    ]
    for a, b in rows:
        print("  {:<26} -> {}".format(a, b))
    print()
    print("한 줄 요약: 트리의 모든 경로는 LCA 에서 꺾인다.")
    print("           그래서 LCA 는 트리 경로 문제의 좌표계다.")
    print(SEP)


if __name__ == "__main__":
    demo_basic()
    demo_binary_lifting_table()
    demo_applications()
    demo_cross_validation()
    demo_benchmark()
    demo_recursion_limit()
    demo_summary()
