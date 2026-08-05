"""Day 43 해설 - 최소 공통 조상 (LCA: Lowest Common Ancestor)

실행:  PYTHONIOENCODING=cp949 python solutions.py

문제 목록 (출처: 프로그래머스 / LeetCode 만)
  1) LeetCode #235  Lowest Common Ancestor of a BST                     기초
  2) LeetCode #236  Lowest Common Ancestor of a Binary Tree             중급
  3) LeetCode #1123 Lowest Common Ancestor of Deepest Leaves            중급
  4) 프로그래머스 #72413  합승 택시 요금 (2021 카카오 블라인드)          기출
  5) LeetCode #2096 Step-By-Step Directions From a Binary Tree Node...  심화
  6) LeetCode #1483 Kth Ancestor of a Tree Node                         심화

각 문제는 플랫폼 시그니처를 그대로 쓰고, 가능한 곳은 다중 접근 + 교차 검증을 붙였다.
주의: cp949 콘솔 안전을 위해 출력에는 ASCII 기호만 사용한다.
"""

import heapq
import random
from collections import deque

SEP = "=" * 66


# ==========================================================================
# 공통: LeetCode 스타일 이진 트리
# ==========================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return "TreeNode({})".format(self.val)


def build_tree(vals):
    """LeetCode 레벨 순서 리스트([3,5,1,6,2,0,8,None,None,7,4]) -> 트리."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    dq = deque([root])
    i = 1
    while dq and i < len(vals):
        node = dq.popleft()
        if i < len(vals):
            v = vals[i]
            i += 1
            if v is not None:
                node.left = TreeNode(v)
                dq.append(node.left)
        if i < len(vals):
            v = vals[i]
            i += 1
            if v is not None:
                node.right = TreeNode(v)
                dq.append(node.right)
    return root


def find_node(root, val):
    """값으로 노드 객체를 찾는다 (테스트용). 반복문 BFS 라 깊이 제한 없음."""
    dq = deque([root])
    while dq:
        node = dq.popleft()
        if node.val == val:
            return node
        if node.left:
            dq.append(node.left)
        if node.right:
            dq.append(node.right)
    return None


# ==========================================================================
# 1) LeetCode #235 - Lowest Common Ancestor of a BST            [기초]
#    https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
#
#    BST 의 정렬 성질로 한 방향만 내려간다. O(h) 시간, O(1) 공간.
# ==========================================================================
class Solution235:
    def lowestCommonAncestor(self, root, p, q):
        """[접근 1] 반복문 값 비교. O(h) 시간, O(1) 공간. 이것이 정답."""
        cur = root
        while cur:
            if p.val < cur.val and q.val < cur.val:
                cur = cur.left               # 둘 다 왼쪽
            elif p.val > cur.val and q.val > cur.val:
                cur = cur.right              # 둘 다 오른쪽
            else:
                return cur                   # 갈라지거나, cur 가 p/q 자신 -> 여기가 LCA
        return None

    def lca_range(self, root, p, q):
        """[접근 2] 구간 [lo, hi] 에 처음 들어오는 노드가 LCA. 같은 알고리즘의 다른 표현."""
        lo, hi = min(p.val, q.val), max(p.val, q.val)
        cur = root
        while not (lo <= cur.val <= hi):
            cur = cur.left if cur.val > hi else cur.right
        return cur

    def lca_recursive(self, root, p, q):
        """[접근 3] 재귀 버전. 치우친 BST(h=10^5)에서는 RecursionError 위험."""
        if p.val < root.val and q.val < root.val:
            return self.lca_recursive(root.left, p, q)
        if p.val > root.val and q.val > root.val:
            return self.lca_recursive(root.right, p, q)
        return root


def test_235():
    print(SEP)
    print("[1] LeetCode #235 - Lowest Common Ancestor of a BST")
    print(SEP)
    #          6
    #        /   \
    #       2     8
    #      / \   / \
    #     0   4 7   9
    #        / \
    #       3   5
    root = build_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    sol = Solution235()

    cases = [
        (2, 8, 6),      # 루트에서 갈라진다
        (2, 4, 2),      # 2 가 4 의 조상 -> 자기 자신도 조상으로 센다!
        (3, 5, 4),
        (0, 5, 2),
        (7, 9, 8),
        (0, 9, 6),
    ]
    for pv, qv, expect in cases:
        p, q = find_node(root, pv), find_node(root, qv)
        a = sol.lowestCommonAncestor(root, p, q).val
        b = sol.lca_range(root, p, q).val
        c = sol.lca_recursive(root, p, q).val
        assert a == b == c == expect, (pv, qv, a, b, c, expect)
        print("  LCA({}, {}) = {}   (반복 / 구간 / 재귀 세 접근 일치)".format(pv, qv, a))

    print()
    print("  핵심: p=2, q=4 의 답이 6 이 아니라 2 다.")
    print("        '노드는 자기 자신의 자손' 이라는 관례를 놓치면 여기서 틀린다.")
    print("  통과: 모든 assert OK")
    print()


# ==========================================================================
# 2) LeetCode #236 - Lowest Common Ancestor of a Binary Tree     [중급]
#    https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
#
#    후위 순회로 "양쪽에서 신호가 오면 내가 답". O(N).
# ==========================================================================
class Solution236:
    def lowestCommonAncestor(self, root, p, q):
        """[접근 1] 후위 순회 재귀 6줄. O(N) 시간, O(h) 스택."""
        if root is None or root is p or root is q:
            return root                      # 찾았으면 나를 올려보낸다
        L = self.lowestCommonAncestor(root.left, p, q)
        R = self.lowestCommonAncestor(root.right, p, q)
        if L and R:
            return root                      # 양쪽에서 왔다 -> 내가 갈라지는 지점
        return L or R                        # 한쪽만 -> 그대로 전달

    def lca_iterative(self, root, p, q):
        """[접근 2] parent 맵 + 조상 집합. 재귀 0줄이라 깊은 트리에서도 안전. O(N)."""
        parent = {root: None}
        stack = [root]
        while p not in parent or q not in parent:
            node = stack.pop()
            if node.left:
                parent[node.left] = node
                stack.append(node.left)
            if node.right:
                parent[node.right] = node
                stack.append(node.right)
        ancestors = set()
        n = p
        while n is not None:                 # p 의 조상을 전부 담는다 (자기 자신 포함)
            ancestors.add(n)
            n = parent[n]
        n = q
        while n not in ancestors:            # q 에서 올라가며 처음 만나는 조상
            n = parent[n]
        return n


def test_236():
    print(SEP)
    print("[2] LeetCode #236 - Lowest Common Ancestor of a Binary Tree")
    print(SEP)
    #          3
    #        /   \
    #       5     1
    #      / \   / \
    #     6   2 0   8
    #        / \
    #       7   4
    root = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    sol = Solution236()

    cases = [(5, 1, 3), (5, 4, 5), (7, 4, 2), (6, 4, 5), (7, 8, 3), (0, 8, 1)]
    for pv, qv, expect in cases:
        p, q = find_node(root, pv), find_node(root, qv)
        a = sol.lowestCommonAncestor(root, p, q).val
        b = sol.lca_iterative(root, p, q).val
        assert a == b == expect, (pv, qv, a, b, expect)
        print("  LCA({}, {}) = {}   (재귀 / 반복 두 접근 일치)".format(pv, qv, a))

    print()
    print("  핵심: p=5, q=4 의 답은 5 다 (5 가 4 의 조상).")
    print("  주의: 이 6줄은 'p 와 q 가 둘 다 존재' 를 가정한다.")
    print("        하나만 있으면 있는 쪽을 반환해 조용히 틀린다 (LCA II 변형).")
    print("  통과: 모든 assert OK")
    print()


# ==========================================================================
# 3) LeetCode #1123 - Lowest Common Ancestor of Deepest Leaves   [중급]
#    https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/
#
#    (서브트리 높이, 그 안 최심 잎들의 LCA) 를 한 번에 올려보낸다.
# ==========================================================================
class Solution1123:
    def lcaDeepestLeaves(self, root):
        """[접근 1] 1-pass 트리 DP. (높이, LCA) 튜플을 동시에 반환. O(N)."""
        def dfs(node):
            if not node:
                return 0, None               # (높이, LCA)
            hl, al = dfs(node.left)
            hr, ar = dfs(node.right)
            if hl == hr:
                return hl + 1, node          # 양쪽 높이가 같다 -> 내가 갈라지는 지점
            if hl > hr:
                return hl + 1, al            # 왼쪽이 깊다 -> 왼쪽 답을 그대로 올린다
            return hr + 1, ar

        return dfs(root)[1]

    def lca_2pass(self, root):
        """[접근 2] 최대 깊이를 먼저 구하고 내려가며 판정. 재귀 0줄. O(N)."""
        if root is None:
            return None
        # (a) BFS 로 부모 / 깊이 / 방문 순서
        order, parent, depth = [root], {root: None}, {root: 0}
        i = 0
        while i < len(order):
            node = order[i]
            i += 1
            for ch in (node.left, node.right):
                if ch:
                    parent[ch] = node
                    depth[ch] = depth[node] + 1
                    order.append(ch)
        D = max(depth.values())

        # (b) reversed(BFS 순서) 로 서브트리 최대 깊이 md 를 올린다 (후위 순회 효과)
        md = {node: depth[node] for node in order}
        for node in reversed(order):
            p = parent[node]
            if p is not None and md[node] > md[p]:
                md[p] = md[node]

        # (c) 루트에서 내려가며 "양쪽 다 최심을 품으면 여기가 답"
        cur = root
        while True:
            lok = cur.left is not None and md[cur.left] == D
            rok = cur.right is not None and md[cur.right] == D
            if lok and rok:
                return cur
            if lok:
                cur = cur.left
            elif rok:
                cur = cur.right
            else:
                return cur


def test_1123():
    print(SEP)
    print("[3] LeetCode #1123 - Lowest Common Ancestor of Deepest Leaves")
    print(SEP)
    sol = Solution1123()
    cases = [
        ([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 2),   # 최심 잎 7, 4 -> LCA = 2
        ([1], 1),                                        # 노드 하나 -> 자기 자신
        ([0, 1, 3, None, 2], 2),                         # 최심 잎이 2 하나뿐
        ([1, 2, 3, 4, 5], 2),                            # 최심 잎 4,5 -> LCA = 2 (3 은 얕다)
    ]
    for vals, expect in cases:
        root = build_tree(vals)
        a = sol.lcaDeepestLeaves(root).val
        b = sol.lca_2pass(root).val
        assert a == b == expect, (vals, a, b, expect)
        print("  {} -> LCA = {}   (1-pass / 2-pass 일치)".format(vals, a))

    print()
    print("  핵심: '왼쪽 높이 == 오른쪽 높이' 인 가장 깊은 노드가 답이다.")
    print("        같으면 자신을, 다르면 깊은 쪽 답을 그대로 올려보낸다.")
    print("  참고: LeetCode #865 (Smallest Subtree with all the Deepest Nodes) 와 같은 문제.")
    print("  통과: 모든 assert OK")
    print()


# ==========================================================================
# 4) 프로그래머스 #72413 - 합승 택시 요금 (2021 카카오 블라인드)   [기출]
#    https://school.programmers.co.kr/learn/courses/30/lessons/72413
#
#    "함께 가다가 갈라지는 지점 c" 를 전수 조사한다 = 일반 그래프에서의 LCA 사고.
#    답 = min over c of  d[s][c] + d[c][a] + d[c][b]
#    c = s 로 두면 "합승 안 함" 이 자동으로 포함된다.
# ==========================================================================
def solution(n, s, a, b, fares):
    """[접근 1] 플로이드-워셜로 모든 쌍 최단 거리. O(n^3). n <= 200 이라 충분."""
    INF = float('inf')
    d = [[INF] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][i] = 0                                  # 이 초기화를 빼먹으면 c=s 케이스를 놓친다
    for c, e, f in fares:
        if f < d[c][e]:                              # 중복 간선 대비
            d[c][e] = d[e][c] = f                    # 양방향!

    for k in range(1, n + 1):                        # 경유지 k 가 가장 바깥 루프!
        dk = d[k]
        for i in range(1, n + 1):
            di = d[i]
            dik = di[k]
            if dik == INF:
                continue
            for j in range(1, n + 1):
                nd = dik + dk[j]
                if nd < di[j]:
                    di[j] = nd

    return min(d[s][c] + d[c][a] + d[c][b] for c in range(1, n + 1))


def solution_dijkstra(n, s, a, b, fares):
    """[접근 2] 다익스트라 3회. 필요한 것은 s, a, b 에서의 거리 세 줄뿐이다.

    O(3 * E log V) 로 플로이드보다 훨씬 빠르다. n 이 커지면 이쪽만 살아남는다.
    """
    INF = float('inf')
    graph = [[] for _ in range(n + 1)]
    for c, e, f in fares:
        graph[c].append((e, f))
        graph[e].append((c, f))                      # 양방향

    def dijkstra(src):
        dist = [INF] * (n + 1)
        dist[src] = 0
        pq = [(0, src)]
        while pq:
            cost, v = heapq.heappop(pq)
            if cost > dist[v]:
                continue
            for w, f in graph[v]:
                nd = cost + f
                if nd < dist[w]:
                    dist[w] = nd
                    heapq.heappush(pq, (nd, w))
        return dist

    ds, da, db = dijkstra(s), dijkstra(a), dijkstra(b)
    # 무향 그래프이므로 da[c] == d[c][a] 다
    return min(ds[c] + da[c] + db[c] for c in range(1, n + 1))


def test_72413():
    print(SEP)
    print("[4] 프로그래머스 #72413 - 합승 택시 요금 (2021 카카오 블라인드)")
    print(SEP)
    cases = [
        (6, 4, 6, 2,
         [[4, 1, 10], [3, 5, 24], [5, 6, 2], [3, 1, 41], [5, 1, 24],
          [4, 6, 50], [2, 4, 66], [2, 3, 22], [1, 6, 25]], 82),
        (7, 3, 4, 1,
         [[5, 7, 9], [4, 6, 4], [3, 6, 1], [3, 2, 3], [2, 1, 6]], 14),
        (6, 4, 5, 6,
         [[2, 6, 6], [6, 3, 7], [4, 6, 7], [6, 5, 11], [2, 5, 12],
          [5, 3, 20], [2, 4, 8]], 18),
    ]
    for n, s, a, b, fares, expect in cases:
        r1 = solution(n, s, a, b, fares)
        r2 = solution_dijkstra(n, s, a, b, fares)
        assert r1 == r2 == expect, (n, s, a, b, r1, r2, expect)
        print("  n={} s={} a={} b={} -> {}   (플로이드 / 다익스트라 일치)".format(
            n, s, a, b, r1))

    print()
    print("  핵심: 분기점 c 를 모든 지점에 대해 전수 조사한다.")
    print("        d[s][c] + d[c][a] + d[c][b] 의 최솟값.")
    print("        트리라면 c = LCA(a,b) 로 즉시 정해지지만, 일반 그래프라 전수 조사한다.")
    print("  주의: c = s 가 '합승 안 함' 을 자동으로 커버한다 (d[s][s] = 0).")
    print("  통과: 모든 assert OK")
    print()


# ==========================================================================
# 5) LeetCode #2096 - Step-By-Step Directions ...                [심화]
#    https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/
#
#    루트에서 두 노드까지의 경로 문자열을 만들고 공통 접두사를 잘라낸다.
#    "공통 접두사를 자르는 것 = LCA 를 지나치는 것"
# ==========================================================================
class Solution2096:
    def getDirections(self, root, startValue, destValue):
        """[접근 1] 루트 경로 두 개 + 공통 접두사 제거. O(N).

        parent/dir 맵을 한 번의 순회로 만들고 대상에서 거슬러 올라간다.
        문자열 += 누적을 피해 O(N) 을 보장한다.
        """
        par = {}                                    # val -> (부모 val, 'L' 또는 'R')
        stack = [root]
        while stack:
            node = stack.pop()
            if node.left:
                par[node.left.val] = (node.val, 'L')
                stack.append(node.left)
            if node.right:
                par[node.right.val] = (node.val, 'R')
                stack.append(node.right)

        def root_path(val):
            """루트 -> val 의 방향 문자열."""
            out = []
            while val in par:
                p, c = par[val]
                out.append(c)
                val = p
            out.reverse()
            return ''.join(out)

        ps, pd = root_path(startValue), root_path(destValue)
        i = 0
        while i < len(ps) and i < len(pd) and ps[i] == pd[i]:
            i += 1                                  # 공통 접두사 = 루트에서 LCA 까지
        return 'U' * (len(ps) - i) + pd[i:]

    def getDirections_lca(self, root, startValue, destValue):
        """[접근 2] LCA 를 명시적으로 찾아 조립한다. O(N)."""
        par = {}
        stack = [root]
        while stack:
            node = stack.pop()
            if node.left:
                par[node.left.val] = (node.val, 'L')
                stack.append(node.left)
            if node.right:
                par[node.right.val] = (node.val, 'R')
                stack.append(node.right)

        # start 의 조상들과 "start 로부터의 거리"
        anc = {}
        v, d = startValue, 0
        while True:
            anc[v] = d
            if v not in par:
                break
            v = par[v][0]
            d += 1

        # dest 에서 올라가며 처음 만나는 start 의 조상이 LCA
        downs = []
        v = destValue
        while v not in anc:
            p, c = par[v]
            downs.append(c)
            v = p
        downs.reverse()
        return 'U' * anc[v] + ''.join(downs)        # anc[v] = start 에서 LCA 까지 거리


def test_2096():
    print(SEP)
    print("[5] LeetCode #2096 - Step-By-Step Directions From a Binary Tree Node")
    print(SEP)
    sol = Solution2096()
    cases = [
        ([5, 1, 2, 3, None, 6, 4], 3, 6, "UURL"),
        ([2, 1], 2, 1, "L"),
        ([5, 1, 2, 3, None, 6, 4], 6, 3, "UULL"),   # 역방향: 6 -> 5 는 U 두 번
        ([5, 1, 2, 3, None, 6, 4], 3, 4, "UURR"),
        ([5, 1, 2, 3, None, 6, 4], 5, 3, "LL"),
    ]
    for vals, sv, dv, expect in cases:
        root = build_tree(vals)
        a = sol.getDirections(root, sv, dv)
        b = sol.getDirections_lca(root, sv, dv)
        assert a == b == expect, (vals, sv, dv, a, b, expect)
        print("  start={} dest={} -> '{}'   (접두사 / 명시적 LCA 일치)".format(sv, dv, a))

    print()
    print("  핵심: ps = 'LL'(5->1->3), pd = 'RL'(5->2->6)")
    print("        공통 접두사 없음 -> LCA = 루트 5")
    print("        'U' x len(ps) + pd = 'UU' + 'RL' = 'UURL'")
    print("  주의: 항상 먼저 올라가고(U) 그다음 내려간다. 트리 경로는 U 자 모양이다.")
    print("  통과: 모든 assert OK")
    print()


# ==========================================================================
# 6) LeetCode #1483 - Kth Ancestor of a Tree Node                [심화]
#    https://leetcode.com/problems/kth-ancestor-of-a-tree-node/
#
#    이진 상승. up[j][v] = v 의 2^j 번째 조상.
#    전처리 O(n log n), 질의 O(log k).
# ==========================================================================
class TreeAncestor:
    """[접근 1] -1 을 명시적으로 검사하는 버전."""

    def __init__(self, n, parent):
        self.n = n
        self.LOG = max(1, n.bit_length())        # 2^LOG > n. 고정값 20 금지!
        up = [[-1] * n for _ in range(self.LOG)]
        up[0] = parent[:]                        # 복사! 원본 오염 방지
        for j in range(1, self.LOG):
            prev, cur = up[j - 1], up[j]
            for v in range(n):
                mid = prev[v]
                cur[v] = prev[mid] if mid != -1 else -1
        self.up = up

    def getKthAncestor(self, node, k):
        up = self.up
        if k >= (1 << self.LOG):                 # 표가 감당하는 최대 점프를 넘는다
            return -1                            # (트리 높이 < 2^LOG 이므로 반드시 범위 밖)
        j = 0
        while k and node != -1:                  # node != -1 검사가 필수!
            if k & 1:                            # 이 비트가 켜졌으면 2^j 점프
                node = up[j][node]
            k >>= 1
            j += 1
        return node


class TreeAncestorSentinel:
    """[접근 2] 가상 노드 n 을 루트의 부모로 두는 버전 (자기 루프).

    경계 검사가 사라져 코드가 깔끔하고, 파이썬 음수 인덱싱 버그가 원천 봉쇄된다.
    """

    def __init__(self, n, parent):
        self.n = n
        m = n + 1                                # 가상 노드 n 추가
        self.LOG = max(1, m.bit_length())
        up = [[n] * m for _ in range(self.LOG)]
        base = up[0]
        for v in range(n):
            base[v] = parent[v] if parent[v] != -1 else n    # 루트의 부모 = 가상 노드
        base[n] = n                              # 가상 노드는 자기 자신을 가리킨다
        for j in range(1, self.LOG):
            prev, cur = up[j - 1], up[j]
            for v in range(m):
                cur[v] = prev[prev[v]]           # 검사 한 줄도 없다
        self.up = up

    def getKthAncestor(self, node, k):
        up, n = self.up, self.n
        if k >= (1 << self.LOG):                 # 표가 감당하는 최대 점프를 넘는다
            return -1
        j = 0
        while k:
            if k & 1:
                node = up[j][node]               # 가상 노드에 닿으면 계속 가상 노드
            k >>= 1
            j += 1
        return -1 if node == n else node


def kth_ancestor_naive(parent, node, k):
    """[검증용] 한 칸씩 k 번 올라간다. O(k)."""
    for _ in range(k):
        if node == -1:
            return -1
        node = parent[node]
    return node


def test_1483():
    print(SEP)
    print("[6] LeetCode #1483 - Kth Ancestor of a Tree Node")
    print(SEP)
    #      0
    #     / \
    #    1   2
    #   /
    #  3
    #  |
    #  4
    parent = [-1, 0, 0, 1, 3]
    n = 5
    ta = TreeAncestor(n, parent)
    ts = TreeAncestorSentinel(n, parent)

    print("  parent =", parent, "  (LOG = {})".format(ta.LOG))
    for j in range(ta.LOG):
        print("  up[{}] (= {}칸 위): {}".format(j, 1 << j, ta.up[j]))
    print()

    cases = [(3, 1, 1), (4, 2, 1), (4, 3, 0), (4, 4, -1), (0, 1, -1), (2, 1, 0)]
    for node, k, expect in cases:
        a = ta.getKthAncestor(node, k)
        b = ts.getKthAncestor(node, k)
        c = kth_ancestor_naive(parent, node, k)
        assert a == b == c == expect, (node, k, a, b, c, expect)
        print("  getKthAncestor({}, {}) = {}   (이진상승 / 가상노드 / 나이브 일치)".format(
            node, k, a))

    print()
    print("  교차 검증: 무작위 트리 x 모든 (node, k) 조합")
    rng = random.Random(1483)
    total = 0
    for _ in range(40):
        m = rng.randint(1, 60)
        par = [-1] + [rng.randrange(i) for i in range(1, m)]
        A = TreeAncestor(m, par)
        S = TreeAncestorSentinel(m, par)
        for node in range(m):
            for k in range(1, m + 2):
                e = kth_ancestor_naive(par, node, k)
                assert A.getKthAncestor(node, k) == e, ("lifting", m, node, k)
                assert S.getKthAncestor(node, k) == e, ("sentinel", m, node, k)
                total += 1
    print("  무작위 트리 40개, 총 {}개 질의가 모두 나이브와 일치했다.".format(total))
    print()
    print("  주의: node != -1 검사를 빼면 파이썬 음수 인덱싱으로")
    print("        에러 없이 '조용히 틀린 값' 이 나온다. 이 문제 최다 버그다.")
    print("  통과: 모든 assert OK")
    print()


# ==========================================================================
# 보너스: 이진 상승 표로 LCA 까지 공짜로 얻는다
# ==========================================================================
def bonus_lca_from_same_table():
    print(SEP)
    print("[보너스] #1483 의 표 그대로 LCA 를 얻는다")
    print(SEP)

    class TreeLCA(TreeAncestor):
        def __init__(self, n, parent):
            TreeAncestor.__init__(self, n, parent)
            depth = [0] * n
            for v in range(n):               # parent[i] < i 인 트리라 순서대로 계산 가능
                if parent[v] != -1:
                    depth[v] = depth[parent[v]] + 1
            self.depth = depth

        def lca(self, u, v):
            depth, up = self.depth, self.up
            if depth[u] < depth[v]:
                u, v = v, u
            u = self.getKthAncestor(u, depth[u] - depth[v])
            if u == v:                       # v 가 u 의 조상. 필수 검사!
                return u
            for j in range(self.LOG - 1, -1, -1):
                if up[j][u] != up[j][v]:     # 다를 때만 올라간다
                    u, v = up[j][u], up[j][v]
            return up[0][u]                  # u 가 아니라 부모!

    def lca_brute(parent, u, v):
        anc = set()
        x = u
        while x != -1:
            anc.add(x)
            x = parent[x]
        x = v
        while x not in anc:
            x = parent[x]
        return x

    rng = random.Random(43)
    total = 0
    for _ in range(40):
        m = rng.randint(1, 60)
        par = [-1] + [rng.randrange(i) for i in range(1, m)]
        T = TreeLCA(m, par)
        for u in range(m):
            for v in range(m):
                assert T.lca(u, v) == lca_brute(par, u, v), (m, u, v)
                total += 1
    print("  무작위 트리 40개, 총 {}개 쌍의 LCA 가 전부 나이브와 일치했다.".format(total))
    print()
    print("  같은 up 표 하나로 k 번째 조상과 LCA 를 모두 답한다.")
    print("  이것이 '이진 상승을 배우면 조상 질의 전부가 따라온다' 는 뜻이다.")
    print()


def summary():
    print(SEP)
    print("오늘의 정리")
    print(SEP)
    rows = [
        ("#235  BST", "값 비교로 한 방향 O(h), O(1) 공간"),
        ("#236  일반 이진 트리", "후위 순회 6줄. 양쪽 신호 -> 내가 답"),
        ("#1123 최심 잎 LCA", "(높이, LCA) 튜플을 동시에 올려보낸다"),
        ("#72413 합승 택시", "분기점 c 전수 조사 + 전체 최단 거리"),
        ("#2096 경로 문자열", "루트 경로 두 개의 공통 접두사 제거"),
        ("#1483 k 번째 조상", "이진 상승 up[j][v]=up[j-1][up[j-1][v]]"),
    ]
    for a, b in rows:
        print("  {:<22} {}".format(a, b))
    print()
    print("  놓치기 쉬운 세 가지")
    print("    1. '조상' 에는 자기 자신이 포함된다 (#235 의 p=2,q=4 -> 2)")
    print("    2. 이진 상승 2단계는 큰 k 부터, '다를 때만', 마지막은 up[0][u]")
    print("    3. 파이썬 재귀 한도 1000. 깊은 트리는 BFS + reversed(order) 로")
    print(SEP)


if __name__ == "__main__":
    test_235()
    test_236()
    test_1123()
    test_72413()
    test_2096()
    test_1483()
    bonus_lca_from_same_table()
    summary()
