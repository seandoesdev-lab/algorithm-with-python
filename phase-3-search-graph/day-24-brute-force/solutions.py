# -*- coding: utf-8 -*-
"""
Day 24 - 완전 탐색 (Brute Force): 연습문제 해설

플랫폼 시그니처 유지: LeetCode = class Solution / 프로그래머스 = def solution.
가능하면 한 문제에 여러 접근(재귀 vs itertools vs 비트마스크)을 두고 복잡도를 비교한다.
콘솔 안전 규칙: print 문자열에는 ASCII 기호(=, -, O, X)만 사용한다.
실행: PYTHONIOENCODING=cp949 python solutions.py
"""

from itertools import permutations, combinations, product


# ===========================================================================
# 1. 모의고사 (프로그래머스 #42840)
#    세 패턴을 사이클로 두고 모든 문제를 전수 채점. O(n).
# ===========================================================================
def solution_mock(answers):
    patterns = [
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5],
    ]
    scores = [0, 0, 0]
    for i, ans in enumerate(answers):
        for p in range(3):
            if patterns[p][i % len(patterns[p])] == ans:
                scores[p] += 1
    best = max(scores)
    return [p + 1 for p in range(3) if scores[p] == best]


# ===========================================================================
# 2. Two Sum (LeetCode #1)
#    완전 탐색 O(n^2) vs 해시맵 O(n).
# ===========================================================================
class SolutionTwoSum:
    def twoSum(self, nums, target):
        """해시맵. O(n) 시간, O(n) 공간."""
        seen = {}                          # 값 -> 인덱스
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
        return []

    def twoSum_brute(self, nums, target):
        """완전 탐색. O(n^2)."""
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []


# ===========================================================================
# 3. Subsets (LeetCode #78)
#    재귀(선택/미선택) vs 비트마스크. 둘 다 2^n.
# ===========================================================================
class SolutionSubsets:
    def subsets(self, nums):
        """재귀 완전 탐색. O(n * 2^n)."""
        res = []

        def go(i, chosen):
            if i == len(nums):
                res.append(chosen[:])
                return
            go(i + 1, chosen)             # nums[i] 빼고
            chosen.append(nums[i])
            go(i + 1, chosen)             # nums[i] 넣고
            chosen.pop()

        go(0, [])
        return res

    def subsets_bitmask(self, nums):
        """비트마스크. 재귀 없이 2^n 순회."""
        n = len(nums)
        res = []
        for mask in range(1 << n):
            res.append([nums[i] for i in range(n) if mask & (1 << i)])
        return res


# ===========================================================================
# 4. 소수 찾기 (프로그래머스 #42839)
#    순열로 만들 수 있는 모든 수 -> set -> 소수 판정.
# ===========================================================================
def solution_primes(numbers):
    cards = list(numbers)
    made = set()
    for length in range(1, len(cards) + 1):
        for perm in permutations(cards, length):
            made.add(int("".join(perm)))   # 앞자리 0은 int 변환에서 제거
    return sum(1 for x in made if _is_prime(x))


def _is_prime(x):
    if x < 2:
        return False
    i = 2
    while i * i <= x:                      # 2..sqrt(x)
        if x % i == 0:
            return False
        i += 1
    return True


# ===========================================================================
# 5. Permutations (LeetCode #46)
#    재귀(used 배열) vs itertools. 둘 다 n!.
# ===========================================================================
class SolutionPermutations:
    def permute(self, nums):
        """재귀 완전 탐색. O(n * n!)."""
        res = []
        used = [False] * len(nums)
        cur = []

        def go():
            if len(cur) == len(nums):
                res.append(cur[:])
                return
            for i in range(len(nums)):
                if used[i]:
                    continue
                used[i] = True
                cur.append(nums[i])
                go()
                cur.pop()
                used[i] = False

        go()
        return res

    def permute_itertools(self, nums):
        """비교용. itertools.permutations."""
        return [list(p) for p in permutations(nums)]


# ===========================================================================
# 6. 카펫 (프로그래머스 #42842)
#    약수 완전 탐색: 세로를 1..sqrt(total) 로 전수.
# ===========================================================================
def solution_carpet(brown, yellow):
    total = brown + yellow
    h = 1
    while h * h <= total:                  # 세로 후보(가로 >= 세로)
        if total % h == 0:
            w = total // h                 # 가로
            if (w - 2) * (h - 2) == yellow:   # 내부 노란 넓이 일치
                return [w, h]
        h += 1
    return []


# ===========================================================================
# 7. Combinations (LeetCode #77)
#    재귀(start 인덱스) vs itertools. nCk.
# ===========================================================================
class SolutionCombinations:
    def combine(self, n, k):
        """재귀 완전 탐색. start로 오름차순만 생성해 중복 차단."""
        res = []
        cur = []

        def go(start):
            if len(cur) == k:
                res.append(cur[:])
                return
            for x in range(start, n + 1):
                cur.append(x)
                go(x + 1)
                cur.pop()

        go(1)
        return res

    def combine_itertools(self, n, k):
        return [list(c) for c in combinations(range(1, n + 1), k)]


# ===========================================================================
# 8. Letter Combinations of a Phone Number (LeetCode #17)
#    곱집합 완전 탐색: product 또는 재귀 DFS.
# ===========================================================================
class SolutionLetterCombos:
    KEYPAD = {
        "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
        "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
    }

    def letterCombinations(self, digits):
        """itertools.product. O(4^n)."""
        if not digits:
            return []
        groups = [self.KEYPAD[d] for d in digits]
        return ["".join(p) for p in product(*groups)]

    def letterCombinations_dfs(self, digits):
        """재귀 DFS로 같은 곱집합 생성."""
        if not digits:
            return []
        res = []

        def go(i, path):
            if i == len(digits):
                res.append(path)
                return
            for ch in self.KEYPAD[digits[i]]:
                go(i + 1, path + ch)

        go(0, "")
        return res


# ===========================================================================
# 9. Combination Sum (LeetCode #39)
#    중복 사용 허용 조합. start 유지로 오름차순, 남은 합 음수면 가지치기.
# ===========================================================================
class SolutionCombinationSum:
    def combinationSum(self, candidates, target):
        res = []
        cur = []

        def go(start, remain):
            if remain == 0:
                res.append(cur[:])
                return
            if remain < 0:
                return                     # 가지치기
            for i in range(start, len(candidates)):
                cur.append(candidates[i])
                go(i, remain - candidates[i])   # i 유지: 같은 수 재사용
                cur.pop()

        go(0, target)
        return res


# ===========================================================================
# 10. Subsets II (LeetCode #90)
#     중복 원소 배열의 부분집합. 정렬 후 같은 깊이 중복 스킵.
# ===========================================================================
class SolutionSubsetsII:
    def subsetsWithDup(self, nums):
        nums.sort()
        res = []
        cur = []

        def go(start):
            res.append(cur[:])
            for i in range(start, len(nums)):
                if i > start and nums[i] == nums[i - 1]:
                    continue               # 같은 깊이의 중복 값 건너뛰기
                cur.append(nums[i])
                go(i + 1)
                cur.pop()

        go(0)
        return res


# ===========================================================================
# 자체 검증 (assert)
# ===========================================================================
def _norm(list_of_lists):
    """순서 무관 비교용: 각 후보를 정렬하고 전체를 정렬."""
    return sorted(sorted(x) for x in list_of_lists)


def _run_tests():
    assert solution_mock([1, 2, 3, 4, 5]) == [1]
    assert solution_mock([1, 3, 2, 4, 2]) == [1, 2, 3]

    ts = SolutionTwoSum()
    assert ts.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert ts.twoSum_brute([3, 2, 4], 6) == [1, 2]
    assert ts.twoSum_brute([2, 7, 11, 15], 9) == [0, 1]

    ss = SolutionSubsets()
    expected_sub = _norm([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
    assert _norm(ss.subsets([1, 2, 3])) == expected_sub
    assert _norm(ss.subsets_bitmask([1, 2, 3])) == expected_sub
    assert len(ss.subsets([1, 2, 3, 4])) == 16

    assert solution_primes("17") == 3        # 7, 17, 71
    assert solution_primes("011") == 2       # 11, 101
    assert solution_primes("11") == 1        # 만들 수 있는 수 {1, 11} 중 소수는 11

    sp = SolutionPermutations()
    assert _norm(sp.permute([1, 2, 3])) == _norm(sp.permute_itertools([1, 2, 3]))
    assert len(sp.permute([1, 2, 3, 4])) == 24

    assert solution_carpet(10, 2) == [4, 3]
    assert solution_carpet(8, 1) == [3, 3]
    assert solution_carpet(24, 24) == [8, 6]

    sc = SolutionCombinations()
    assert _norm(sc.combine(4, 2)) == _norm(sc.combine_itertools(4, 2))
    assert len(sc.combine(5, 3)) == 10       # 5C3

    lc = SolutionLetterCombos()
    assert sorted(lc.letterCombinations("23")) == sorted(
        ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"])
    assert lc.letterCombinations("") == []
    assert sorted(lc.letterCombinations_dfs("23")) == sorted(lc.letterCombinations("23"))

    cs = SolutionCombinationSum()
    assert _norm(cs.combinationSum([2, 3, 6, 7], 7)) == _norm([[2, 2, 3], [7]])
    assert _norm(cs.combinationSum([2, 3, 5], 8)) == _norm(
        [[2, 2, 2, 2], [2, 3, 3], [3, 5]])

    s2 = SolutionSubsetsII()
    assert _norm(s2.subsetsWithDup([1, 2, 2])) == _norm(
        [[], [1], [2], [1, 2], [2, 2], [1, 2, 2]])

    print("Day 24 solutions: all tests passed OK")


if __name__ == "__main__":
    _run_tests()
