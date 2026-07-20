# -*- coding: utf-8 -*-
"""
Day 29 - 트리 순회.응용 (Tree Traversal): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(재귀 vs 반복, DFS vs BFS)을 두고 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

import sys
from collections import deque


# 공용 이진 트리 노드 + 리스트 -> 트리 빌더(테스트용)
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(level_values):
    if not level_values:
        return None
    root = TreeNode(level_values[0])
    q = deque([root])
    i, n = 1, len(level_values)
    while q and i < n:
        node = q.popleft()
        if i < n:
            if level_values[i] is not None:
                node.left = TreeNode(level_values[i])
                q.append(node.left)
            i += 1
        if i < n:
            if level_values[i] is not None:
                node.right = TreeNode(level_values[i])
                q.append(node.right)
            i += 1
    return root


# ===========================================================================
# 1. Binary Tree Inorder Traversal (LeetCode #94)
#    (A) 재귀  (B) 스택 반복. 순회 시점 이해의 기본기.
# ===========================================================================
class SolutionInorder:
    def inorderTraversal(self, root):            # 재귀
        res = []

        def dfs(node):
            if node:
                dfs(node.left)
                res.append(node.val)
                dfs(node.right)

        dfs(root)
        return res

    def inorderTraversal_iter(self, root):       # 스택 반복
        res, stack, cur = [], [], root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            res.append(cur.val)
            cur = cur.right
        return res


# ===========================================================================
# 2. Maximum Depth of Binary Tree (LeetCode #104)
#    (A) 재귀 DFS  (B) 레벨 순회 BFS로 층 수 세기.
# ===========================================================================
class SolutionMaxDepth:
    def maxDepth(self, root):                    # DFS
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

    def maxDepth_bfs(self, root):                # BFS 층 카운트
        if root is None:
            return 0
        depth, q = 0, deque([root])
        while q:
            depth += 1
            for _ in range(len(q)):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        return depth


# ===========================================================================
# 3. Invert Binary Tree (LeetCode #226)
#    좌우 자식을 재귀로 맞바꾼다.
# ===========================================================================
class SolutionInvert:
    def invertTree(self, root):
        if root is None:
            return None
        root.left, root.right = (self.invertTree(root.right),
                                 self.invertTree(root.left))
        return root


# ===========================================================================
# 4. Same Tree (LeetCode #100)
#    두 트리를 동시 전위 순회하며 구조.값 비교.
# ===========================================================================
class SolutionSameTree:
    def isSameTree(self, p, q):
        if p is None and q is None:
            return True
        if p is None or q is None or p.val != q.val:
            return False
        return (self.isSameTree(p.left, q.left)
                and self.isSameTree(p.right, q.right))


# ===========================================================================
# 5. Symmetric Tree (LeetCode #101)
#    거울 대칭: 왼쪽의 왼쪽 == 오른쪽의 오른쪽.
# ===========================================================================
class SolutionSymmetric:
    def isSymmetric(self, root):
        if root is None:
            return True

        def mirror(a, b):
            if a is None and b is None:
                return True
            if a is None or b is None or a.val != b.val:
                return False
            return mirror(a.left, b.right) and mirror(a.right, b.left)

        return mirror(root.left, root.right)


# ===========================================================================
# 6. Binary Tree Level Order Traversal (LeetCode #102)
#    BFS로 층별 묶어 반환.
# ===========================================================================
class SolutionLevelOrder:
    def levelOrder(self, root):
        if root is None:
            return []
        res, q = [], deque([root])
        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(level)
        return res


# ===========================================================================
# 7. Path Sum (LeetCode #112)
#    루트->리프 경로 합 == target 존재? 남은 합을 아래로 넘긴다.
# ===========================================================================
class SolutionPathSum:
    def hasPathSum(self, root, targetSum):
        if root is None:
            return False
        if root.left is None and root.right is None:
            return root.val == targetSum
        rest = targetSum - root.val
        return (self.hasPathSum(root.left, rest)
                or self.hasPathSum(root.right, rest))


# ===========================================================================
# 8. Validate Binary Search Tree (LeetCode #98)
#    (A) 중위 순회가 오름차순인지  (B) min/max 경계 전파.
# ===========================================================================
class SolutionValidateBST:
    def isValidBST(self, root):                  # 중위 순회 단조증가
        prev = None
        stack, cur = [], root
        while cur or stack:
            while cur:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            if prev is not None and cur.val <= prev:
                return False
            prev = cur.val
            cur = cur.right
        return True

    def isValidBST_bounds(self, root):           # 경계 전파 재귀
        def valid(node, low, high):
            if node is None:
                return True
            if not (low < node.val < high):
                return False
            return (valid(node.left, low, node.val)
                    and valid(node.right, node.val, high))

        return valid(root, float("-inf"), float("inf"))


# ===========================================================================
# 9. Lowest Common Ancestor of a Binary Tree (LeetCode #236)
#    후위 순회: 좌/우에서 각각 p 또는 q를 찾으면 현재 노드가 LCA.
# ===========================================================================
class SolutionLCA:
    def lowestCommonAncestor(self, root, p, q):
        if root is None or root is p or root is q:
            return root
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)
        if left and right:          # 양쪽에서 하나씩 -> 여기가 갈림점
            return root
        return left if left else right


# ===========================================================================
# 10. 길 찾기 게임 (프로그래머스 #42892, 2019 KAKAO BLIND)
#     좌표로 이진트리 구성(x는 BST 규칙, y 큰 것이 위) 후 전위/후위 순회.
#     핵심: y 내림차순으로 위에서부터 삽입하면 한쪽으로 치우친 트리가 나올 수
#     있어 재귀 순회는 깊이 한계 위험 -> 반복(iterative) 순회를 쓴다.
# ===========================================================================
class _Node:
    __slots__ = ("idx", "x", "left", "right")

    def __init__(self, idx, x):
        self.idx = idx
        self.x = x
        self.left = None
        self.right = None


def solution(nodeinfo):
    # 1) (x, y, 번호) 준비 후 y 내림차순, 같으면 x 오름차순 -> 위에서 아래로 삽입
    nodes = [(x, y, i + 1) for i, (x, y) in enumerate(nodeinfo)]
    nodes.sort(key=lambda t: (-t[1], t[0]))

    # 2) BST 규칙(x 비교)으로 반복 삽입 -> 이진트리 구성
    root = _Node(nodes[0][2], nodes[0][0])
    for x, _, idx in nodes[1:]:
        cur = root
        node = _Node(idx, x)
        while True:
            if x < cur.x:
                if cur.left is None:
                    cur.left = node
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    break
                cur = cur.right

    # 3) 전위/후위 순회(반복) - 10000개 노드에서 재귀 한계 회피
    def preorder_iter(r):
        order, stack = [], [r]
        while stack:
            n = stack.pop()
            order.append(n.idx)
            if n.right:
                stack.append(n.right)
            if n.left:
                stack.append(n.left)
        return order

    def postorder_iter(r):
        order, stack = [], [(r, False)]
        while stack:
            n, processed = stack.pop()
            if processed:
                order.append(n.idx)
            else:
                stack.append((n, True))
                if n.right:
                    stack.append((n.right, False))
                if n.left:
                    stack.append((n.left, False))
        return order

    return [preorder_iter(root), postorder_iter(root)]


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    # 1. Inorder Traversal
    it = SolutionInorder()
    r1 = build_tree([1, None, 2, 3])          # 1 -R-> 2 -L-> 3
    assert it.inorderTraversal(r1) == [1, 3, 2]
    assert it.inorderTraversal_iter(r1) == [1, 3, 2]
    assert it.inorderTraversal(None) == []

    # 2. Maximum Depth
    md = SolutionMaxDepth()
    r2 = build_tree([3, 9, 20, None, None, 15, 7])
    assert md.maxDepth(r2) == 3
    assert md.maxDepth_bfs(r2) == 3
    assert md.maxDepth(None) == 0

    # 3. Invert Tree
    iv = SolutionInvert()
    inv = iv.invertTree(build_tree([4, 2, 7, 1, 3, 6, 9]))

    def bfs_vals(root):                       # 뒤집힌 트리 레벨 순회로 검증
        out, q = [], deque([root]) if root else deque()
        while q:
            n = q.popleft()
            out.append(n.val)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        return out

    assert bfs_vals(inv) == [4, 7, 2, 9, 6, 3, 1]

    # 4. Same Tree
    st = SolutionSameTree()
    assert st.isSameTree(build_tree([1, 2, 3]), build_tree([1, 2, 3])) is True
    assert st.isSameTree(build_tree([1, 2]), build_tree([1, None, 2])) is False

    # 5. Symmetric Tree
    sy = SolutionSymmetric()
    assert sy.isSymmetric(build_tree([1, 2, 2, 3, 4, 4, 3])) is True
    assert sy.isSymmetric(build_tree([1, 2, 2, None, 3, None, 3])) is False

    # 6. Level Order
    lo = SolutionLevelOrder()
    assert lo.levelOrder(r2) == [[3], [9, 20], [15, 7]]
    assert lo.levelOrder(None) == []

    # 7. Path Sum
    ps = SolutionPathSum()
    r7 = build_tree([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])
    assert ps.hasPathSum(r7, 22) is True     # 5+4+11+2
    assert ps.hasPathSum(r7, 100) is False
    assert ps.hasPathSum(None, 0) is False

    # 8. Validate BST
    vb = SolutionValidateBST()
    assert vb.isValidBST(build_tree([2, 1, 3])) is True
    assert vb.isValidBST(build_tree([5, 1, 4, None, None, 3, 6])) is False
    assert vb.isValidBST_bounds(build_tree([2, 1, 3])) is True
    assert vb.isValidBST_bounds(build_tree([5, 1, 4, None, None, 3, 6])) is False

    # 9. Lowest Common Ancestor
    lca = SolutionLCA()
    root9 = build_tree([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    p = root9.left               # 5
    q = root9.right              # 1
    assert lca.lowestCommonAncestor(root9, p, q).val == 3
    q2 = root9.left.right.right   # 4
    assert lca.lowestCommonAncestor(root9, p, q2).val == 5

    # 10. 길 찾기 게임 (프로그래머스 #42892)
    ans = solution([[5, 3], [11, 5], [13, 3], [3, 5], [6, 1], [1, 3],
                    [8, 6], [7, 2], [2, 2]])
    assert ans == [[7, 4, 6, 9, 1, 8, 5, 2, 3],
                   [9, 6, 5, 8, 1, 4, 3, 2, 7]]

    print("Day 29 solutions: all tests passed OK")


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    _run_tests()
