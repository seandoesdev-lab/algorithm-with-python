# -*- coding: utf-8 -*-
"""
Day 11 - 트리 기본 (Tree Basics) 예제 모음

표준 라이브러리만 사용한다. cp949 콘솔에서도 안전하도록
print 출력에는 ASCII 기호(=, -, O, X)만 쓴다(한글은 OK).

실행:  PYTHONIOENCODING=cp949 python examples.py
"""

from collections import deque


class TreeNode:
    """이진 트리 노드 (값 + 왼쪽/오른쪽 자식)."""

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------------------------------------------------------------------------
# 테스트용: 리스트(레벨 순서, None은 빈 자리) <-> 트리 변환
# ---------------------------------------------------------------------------
def build(values):
    """레벨 순서 리스트로 이진 트리를 만든다. None은 자식 없음.

    노드를 꺼낼 때마다 다음 두 칸을 왼쪽/오른쪽 자식으로 소비한다.
    """
    if not values:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    n = len(values)
    while q and i < n:
        node = q.popleft()
        if i < n:
            if values[i] is not None:
                node.left = TreeNode(values[i])
                q.append(node.left)
            i += 1
        if i < n:
            if values[i] is not None:
                node.right = TreeNode(values[i])
                q.append(node.right)
            i += 1
    return root


# ---------------------------------------------------------------------------
# 1) 깊이/개수: "나 + 왼쪽 + 오른쪽" 재귀 틀
# ---------------------------------------------------------------------------
def max_depth(node):
    if not node:
        return 0
    return 1 + max(max_depth(node.left), max_depth(node.right))


def count_nodes(node):
    if not node:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


def sum_values(node):
    if not node:
        return 0
    return node.val + sum_values(node.left) + sum_values(node.right)


# ---------------------------------------------------------------------------
# 2) 순회 (DFS): 전위 / 중위 / 후위
# ---------------------------------------------------------------------------
def preorder(node, out):
    if not node:
        return
    out.append(node.val)        # 부모 먼저
    preorder(node.left, out)
    preorder(node.right, out)


def inorder(node, out):
    if not node:
        return
    inorder(node.left, out)
    out.append(node.val)        # 부모 가운데
    inorder(node.right, out)


def postorder(node, out):
    if not node:
        return
    postorder(node.left, out)
    postorder(node.right, out)
    out.append(node.val)        # 부모 마지막


def preorder_iter(root):
    """전위 순회의 반복문(명시적 스택) 버전 - 깊은 트리에서 재귀 한계 회피."""
    out, stack = [], ([root] if root else [])
    while stack:
        node = stack.pop()
        out.append(node.val)
        # 스택은 LIFO라 오른쪽을 먼저 넣어야 왼쪽이 먼저 나온다.
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out


# ---------------------------------------------------------------------------
# 3) 레벨 순회 (BFS): 큐 사용, 레벨별로 묶기
# ---------------------------------------------------------------------------
def level_order(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):          # 현재 레벨 크기만큼만 처리
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
    return out


# ---------------------------------------------------------------------------
# 4) BST: 삽입과 탐색 (값 비교로 한쪽만 내려감)
# ---------------------------------------------------------------------------
def bst_insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = bst_insert(root.left, val)
    else:
        root.right = bst_insert(root.right, val)
    return root


def bst_search(root, target):
    cur = root
    while cur:
        if target == cur.val:
            return True
        cur = cur.left if target < cur.val else cur.right
    return False


def build_bst(values):
    root = None
    for v in values:
        root = bst_insert(root, v)
    return root


# ---------------------------------------------------------------------------
# 데모
# ---------------------------------------------------------------------------
def main():
    print("=" * 56)
    print("Day 11 - 트리 기본 (Tree Basics) 예제")
    print("=" * 56)

    # 예제 트리:        1
    #                 /   \
    #                2     3
    #               / \
    #              4   5
    root = build([1, 2, 3, 4, 5])

    print("\n[1] 깊이/개수/합")
    print("max_depth   =", max_depth(root))        # 3
    print("count_nodes =", count_nodes(root))      # 5
    print("sum_values  =", sum_values(root))       # 15

    print("\n[2] 순회 (DFS)")
    pre = []
    preorder(root, pre)
    ino = []
    inorder(root, ino)
    post = []
    postorder(root, post)
    print("preorder  =", pre)                       # [1, 2, 4, 5, 3]
    print("inorder   =", ino)                       # [4, 2, 5, 1, 3]
    print("postorder =", post)                      # [4, 5, 2, 3, 1]
    print("preorder_iter =", preorder_iter(root))   # 재귀와 동일

    print("\n[3] 레벨 순회 (BFS)")
    print("level_order =", level_order(root))       # [[1], [2, 3], [4, 5]]

    print("\n[4] 이진 탐색 트리 (BST)")
    bst = build_bst([5, 3, 8, 1, 4, 7, 9])
    bst_ino = []
    inorder(bst, bst_ino)
    print("BST 중위 순회(정렬됨) =", bst_ino)        # [1, 3, 4, 5, 7, 8, 9]
    print("search 7 ->", "O" if bst_search(bst, 7) else "X")   # O
    print("search 6 ->", "O" if bst_search(bst, 6) else "X")   # X

    print("\n모든 예제 실행 완료")


if __name__ == "__main__":
    main()
