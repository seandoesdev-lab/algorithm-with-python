# -*- coding: utf-8 -*-
"""Day 44 연습문제 해설 - 트리 DP (Tree DP)

실행:  PYTHONIOENCODING=cp949 python solutions.py

문제 목록 (출처: LeetCode / 프로그래머스)
  1. LeetCode #543   Diameter of Binary Tree            - 경로형 입문
  2. LeetCode #337   House Robber III                   - dp[v][0/1]
  3. LeetCode #124   Binary Tree Maximum Path Sum       - 경로형 + 음수 클램프
  4. 프로그래머스 #92343  양과 늑대                      - 트리 위 완전 탐색
  5. LeetCode #968   Binary Tree Cameras                - 3-state DP vs 그리디
  6. LeetCode #834   Sum of Distances in Tree           - 리루팅 2-pass

각 문제는 플랫폼 시그니처를 그대로 쓰고, 가능한 곳은 다중 접근 + 교차 검증을 붙였다.
표준 라이브러리만 사용한다.
"""

from collections import deque
import random

INF = float("inf")


# =====================================================================
# 공통 - 이진 트리 노드와 헬퍼
# =====================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(values):
    """LeetCode 레벨 순서 배열(None 포함)에서 이진 트리를 만든다."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    dq = deque([root])
    i = 1
    while dq and i < len(values):
        node = dq.popleft()
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.left = TreeNode(v)
                dq.append(node.left)
        if i < len(values):
            v = values[i]
            i += 1
            if v is not None:
                node.right = TreeNode(v)
                dq.append(node.right)
    return root


def postorder_nodes(root):
    """반복 후위 순회 - 자식이 부모보다 먼저 나오는 노드 목록. 재귀 0줄."""
    out, stack = [], [(root, False)]
    while stack:
        node, done = stack.pop()
        if node is None:
            continue
        if done:
            out.append(node)
        else:
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))
    return out


def random_binary_tree(n, seed=0, lo=-10, hi=10):
    """무작위 이진 트리(검증 전용). n 개 노드, 값은 [lo, hi]."""
    if n == 0:
        return None
    rng = random.Random(seed)
    root = TreeNode(rng.randint(lo, hi))
    nodes = [root]
    for _ in range(n - 1):
        node = TreeNode(rng.randint(lo, hi))
        while True:
            p = rng.choice(nodes)
            if p.left is None:
                p.left = node
                break
            if p.right is None:
                p.right = node
                break
        nodes.append(node)
    return root


# =====================================================================
# 1. LeetCode #543 - Diameter of Binary Tree
#    "경로형 트리 DP" 의 가장 순한 입문.
#    올려보내는 값(한 갈래 최장 깊이) != 정답(두 갈래 합)
# =====================================================================
class SolutionDiameter:
    def diameterOfBinaryTree(self, root: "TreeNode") -> int:
        """접근 1) 재귀 트리 DP. O(N) 시간, O(h) 공간."""
        best = 0

        def depth(node):
            nonlocal best
            if node is None:
                return 0
            l = depth(node.left)
            r = depth(node.right)
            if l + r > best:
                best = l + r             # 여기서 꺾이는 경로 = 정답 후보
            return max(l, r) + 1         # 부모에게는 한 갈래만 올려보낸다

        depth(root)
        return best

    def diameterIterative(self, root: "TreeNode") -> int:
        """접근 2) 반복 후위 순회. 재귀 0줄이라 깊은 트리에서도 안전하다."""
        best = 0
        depth = {}
        for node in postorder_nodes(root):
            l = depth.get(node.left, 0)
            r = depth.get(node.right, 0)
            if l + r > best:
                best = l + r
            depth[node] = max(l, r) + 1
        return best


def test_543():
    s = SolutionDiameter()
    cases = [
        ([1, 2, 3, 4, 5], 3),        # 4-2-1-3 (간선 3개)
        ([1, 2], 1),
        ([1], 0),
    ]
    for values, want in cases:
        for fn in (s.diameterOfBinaryTree, s.diameterIterative):
            got = fn(build_tree(values))
            assert got == want, (values, fn.__name__, got, want)

    # 왼쪽으로 늘어진 체인 100개 -> 지름 99
    root = TreeNode(0)
    cur = root
    for i in range(1, 100):
        cur.left = TreeNode(i)
        cur = cur.left
    assert s.diameterOfBinaryTree(root) == 99
    assert s.diameterIterative(root) == 99

    # 두 접근 교차 검증
    for seed in range(40):
        t = random_binary_tree(random.Random(seed).randint(1, 40), seed=seed)
        assert s.diameterOfBinaryTree(t) == s.diameterIterative(t), seed
    print("  #543 Diameter of Binary Tree ....... OK (재귀 / 반복 두 접근 일치)")


# =====================================================================
# 2. LeetCode #337 - House Robber III
#    dp[v][0] = v 를 안 턴다,  dp[v][1] = v 를 턴다
#    턴다면 자식은 반드시 안 턴 값(dp[c][0])만 쓸 수 있다
# =====================================================================
class SolutionRobber:
    def rob(self, root: "TreeNode") -> int:
        """접근 1) (안 턴다, 턴다) 튜플을 올려보내는 1-pass 재귀. O(N)."""
        def dfs(node):
            if node is None:
                return (0, 0)                       # (skip, take)
            ls, lt = dfs(node.left)
            rs, rt = dfs(node.right)
            skip = max(ls, lt) + max(rs, rt)        # 안 털면 자식은 자유
            take = node.val + ls + rs               # 털면 자식은 못 턴다
            return (skip, take)

        return max(dfs(root))

    def robIterative(self, root: "TreeNode") -> int:
        """접근 2) 반복 후위 순회. 재귀 0줄, 같은 점화식."""
        dp = {}                                     # node -> (skip, take)
        for node in postorder_nodes(root):
            ls, lt = dp.get(node.left, (0, 0))
            rs, rt = dp.get(node.right, (0, 0))
            dp[node] = (max(ls, lt) + max(rs, rt), node.val + ls + rs)
        return max(dp.get(root, (0, 0)))


def rob_bruteforce(root):
    """모든 독립 집합을 전수 조사(검증 전용). 노드가 적을 때만."""
    nodes = postorder_nodes(root)
    idx = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    if n == 0:
        return 0
    best = 0
    for mask in range(1 << n):
        ok = True
        for node in nodes:
            if not (mask >> idx[node]) & 1:
                continue
            for c in (node.left, node.right):
                if c is not None and (mask >> idx[c]) & 1:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            total = sum(nodes[i].val for i in range(n) if (mask >> i) & 1)
            if total > best:
                best = total
    return best


def test_337():
    s = SolutionRobber()
    cases = [
        ([3, 2, 3, None, 3, None, 1], 7),
        ([3, 4, 5, 1, 3, None, 1], 9),
        ([0], 0),
    ]
    for values, want in cases:
        for fn in (s.rob, s.robIterative):
            got = fn(build_tree(values))
            assert got == want, (values, fn.__name__, got, want)

    for seed in range(30):
        t = random_binary_tree(random.Random(seed * 5).randint(1, 12), seed=seed, lo=0, hi=20)
        want = rob_bruteforce(t)
        assert s.rob(t) == want, seed
        assert s.robIterative(t) == want, seed
    print("  #337 House Robber III .............. OK (DP vs 부분집합 전수 일치)")


# =====================================================================
# 3. LeetCode #124 - Binary Tree Maximum Path Sum
#    #543 과 골격이 같지만 값이 음수일 수 있어 max(gain, 0) 클램프가 필수.
#    답의 초깃값은 0 이 아니라 -inf 여야 한다.
# =====================================================================
class SolutionMaxPathSum:
    def maxPathSum(self, root: "TreeNode") -> int:
        """접근 1) 재귀 gain + 음수 클램프. O(N)."""
        best = -INF

        def gain(node):
            nonlocal best
            if node is None:
                return 0
            l = max(gain(node.left), 0)          # 음수 가지는 안 타는 게 이득
            r = max(gain(node.right), 0)
            cur = node.val + l + r               # 여기서 꺾이는 경로
            if cur > best:
                best = cur
            return node.val + max(l, r)          # 부모에게는 한 갈래만

        gain(root)
        return int(best)

    def maxPathSumIterative(self, root: "TreeNode") -> int:
        """접근 2) 반복 후위 순회. 깊은 트리에서도 안전."""
        best = -INF
        gain = {}
        for node in postorder_nodes(root):
            l = max(gain.get(node.left, 0), 0)
            r = max(gain.get(node.right, 0), 0)
            cur = node.val + l + r
            if cur > best:
                best = cur
            gain[node] = node.val + max(l, r)
        return int(best)


def test_124():
    s = SolutionMaxPathSum()
    cases = [
        ([1, 2, 3], 6),
        ([-10, 9, 20, None, None, 15, 7], 42),
        ([-3], -3),                     # 전부 음수 - best 초깃값이 0 이면 틀린다
        ([-2, -1], -1),
        ([2, -1], 2),
    ]
    for values, want in cases:
        for fn in (s.maxPathSum, s.maxPathSumIterative):
            got = fn(build_tree(values))
            assert got == want, (values, fn.__name__, got, want)

    for seed in range(40):
        t = random_binary_tree(random.Random(seed * 3).randint(1, 30), seed=seed, lo=-15, hi=15)
        assert s.maxPathSum(t) == s.maxPathSumIterative(t), seed
    print("  #124 Binary Tree Maximum Path Sum .. OK (음수 트리 포함, 두 접근 일치)")


# =====================================================================
# 4. 프로그래머스 #92343 - 양과 늑대 (2022 KAKAO BLIND RECRUITMENT)
#    "트리라고 전부 트리 DP는 아니다" 의 대표 사례.
#    이미 방문한 노드 어디로든 되돌아갈 수 있어 서브트리로 분해되지 않는다.
#    n <= 17 이 "지수 탐색을 허용한다"는 신호다.
# =====================================================================
def solution(info, edges):
    """접근 1) 방문 가능 후보 집합을 들고 다니는 DFS. O(2^n * n)."""
    n = len(info)
    children = [[] for _ in range(n)]
    for p, c in edges:
        children[p].append(c)

    best = 1                                    # 루트(0번)는 항상 양이다

    def dfs(sheep, wolf, candidates):
        nonlocal best
        if sheep > best:
            best = sheep
        for c in candidates:
            ns, nw = (sheep + 1, wolf) if info[c] == 0 else (sheep, wolf + 1)
            if ns <= nw:                        # 늑대가 양 이상이면 전멸
                continue
            nxt = set(candidates)
            nxt.remove(c)
            nxt.update(children[c])             # c 를 먹었으니 c 의 자식이 열린다
            dfs(ns, nw, nxt)

    dfs(1, 0, set(children[0]))
    return best


def solution_bitmask(info, edges):
    """접근 2) 방문 집합을 비트마스크로 두고 같은 집합을 두 번 안 본다.

    (양, 늑대) 수는 방문 집합만으로 결정되므로 mask 를 메모하면 안전하다.
    상태 수가 최대 2^17 이라 실전에서 훨씬 빠르다.
    """
    n = len(info)
    parent = [-1] * n
    for p, c in edges:
        parent[c] = p

    best = 1
    seen = set()
    stack = [(1, 1, 0)]                         # (mask, sheep, wolf)
    while stack:
        mask, s, w = stack.pop()
        if mask in seen:
            continue
        seen.add(mask)
        if s > best:
            best = s
        for v in range(n):
            if (mask >> v) & 1:
                continue
            p = parent[v]
            if p == -1 or not (mask >> p) & 1:  # 부모를 아직 안 먹었다
                continue
            ns, nw = (s + 1, w) if info[v] == 0 else (s, w + 1)
            if ns <= nw:
                continue
            stack.append((mask | (1 << v), ns, nw))
    return best


def test_92343():
    cases = [
        (
            [0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
            [[0, 1], [1, 2], [1, 4], [0, 8], [8, 7], [9, 10], [9, 11],
             [4, 3], [6, 5], [4, 6], [8, 9]],
            5,
        ),
        (
            [0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0],
            [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7],
             [4, 8], [6, 9], [9, 10]],
            5,
        ),
        ([0], [], 1),                            # 노드 하나면 양 1마리
        ([0, 1], [[0, 1]], 1),                   # 늑대를 먹으면 1대1 -> 전멸
        ([0, 0], [[0, 1]], 2),
    ]
    for info, edges, want in cases:
        assert solution(info, edges) == want, (info, want, solution(info, edges))
        assert solution_bitmask(info, edges) == want, (info, want)
    print("  #92343 양과 늑대 ................... OK (집합 DFS / 비트마스크 일치)")


# =====================================================================
# 5. LeetCode #968 - Binary Tree Cameras
#    3-state 트리 DP: (카메라 설치 / 감시됨 / 감시 안 됨)
# =====================================================================
class SolutionCameras:
    def minCameraCover(self, root: "TreeNode") -> int:
        """접근 1) 3-state DP. O(N).

        반환 (A, B, C)
          A = 이 노드에 카메라를 설치한다
          B = 카메라는 없지만 감시되고 있다 (자식 중 누군가에 카메라)
          C = 카메라도 없고 감시도 안 된다 (부모가 책임진다)
        빈 노드는 (INF, 0, 0) - 카메라를 놓을 수 없고, 감시 여부는 따질 게 없다.
        """
        def dfs(node):
            if node is None:
                return (INF, 0, 0)
            la, lb, lc = dfs(node.left)
            ra, rb, rc = dfs(node.right)
            a = 1 + min(la, lb, lc) + min(ra, rb, rc)
            b = min(la + min(ra, rb), ra + min(la, lb))
            c = lb + rb
            return (a, b, c)

        a, b, _ = dfs(root)
        return int(min(a, b))            # C 는 안 된다 - 루트 위에 부모가 없다

    def minCameraCoverGreedy(self, root: "TreeNode") -> int:
        """접근 2) 아래에서 위로 그리디. 더 짧지만 최적성 논증이 필요하다.

        상태 0 = 감시 안 됨, 1 = 감시됨, 2 = 카메라 있음
        "감시 안 된 자식이 하나라도 있으면 지금 나에게 카메라를 놓는다."
        """
        count = 0

        def dfs(node):
            nonlocal count
            if node is None:
                return 1                 # 빈 노드는 감시된 것으로 친다
            l = dfs(node.left)
            r = dfs(node.right)
            if l == 0 or r == 0:
                count += 1
                return 2
            if l == 2 or r == 2:
                return 1
            return 0

        if dfs(root) == 0:               # 루트가 감시 안 됐으면 하나 더
            count += 1
        return count


def test_968():
    s = SolutionCameras()
    cases = [
        ([0, 0, None, 0, 0], 1),
        ([0, 0, None, 0, None, 0, None, None, 0], 2),
        ([0], 1),
        ([0, 0], 1),
    ]
    for values, want in cases:
        for fn in (s.minCameraCover, s.minCameraCoverGreedy):
            got = fn(build_tree(values))
            assert got == want, (values, fn.__name__, got, want)

    for seed in range(60):
        t = random_binary_tree(random.Random(seed * 9 + 2).randint(1, 30), seed=seed, lo=0, hi=0)
        assert s.minCameraCover(t) == s.minCameraCoverGreedy(t), seed
    print("  #968 Binary Tree Cameras ........... OK (3-state DP vs 그리디 일치)")


# =====================================================================
# 6. LeetCode #834 - Sum of Distances in Tree
#    리루팅(rerooting) 2-pass. "모든 노드에 대한 답"의 표준 도구.
# =====================================================================
class SolutionSumOfDistances:
    def sumOfDistancesInTree(self, n: int, edges) -> list:
        """접근 1) 리루팅 2-pass. O(N). 재귀 0줄."""
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        # BFS 로 parent / 순서를 만든다 (재귀 없음)
        parent = [-1] * n
        visited = [False] * n
        visited[0] = True
        order = [0]
        dq = deque([0])
        while dq:
            v = dq.popleft()
            for w in adj[v]:
                if not visited[w]:
                    visited[w] = True
                    parent[w] = v
                    order.append(w)
                    dq.append(w)

        cnt = [1] * n
        ans = [0] * n
        for v in reversed(order):            # 1차: 아래 -> 위
            p = parent[v]
            if p != -1:
                cnt[p] += cnt[v]
                ans[p] += ans[v] + cnt[v]
        for v in order[1:]:                  # 2차: 위 -> 아래 (순서가 정반대!)
            p = parent[v]
            ans[v] = ans[p] - cnt[v] + (n - cnt[v])
        return ans

    def sumOfDistancesNaive(self, n: int, edges) -> list:
        """접근 2) 각 노드에서 BFS. O(N^2). 검증 기준선."""
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)
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


def test_834():
    s = SolutionSumOfDistances()
    cases = [
        (6, [[0, 1], [0, 2], [2, 3], [2, 4], [2, 5]], [8, 12, 6, 10, 10, 10]),
        (1, [], [0]),
        (2, [[1, 0]], [1, 1]),
    ]
    for n, edges, want in cases:
        got = s.sumOfDistancesInTree(n, edges)
        assert got == want, (n, got, want)
        assert s.sumOfDistancesNaive(n, edges) == want

    for seed in range(40):
        rng = random.Random(seed)
        n = rng.randint(1, 60)
        edges = [[i, rng.randint(0, i - 1)] for i in range(1, n)]
        assert s.sumOfDistancesInTree(n, edges) == s.sumOfDistancesNaive(n, edges), seed

    # 체인 5개:  0-1-2-3-4  ->  [10, 7, 6, 7, 10]
    chain = [[i, i + 1] for i in range(4)]
    assert s.sumOfDistancesInTree(5, chain) == [10, 7, 6, 7, 10]
    print("  #834 Sum of Distances in Tree ...... OK (리루팅 vs 나이브 일치)")


# =====================================================================
if __name__ == "__main__":
    print("=" * 62)
    print("Day 44 연습문제 해설 - 트리 DP (Tree DP)")
    print("=" * 62)
    test_543()
    test_337()
    test_124()
    test_92343()
    test_968()
    test_834()
    print("=" * 62)
    print("전체 6문제 자체 테스트 통과")
    print()
    print("복잡도 요약")
    print("  #543   경로형 트리 DP           O(N) 시간 / O(h) 공간")
    print("  #337   dp[v][0/1] 상태 추가형   O(N) 시간 / O(h) 공간")
    print("  #124   경로형 + 음수 클램프     O(N) 시간 / O(h) 공간")
    print("  #92343 방문 집합 완전 탐색      O(2^n * n),  n <= 17 이라 가능")
    print("  #968   3-state DP / 그리디      O(N) 시간 / O(h) 공간")
    print("  #834   리루팅 2-pass            O(N)  (나이브는 O(N^2) 로 불가)")
    print("=" * 62)
