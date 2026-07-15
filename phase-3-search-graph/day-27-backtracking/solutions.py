# -*- coding: utf-8 -*-
"""
Day 27 - 백트래킹 (Backtracking): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(직접 백트래킹 vs itertools, 생성 vs 수학)을
두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from itertools import permutations


# ===========================================================================
# 1. Subsets (LeetCode #78)
#    (A) 이진 결정 백트래킹  (B) start 인덱스 방식. 둘 다 2^n개.
# ===========================================================================
class SolutionSubsets:
    def subsets(self, nums):
        res, path = [], []

        def dfs(i):
            if i == len(nums):
                res.append(path[:])
                return
            dfs(i + 1)                   # 불포함
            path.append(nums[i])         # choose(포함)
            dfs(i + 1)
            path.pop()                   # undo

        dfs(0)
        return res

    def subsets_start(self, nums):       # 대안: 모든 노드에서 기록
        res, path = [], []

        def dfs(start):
            res.append(path[:])
            for i in range(start, len(nums)):
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return res


# ===========================================================================
# 2. Permutations (LeetCode #46)
#    used 배열 백트래킹. n!개.
# ===========================================================================
class SolutionPermutations:
    def permute(self, nums):
        res, path, used = [], [], [False] * len(nums)

        def dfs():
            if len(path) == len(nums):
                res.append(path[:])
                return
            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                dfs()
                path.pop()
                used[i] = False

        dfs()
        return res


# ===========================================================================
# 3. Combinations (LeetCode #77)
#    start 인덱스로 오름차순 고정 + 남은 자리 가지치기.
# ===========================================================================
class SolutionCombinations:
    def combine(self, n, k):
        res, path = [], []

        def dfs(start):
            if len(path) == k:
                res.append(path[:])
                return
            for x in range(start, n - (k - len(path)) + 2):
                path.append(x)
                dfs(x + 1)
                path.pop()

        dfs(1)
        return res


# ===========================================================================
# 4. Combination Sum (LeetCode #39)
#    같은 수 재사용 허용(i 유지) + 정렬 후 초과 시 break 가지치기.
# ===========================================================================
class SolutionCombinationSum:
    def combinationSum(self, candidates, target):
        cand = sorted(candidates)
        res, path = [], []

        def dfs(start, remain):
            if remain == 0:
                res.append(path[:])
                return
            for i in range(start, len(cand)):
                if cand[i] > remain:     # 정렬돼 있으니 이후 전부 초과
                    break
                path.append(cand[i])
                dfs(i, remain - cand[i])  # i 유지 = 같은 수 재사용
                path.pop()

        dfs(0, target)
        return res


# ===========================================================================
# 5. Generate Parentheses (LeetCode #22)
#    열림/닫힘 개수 조건으로 유효 문자열만 생성(가지치기). 카탈란 수 개.
# ===========================================================================
class SolutionGenerateParentheses:
    def generateParenthesis(self, n):
        res = []

        def dfs(cur, open_cnt, close_cnt):
            if len(cur) == 2 * n:
                res.append(cur)
                return
            if open_cnt < n:
                dfs(cur + "(", open_cnt + 1, close_cnt)
            if close_cnt < open_cnt:
                dfs(cur + ")", open_cnt, close_cnt + 1)

        dfs("", 0, 0)
        return res


# ===========================================================================
# 6. 소수 찾기 (프로그래머스 #42839)
#    자릿수 순열로 모든 수 생성 -> 집합으로 중복 제거 -> 소수 개수.
# ===========================================================================
def _is_prime(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def solution_find_primes(numbers):
    made = set()
    for r in range(1, len(numbers) + 1):
        for perm in permutations(numbers, r):
            made.add(int("".join(perm)))   # int()가 앞자리 0을 정규화
    return sum(1 for x in made if _is_prime(x))


def solution_find_primes_backtrack(numbers):   # 대안: 직접 백트래킹
    digits = list(numbers)
    used = [False] * len(digits)
    made = set()

    def dfs(cur):
        if cur:
            made.add(int(cur))
        for i in range(len(digits)):
            if used[i]:
                continue
            used[i] = True
            dfs(cur + digits[i])
            used[i] = False

    dfs("")
    return sum(1 for x in made if _is_prime(x))


# ===========================================================================
# 7. 모음사전 (프로그래머스 #84512)
#    (A) A,E,I,O,U 순 DFS 생성으로 사전순 카운트
#    (B) 자릿값 가중치로 O(L) 수학 계산
# ===========================================================================
def solution_vowel_dict(word):
    vowels = "AEIOU"
    order = [0]
    answer = [-1]

    def dfs(cur):
        if cur:
            order[0] += 1
            if cur == word:
                answer[0] = order[0]
                return True
        if len(cur) == 5:
            return False
        for v in vowels:
            if dfs(cur + v):
                return True
        return False

    dfs("")
    return answer[0]


def solution_vowel_dict_math(word):
    vowels = "AEIOU"
    weight = [781, 156, 31, 6, 1]        # (5^(5-i)-1)/4
    return sum(vowels.index(c) * weight[i] for i, c in enumerate(word)) + len(word)


# ===========================================================================
# 8. 피로도 (프로그래머스 #87946)
#    방문 순열 완전탐색: cur >= 최소필요일 때만 진입(가지치기), 최댓값 갱신.
# ===========================================================================
def solution_fatigue(k, dungeons):
    n = len(dungeons)
    used = [False] * n
    best = [0]

    def dfs(cur, cnt):
        if cnt > best[0]:
            best[0] = cnt
        for i in range(n):
            need, cost = dungeons[i]
            if not used[i] and cur >= need:
                used[i] = True
                dfs(cur - cost, cnt + 1)
                used[i] = False          # undo

    dfs(k, 0)
    return best[0]


# ===========================================================================
# 9. Word Search (LeetCode #79)
#    격자 백트래킹: 방문 칸을 임시 '#'로 덮고 재귀 후 원복.
# ===========================================================================
class SolutionWordSearch:
    def exist(self, board, word):
        R, C = len(board), len(board[0])

        def dfs(r, c, i):
            if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]:
                return False
            if i == len(word) - 1:
                return True
            tmp = board[r][c]
            board[r][c] = "#"            # choose(방문 표시)
            found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1)
                     or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
            board[r][c] = tmp            # undo(원복)
            return found

        for r in range(R):
            for c in range(C):
                if dfs(r, c, 0):
                    return True
        return False


# ===========================================================================
# 10. N-Queens (LeetCode #51)
#     열/두 대각선 집합으로 O(1) 가지치기. 모든 배치를 보드 문자열로 반환.
# ===========================================================================
class SolutionNQueens:
    def solveNQueens(self, n):
        res = []
        cols, diag, anti = set(), set(), set()
        queens = []                      # 각 행의 퀸 열 위치

        def place(r):
            if r == n:
                res.append(["".join("Q" if c == col else "." for c in range(n))
                            for col in queens])
                return
            for c in range(n):
                if c in cols or (r - c) in diag or (r + c) in anti:
                    continue
                cols.add(c); diag.add(r - c); anti.add(r + c); queens.append(c)
                place(r + 1)
                queens.pop()
                cols.discard(c); diag.discard(r - c); anti.discard(r + c)

        place(0)
        return res


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _run_tests():
    # 1. Subsets
    ss = SolutionSubsets()
    s1 = sorted(sorted(x) for x in ss.subsets([1, 2, 3]))
    s2 = sorted(sorted(x) for x in ss.subsets_start([1, 2, 3]))
    assert len(s1) == 8 and s1 == s2
    assert [] in ss.subsets([1, 2, 3]) and [1, 2, 3] in ss.subsets([1, 2, 3])

    # 2. Permutations
    sp = SolutionPermutations()
    perms = sp.permute([1, 2, 3])
    assert len(perms) == 6
    assert sorted(perms) == sorted(list(p) for p in permutations([1, 2, 3]))

    # 3. Combinations
    sc = SolutionCombinations()
    combs = sc.combine(4, 2)
    assert len(combs) == 6                 # 4C2
    assert [1, 2] in combs and [3, 4] in combs

    # 4. Combination Sum
    scs = SolutionCombinationSum()
    assert sorted(scs.combinationSum([2, 3, 6, 7], 7)) == [[2, 2, 3], [7]]
    assert sorted(scs.combinationSum([2, 3, 5], 8)) == \
        [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert scs.combinationSum([2], 1) == []

    # 5. Generate Parentheses
    sg = SolutionGenerateParentheses()
    g3 = sg.generateParenthesis(3)
    assert len(g3) == 5                     # 카탈란 수 C(3)
    assert sorted(g3) == sorted(
        ["((()))", "(()())", "(())()", "()(())", "()()()"])
    assert sg.generateParenthesis(1) == ["()"]

    # 6. 소수 찾기
    assert solution_find_primes("17") == 3          # 7, 17, 71
    assert solution_find_primes("011") == 2         # 11, 101
    assert solution_find_primes_backtrack("17") == 3
    assert solution_find_primes_backtrack("011") == 2

    # 7. 모음사전
    for w, ans in [("AAAAE", 6), ("AAAE", 10), ("I", 1563), ("EIO", 1189)]:
        assert solution_vowel_dict(w) == ans
        assert solution_vowel_dict_math(w) == ans

    # 8. 피로도
    assert solution_fatigue(
        80, [[80, 20], [50, 40], [30, 10]]) == 3
    assert solution_fatigue(80, [[90, 10]]) == 0    # 첫 던전도 못 감

    # 9. Word Search
    sw = SolutionWordSearch()
    board = [["A", "B", "C", "E"],
             ["S", "F", "C", "S"],
             ["A", "D", "E", "E"]]
    assert sw.exist([row[:] for row in board], "ABCCED") is True
    assert sw.exist([row[:] for row in board], "SEE") is True
    assert sw.exist([row[:] for row in board], "ABCB") is False

    # 10. N-Queens
    sn = SolutionNQueens()
    assert len(sn.solveNQueens(4)) == 2
    assert len(sn.solveNQueens(1)) == 1
    assert len(sn.solveNQueens(8)) == 92
    # 반환 보드가 실제로 유효한지(각 행에 Q 하나) 간단 확인
    for board_sol in sn.solveNQueens(4):
        assert all(row.count("Q") == 1 for row in board_sol)

    print("Day 27 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()
