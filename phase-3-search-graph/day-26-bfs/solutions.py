# -*- coding: utf-8 -*-
"""
Day 26 - BFS (너비 우선 탐색): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(dist 배열 vs 레벨 끊기, 단일 소스 vs 다중 소스)을
두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from collections import deque, defaultdict


# ===========================================================================
# 1. Binary Tree Level Order Traversal (LeetCode #102)
#    레벨 끊기 BFS: size = len(q)로 현재 층만 꺼낸다. O(N).
# ===========================================================================
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class SolutionLevelOrder:
    def levelOrder(self, root):
        if root is None:
            return []
        res = []
        q = deque([root])
        while q:
            size = len(q)                  # 지금 큐 = 현재 레벨 전체
            level = []
            for _ in range(size):
                node = q.popleft()
                level.append(node.val)
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
            res.append(level)
        return res


# ===========================================================================
# 2. 게임 맵 최단거리 (프로그래머스 #1844)
#    격자 최단 거리 BFS. 시작 칸 거리 1(칸 수). 못 가면 -1. O(n*m).
# ===========================================================================
def solution_game_map(maps):
    n, m = len(maps), len(maps[0])
    dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
    dist = [[-1] * m for _ in range(n)]
    dist[0][0] = 1
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        for d in range(4):
            nr, nc = r + dr[d], c + dc[d]
            if (0 <= nr < n and 0 <= nc < m
                    and dist[nr][nc] == -1 and maps[nr][nc] == 1):
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist[n - 1][m - 1]


# ===========================================================================
# 3. Shortest Path in Binary Matrix (LeetCode #1091)
#    8방향 격자 BFS. 0이 통과 가능. O(n^2).
# ===========================================================================
class SolutionShortestBinary:
    def shortestPathBinaryMatrix(self, grid):
        n = len(grid)
        if grid[0][0] != 0 or grid[n - 1][n - 1] != 0:
            return -1
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]
        dist = [[-1] * n for _ in range(n)]
        dist[0][0] = 1
        q = deque([(0, 0)])
        while q:
            r, c = q.popleft()
            if r == n - 1 and c == n - 1:
                return dist[r][c]
            for dr2, dc2 in dirs:
                nr, nc = r + dr2, c + dc2
                if (0 <= nr < n and 0 <= nc < n
                        and dist[nr][nc] == -1 and grid[nr][nc] == 0):
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))
        return -1


# ===========================================================================
# 4. Rotting Oranges (LeetCode #994)
#    다중 소스 BFS(레벨=분). 썩은 것 전부를 시작 큐에. O(R*C).
# ===========================================================================
class SolutionRottingOranges:
    def orangesRotting(self, grid):
        R, C = len(grid), len(grid[0])
        q = deque()
        fresh = 0
        for r in range(R):
            for c in range(C):
                if grid[r][c] == 2:
                    q.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1
        dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
        minutes = 0
        while q and fresh > 0:              # 남은 신선 오렌지가 있을 때만 1분 진행
            minutes += 1
            for _ in range(len(q)):
                r, c = q.popleft()
                for d in range(4):
                    nr, nc = r + dr[d], c + dc[d]
                    if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        q.append((nr, nc))
        return minutes if fresh == 0 else -1


# ===========================================================================
# 5. 01 Matrix (LeetCode #542)
#    다중 소스 BFS: 모든 0을 소스로. "소스 뒤집기". O(R*C).
# ===========================================================================
class SolutionMatrix01:
    def updateMatrix(self, mat):
        R, C = len(mat), len(mat[0])
        dist = [[-1] * C for _ in range(R)]
        q = deque()
        for r in range(R):
            for c in range(C):
                if mat[r][c] == 0:
                    dist[r][c] = 0
                    q.append((r, c))
        dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
        while q:
            r, c = q.popleft()
            for d in range(4):
                nr, nc = r + dr[d], c + dc[d]
                if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))
        return dist


# ===========================================================================
# 6. 단어 변환 (프로그래머스 #43163)
#    상태 공간 BFS: 한 글자 차이가 간선. 최소 변환 = 최단 거리. O(N^2 * L).
# ===========================================================================
def solution_word_conversion(begin, target, words):
    if target not in words:
        return 0

    def diff_one(a, b):
        return sum(x != y for x, y in zip(a, b)) == 1

    q = deque([(begin, 0)])
    visited = {begin}
    while q:
        word, steps = q.popleft()
        if word == target:
            return steps
        for w in words:
            if w not in visited and diff_one(word, w):
                visited.add(w)
                q.append((w, steps + 1))
    return 0


# ===========================================================================
# 7. Open the Lock (LeetCode #752)
#    상태 공간 BFS: 4자리 상태, 각 자리 +/-1(순환). deadend + visited 차단.
# ===========================================================================
class SolutionOpenLock:
    def openLock(self, deadends, target):
        dead = set(deadends)
        if "0000" in dead:
            return -1
        if target == "0000":
            return 0
        visited = {"0000"}
        q = deque([("0000", 0)])
        while q:
            state, turns = q.popleft()
            for i in range(4):
                d = int(state[i])
                for nd in ((d + 1) % 10, (d - 1) % 10):
                    ns = state[:i] + str(nd) + state[i + 1:]
                    if ns not in visited and ns not in dead:
                        if ns == target:
                            return turns + 1
                        visited.add(ns)
                        q.append((ns, turns + 1))
        return -1


# ===========================================================================
# 8. Word Ladder (LeetCode #127)
#    상태 공간 BFS + 와일드카드 패턴 버킷으로 이웃 탐색 가속. O(N * L^2).
# ===========================================================================
class SolutionWordLadder:
    def ladderLength(self, beginWord, endWord, wordList):
        words = set(wordList)
        if endWord not in words:
            return 0
        L = len(beginWord)
        buckets = defaultdict(list)
        for w in words:
            for i in range(L):
                buckets[w[:i] + "*" + w[i + 1:]].append(w)
        visited = {beginWord}
        q = deque([(beginWord, 1)])
        while q:
            word, steps = q.popleft()
            if word == endWord:
                return steps
            for i in range(L):
                pat = word[:i] + "*" + word[i + 1:]
                for nxt in buckets[pat]:
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append((nxt, steps + 1))
        return 0


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    # 1. Level Order
    #        3
    #       / \
    #      9  20
    #         / \
    #        15  7
    root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
    lo = SolutionLevelOrder()
    assert lo.levelOrder(root) == [[3], [9, 20], [15, 7]]
    assert lo.levelOrder(None) == []

    # 2. 게임 맵 최단거리
    gmap1 = [[1, 0, 1, 1, 1],
             [1, 0, 1, 0, 1],
             [1, 0, 1, 1, 1],
             [1, 1, 1, 0, 1],
             [0, 0, 0, 0, 1]]
    assert solution_game_map(gmap1) == 11
    gmap2 = [[1, 0, 1, 1, 1],
             [1, 0, 1, 0, 1],
             [1, 0, 1, 1, 1],
             [1, 1, 1, 0, 0],
             [0, 0, 0, 0, 1]]
    assert solution_game_map(gmap2) == -1        # 도착 칸 고립

    # 3. Shortest Path in Binary Matrix
    sb = SolutionShortestBinary()
    assert sb.shortestPathBinaryMatrix([[0, 1], [1, 0]]) == 2
    assert sb.shortestPathBinaryMatrix(
        [[0, 0, 0], [1, 1, 0], [1, 1, 0]]) == 4
    assert sb.shortestPathBinaryMatrix(
        [[1, 0, 0], [1, 1, 0], [1, 1, 0]]) == -1  # 시작 칸이 벽

    # 4. Rotting Oranges
    ro = SolutionRottingOranges()
    assert ro.orangesRotting(
        [[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert ro.orangesRotting(
        [[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1  # 고립된 신선 오렌지
    assert ro.orangesRotting([[0, 2]]) == 0       # 신선 오렌지 없음

    # 5. 01 Matrix
    m01 = SolutionMatrix01()
    assert m01.updateMatrix(
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == \
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    assert m01.updateMatrix(
        [[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == \
        [[0, 0, 0], [0, 1, 0], [1, 2, 1]]

    # 6. 단어 변환
    assert solution_word_conversion(
        "hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 4
    assert solution_word_conversion(
        "hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0  # target 없음

    # 7. Open the Lock
    ol = SolutionOpenLock()
    assert ol.openLock(
        ["0201", "0101", "0102", "1212", "2002"], "0202") == 6
    assert ol.openLock(["8888"], "0009") == 1
    assert ol.openLock(
        ["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"],
        "8888") == -1                              # 목표가 완전히 포위됨
    assert ol.openLock(["0000"], "8888") == -1     # 시작이 deadend

    # 8. Word Ladder
    wl = SolutionWordLadder()
    assert wl.ladderLength(
        "hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert wl.ladderLength(
        "hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0  # endWord 없음

    print("Day 26 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()
