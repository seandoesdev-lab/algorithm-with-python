# -*- coding: utf-8 -*-
"""
Day 11 - 트리 기본 (Tree Basics) 문제 해설

- LeetCode 문제는 `class Solution` 시그니처를 따른다.
- 프로그래머스 문제는 `def solution(...)` 시그니처를 따른다.
- 각 문제는 가능한 경우 다중 접근(재귀/반복, DFS/BFS)을 보여주고
  맨 아래 assert 로 자체 검증한다.
- cp949 콘솔 안전: print 출력에는 ASCII 기호(=, -, O, X)만 사용(한글은 OK).

실행:  PYTHONIOENCODING=cp949 python solutions.py
"""

import sys
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build(values):
    """레벨 순서 리스트(None=빈 자리)로 이진 트리 생성 (테스트용).

    LeetCode 직렬화 규칙: 큐에서 노드를 꺼낼 때마다 다음 두 칸을
    각각 왼쪽/오른쪽 자식으로 소비한다(None이면 자식 없음).
    """
    if not values:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    n = len(values)
    while q and i < n:
        node = q.popleft()
        if i < n:                      # 왼쪽 자식 자리
            if values[i] is not None:
                node.left = TreeNode(values[i])
                q.append(node.left)
            i += 1
        if i < n:                      # 오른쪽 자식 자리
            if values[i] is not None:
                node.right = TreeNode(values[i])
                q.append(node.right)
            i += 1
    return root


# ===========================================================================
# 1) LeetCode #104 - Maximum Depth of Binary Tree
# ===========================================================================
class SolutionMaxDepth:
    # 접근 A: 재귀 DFS  - O(N) 시간 / O(h) 공간
    def maxDepth(self, root):
        if not root:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

    # 접근 B: 반복 BFS(레벨 수 세기) - O(N) 시간 / O(W) 공간(W=최대 너비)
    def maxDepthBFS(self, root):
        if not root:
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
# 2) LeetCode #226 - Invert Binary Tree
# ===========================================================================
class SolutionInvert:
    # 접근 A: 재귀 - O(N)
    def invertTree(self, root):
        if not root:
            return None
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root

    # 접근 B: 반복 BFS - O(N)
    def invertTreeBFS(self, root):
        if not root:
            return None
        q = deque([root])
        while q:
            node = q.popleft()
            node.left, node.right = node.right, node.left
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        return root


# ===========================================================================
# 3) LeetCode #100 - Same Tree
# ===========================================================================
class SolutionSameTree:
    # 접근 A: 동시 재귀 - O(N)
    def isSameTree(self, p, q):
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)


# ===========================================================================
# 4) LeetCode #94 - Binary Tree Inorder Traversal
# ===========================================================================
class SolutionInorder:
    # 접근 A: 재귀 - O(N)
    def inorderTraversal(self, root):
        out = []

        def dfs(node):
            if not node:
                return
            dfs(node.left)
            out.append(node.val)
            dfs(node.right)

        dfs(root)
        return out

    # 접근 B: 명시적 스택(반복) - O(N), 깊은 트리 안전
    def inorderIter(self, root):
        out, stack, cur = [], [], root
        while cur or stack:
            while cur:                 # 왼쪽 끝까지 내려가며 쌓기
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()          # 가장 왼쪽부터 방문
            out.append(cur.val)
            cur = cur.right            # 오른쪽으로
        return out


# ===========================================================================
# 5) LeetCode #101 - Symmetric Tree
# ===========================================================================
class SolutionSymmetric:
    # 접근 A: 거울 비교 재귀 - O(N)
    def isSymmetric(self, root):
        def mirror(a, b):
            if not a and not b:
                return True
            if not a or not b or a.val != b.val:
                return False
            return mirror(a.left, b.right) and mirror(a.right, b.left)

        return mirror(root, root) if root else True


# ===========================================================================
# 6) LeetCode #110 - Balanced Binary Tree
# ===========================================================================
class SolutionBalanced:
    # 접근: 높이 계산 중 불균형이면 -1 전파 - O(N)
    def isBalanced(self, root):
        def height(node):
            if not node:
                return 0
            lh = height(node.left)
            if lh == -1:
                return -1
            rh = height(node.right)
            if rh == -1:
                return -1
            if abs(lh - rh) > 1:
                return -1
            return 1 + max(lh, rh)

        return height(root) != -1


# ===========================================================================
# 7) LeetCode #543 - Diameter of Binary Tree
# ===========================================================================
class SolutionDiameter:
    # 접근: 높이 DFS 도중 (왼 높이 + 오 높이) 최댓값 갱신 - O(N)
    def diameterOfBinaryTree(self, root):
        self.best = 0

        def height(node):
            if not node:
                return 0
            lh = height(node.left)
            rh = height(node.right)
            self.best = max(self.best, lh + rh)   # 이 노드를 꺾인점으로 한 경로
            return 1 + max(lh, rh)

        height(root)
        return self.best


# ===========================================================================
# 8) LeetCode #108 - Convert Sorted Array to BST
# ===========================================================================
class SolutionSortedToBST:
    # 접근: 가운데를 루트로 분할정복 - O(N)
    def sortedArrayToBST(self, nums):
        def build_bst(lo, hi):
            if lo > hi:
                return None
            mid = (lo + hi) // 2
            node = TreeNode(nums[mid])
            node.left = build_bst(lo, mid - 1)
            node.right = build_bst(mid + 1, hi)
            return node

        return build_bst(0, len(nums) - 1)


# ===========================================================================
# 9) LeetCode #235 - Lowest Common Ancestor of a BST
# ===========================================================================
class SolutionLCA:
    # 접근 A: 반복(BST 성질) - O(h) 시간 / O(1) 공간
    def lowestCommonAncestor(self, root, p, q):
        cur = root
        while cur:
            if p.val < cur.val and q.val < cur.val:
                cur = cur.left
            elif p.val > cur.val and q.val > cur.val:
                cur = cur.right
            else:
                return cur
        return None


# ===========================================================================
# 10) 프로그래머스 #42892 - 길 찾기 게임
#     반복(iterative) 삽입/순회로 재귀 한계를 피한다(노드 최대 10000).
# ===========================================================================
def solution(nodeinfo):
    # 각 노드에 1-기반 번호를 붙인다.
    nodes = [(x, y, idx + 1) for idx, (x, y) in enumerate(nodeinfo)]
    # y 내림차순(위에서 아래), 같으면 x 오름차순(왼->오)으로 삽입 순서 결정.
    nodes.sort(key=lambda t: (-t[1], t[0]))

    class N:
        __slots__ = ("num", "x", "left", "right")

        def __init__(self, num, x):
            self.num = num
            self.x = x
            self.left = None
            self.right = None

    root = N(nodes[0][2], nodes[0][0])
    for x, y, num in nodes[1:]:
        cur = root
        while True:                       # x를 BST 키처럼 비교하며 자리 찾기
            if x < cur.x:
                if cur.left is None:
                    cur.left = N(num, x)
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = N(num, x)
                    break
                cur = cur.right

    # 전위 순회(반복): 부모 -> 왼 -> 오
    def preorder_iter(node):
        out, stack = [], [node]
        while stack:
            cur = stack.pop()
            out.append(cur.num)
            if cur.right:
                stack.append(cur.right)
            if cur.left:
                stack.append(cur.left)
        return out

    # 후위 순회(반복): 왼 -> 오 -> 부모 (변형 전위 후 뒤집기)
    def postorder_iter(node):
        out, stack = [], [node]
        while stack:
            cur = stack.pop()
            out.append(cur.num)
            if cur.left:
                stack.append(cur.left)
            if cur.right:
                stack.append(cur.right)
        out.reverse()
        return out

    return [preorder_iter(root), postorder_iter(root)]


# ===========================================================================
# 자체 검증
# ===========================================================================
def main():
    sys.setrecursionlimit(10 ** 6)
    print("=" * 56)
    print("Day 11 - 트리 기본 solutions 자체 검증")
    print("=" * 56)

    # 1) Max Depth
    s = SolutionMaxDepth()
    t = build([3, 9, 20, None, None, 15, 7])
    assert s.maxDepth(t) == 3
    assert s.maxDepthBFS(t) == 3
    assert s.maxDepth(None) == 0
    print("[1] Maximum Depth                 : OK")

    # 2) Invert
    si = SolutionInvert()
    inv = si.invertTree(build([4, 2, 7, 1, 3, 6, 9]))
    out = []
    q = deque([inv])           # 레벨 순회로 결과 확인
    while q:
        n = q.popleft()
        if n:
            out.append(n.val)
            q.append(n.left)
            q.append(n.right)
    assert out == [4, 7, 2, 9, 6, 3, 1]
    inv2 = si.invertTreeBFS(build([1, 2, 3]))
    assert (inv2.left.val, inv2.right.val) == (3, 2)
    print("[2] Invert Binary Tree            : OK")

    # 3) Same Tree
    ss = SolutionSameTree()
    assert ss.isSameTree(build([1, 2, 3]), build([1, 2, 3])) is True
    assert ss.isSameTree(build([1, 2]), build([1, None, 2])) is False
    assert ss.isSameTree(None, None) is True
    print("[3] Same Tree                     : OK")

    # 4) Inorder
    sin = SolutionInorder()
    t = build([1, None, 2, 3])   # 1 - (오)2 - (2의 왼)3
    assert sin.inorderTraversal(t) == [1, 3, 2]
    assert sin.inorderIter(t) == [1, 3, 2]
    assert sin.inorderTraversal(None) == []
    print("[4] Inorder Traversal             : OK")

    # 5) Symmetric
    sym = SolutionSymmetric()
    assert sym.isSymmetric(build([1, 2, 2, 3, 4, 4, 3])) is True
    assert sym.isSymmetric(build([1, 2, 2, None, 3, None, 3])) is False
    print("[5] Symmetric Tree                : OK")

    # 6) Balanced
    sb = SolutionBalanced()
    assert sb.isBalanced(build([3, 9, 20, None, None, 15, 7])) is True
    assert sb.isBalanced(build([1, 2, 2, 3, 3, None, None, 4, 4])) is False
    assert sb.isBalanced(None) is True
    print("[6] Balanced Binary Tree          : OK")

    # 7) Diameter
    sd = SolutionDiameter()
    assert sd.diameterOfBinaryTree(build([1, 2, 3, 4, 5])) == 3  # 4-2-1-3 = 간선 3
    assert sd.diameterOfBinaryTree(build([1, 2])) == 1
    print("[7] Diameter of Binary Tree       : OK")

    # 8) Sorted Array -> BST (중위 순회하면 원래 배열로 복원되어야 함)
    sab = SolutionSortedToBST()
    nums = [-10, -3, 0, 5, 9]
    bst = sab.sortedArrayToBST(nums)
    restored = SolutionInorder().inorderTraversal(bst)
    assert restored == nums
    print("[8] Convert Sorted Array to BST   : OK")

    # 9) LCA of BST
    slca = SolutionLCA()
    bst = build([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    p = bst.left            # 2
    qn = bst.right          # 8
    assert slca.lowestCommonAncestor(bst, p, qn).val == 6
    p2 = bst.left           # 2
    q2 = bst.left.right     # 4
    assert slca.lowestCommonAncestor(bst, p2, q2).val == 2  # 한쪽이 조상
    print("[9] Lowest Common Ancestor (BST)  : OK")

    # 10) 프로그래머스 - 길 찾기 게임 (공식 예시)
    nodeinfo = [[5, 3], [11, 5], [13, 3], [3, 5], [6, 1], [1, 3],
                [8, 6], [7, 2], [2, 2]]
    expected = [[7, 4, 6, 9, 1, 8, 5, 2, 3],
                [9, 6, 5, 8, 1, 4, 3, 2, 7]]
    assert solution(nodeinfo) == expected
    print("[10] 길 찾기 게임 (프로그래머스)    : OK")

    print("\n모든 solutions 검증 통과")


if __name__ == "__main__":
    main()
