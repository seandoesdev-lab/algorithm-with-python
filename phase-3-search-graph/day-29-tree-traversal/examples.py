# -*- coding: utf-8 -*-
"""
Day 29 - 트리 순회.응용 (Tree Traversal): 예제 코드

트리는 사이클 없는 특수 그래프다. 부모만 피하면 visited 없이도 순회가 끝난다.
이진 트리의 네 가지 순회(전위/중위/후위/레벨)와 대표 응용(깊이, 뒤집기,
경로 합, 일반 N진 트리)을 재귀와 반복 두 방식으로 정리한다.

콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python examples.py
"""

from collections import deque


# ---------------------------------------------------------------------------
# 0) 이진 트리 노드 + 리스트로부터 트리 만들기(테스트 편의용)
# ---------------------------------------------------------------------------
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(level_values):
    """LeetCode 스타일 레벨 순서 리스트(None 포함) -> 이진 트리 루트.

    예: [1, 2, 3, None, 4] ->
            1
           / \
          2   3
           \
            4
    """
    if not level_values:
        return None
    root = TreeNode(level_values[0])
    q = deque([root])
    i, n = 1, len(level_values)
    while q and i < n:
        node = q.popleft()
        if i < n:                                # 왼쪽 자식
            if level_values[i] is not None:
                node.left = TreeNode(level_values[i])
                q.append(node.left)
            i += 1
        if i < n:                                # 오른쪽 자식
            if level_values[i] is not None:
                node.right = TreeNode(level_values[i])
                q.append(node.right)
            i += 1
    return root


# ---------------------------------------------------------------------------
# 1) 깊이 우선 순회 3종 - 재귀 (전위/중위/후위)
#    차이는 "루트를 방문(기록)하는 시점" 하나뿐이다.
# ---------------------------------------------------------------------------
def preorder(root):          # 루트 -> 왼쪽 -> 오른쪽
    if root is None:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)


def inorder(root):           # 왼쪽 -> 루트 -> 오른쪽 (BST면 오름차순)
    if root is None:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


def postorder(root):         # 왼쪽 -> 오른쪽 -> 루트 (자식 먼저)
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


# ---------------------------------------------------------------------------
# 2) 전위 순회 - 반복(명시적 스택). 재귀 깊이 한계를 피한다.
#    오른쪽을 먼저 push해야 왼쪽이 먼저 pop된다.
# ---------------------------------------------------------------------------
def preorder_iter(root):
    if root is None:
        return []
    order, stack = [], [root]
    while stack:
        node = stack.pop()
        order.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


# ---------------------------------------------------------------------------
# 3) 중위 순회 - 반복(스택). 왼쪽 끝까지 내려가며 쌓고, 꺼내 기록 후 오른쪽.
# ---------------------------------------------------------------------------
def inorder_iter(root):
    order, stack = [], []
    cur = root
    while cur or stack:
        while cur:               # 왼쪽 끝까지 내려가며 스택에 쌓기
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()        # 가장 왼쪽부터 꺼내 기록
        order.append(cur.val)
        cur = cur.right          # 오른쪽 서브트리로
    return order


# ---------------------------------------------------------------------------
# 4) 레벨 순회(BFS) - 큐. 층별로 나눠 담기.
# ---------------------------------------------------------------------------
def level_order(root):
    if root is None:
        return []
    result, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):      # 현재 층의 노드 수만큼만 처리
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result


# ---------------------------------------------------------------------------
# 5) 대표 응용 - 최대 깊이 / 뒤집기 / 루트-리프 경로 합
# ---------------------------------------------------------------------------
def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def invert(root):                # 좌우 자식을 재귀로 맞바꾸기
    if root is None:
        return None
    root.left, root.right = invert(root.right), invert(root.left)
    return root


def has_path_sum(root, target):  # 루트->리프 합이 target인 경로 존재?
    if root is None:
        return False
    if root.left is None and root.right is None:   # 리프
        return root.val == target
    rest = target - root.val
    return has_path_sum(root.left, rest) or has_path_sum(root.right, rest)


# ---------------------------------------------------------------------------
# 6) 일반 트리 = 그래프 순회에 "부모 회피"를 얹기 (visited 대신 parent)
#    트리는 사이클이 없으므로 방문한 부모만 건너뛰면 무한 루프가 없다.
# ---------------------------------------------------------------------------
def tree_dfs(adj, node, parent):
    order = [node]
    for nxt in adj[node]:
        if nxt != parent:            # visited 배열 없이 부모만 회피
            order += tree_dfs(adj, nxt, node)
    return order


# ---------------------------------------------------------------------------
# 데모 실행
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    #        1
    #       / \
    #      2   3
    #     / \    \
    #    4   5    6
    root = build_tree([1, 2, 3, 4, 5, None, 6])

    print("preorder     :", preorder(root))          # [1, 2, 4, 5, 3, 6]
    print("inorder      :", inorder(root))           # [4, 2, 5, 1, 3, 6]
    print("postorder    :", postorder(root))         # [4, 5, 2, 6, 3, 1]
    print("preorder_iter:", preorder_iter(root))     # [1, 2, 4, 5, 3, 6]
    print("inorder_iter :", inorder_iter(root))      # [4, 2, 5, 1, 3, 6]
    print("level_order  :", level_order(root))       # [[1], [2, 3], [4, 5, 6]]
    print("max_depth    :", max_depth(root))         # 3
    print("has_path_sum(1+2+5=8):", has_path_sum(root, 8))   # True

    inv = invert(build_tree([1, 2, 3, 4, 5, None, 6]))
    print("invert level :", level_order(inv))        # [[1], [3, 2], [6, 5, 4]]

    # 일반 트리(무방향 인접 리스트): 0-1, 0-2, 1-3, 1-4
    adj = {0: [1, 2], 1: [0, 3, 4], 2: [0], 3: [1], 4: [1]}
    print("tree_dfs(0)  :", tree_dfs(adj, 0, -1))    # [0, 1, 3, 4, 2]

    print("examples OK")
